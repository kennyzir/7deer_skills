#!/usr/bin/env python3
"""SignalLayer OpenClaw API client.

The server requires an explicit linkCount. This CLI intentionally supplies a
client-side default of 200 when --quantity is omitted.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
MEMORY_DIR = PROJECT_DIR / "memory"
CONFIG_FILE = MEMORY_DIR / "signallayer-api-user.md"
DEFAULT_BASE_URL = "https://signallayer.io/api/openclaw"


class SignalLayerError(RuntimeError):
    """A network, protocol, or API error with actionable context."""


def load_api_key() -> str | None:
    """Load the key from the environment first, then the legacy memory file."""
    environment_key = os.environ.get("SIGNALLAYER_API_KEY", "").strip()
    if environment_key:
        return environment_key

    if not CONFIG_FILE.exists():
        return None

    content = CONFIG_FILE.read_text(encoding="utf-8")
    match = re.search(r"^- \*\*Key\*\*: `([^`]+)`\s*$", content, re.MULTILINE)
    return match.group(1).strip() if match else None


def save_config(api_key: str, account_email: str | None = None) -> None:
    """Save a legacy plaintext config while preserving local campaign history."""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    existing = CONFIG_FILE.read_text(encoding="utf-8") if CONFIG_FILE.exists() else ""
    history = ""
    marker = "## Campaign 记录"
    if marker in existing:
        history = existing.split(marker, 1)[1].lstrip("\n")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    content = f"""# SignalLayer API 配置（用户）

> 安全提示：这是兼容用的明文配置。优先使用 SIGNALLAYER_API_KEY 环境变量，且不要提交本文件。

## API Key
- **Key**: `{api_key}`
- **配置时间**: {timestamp} UTC

## 账户信息
- **Email**: {account_email or '（通过 API 查询）'}
- **积分余额**: （通过 /credits 查询）

## Campaign 记录

{history}"""
    CONFIG_FILE.write_text(content, encoding="utf-8")
    try:
        CONFIG_FILE.chmod(0o600)
    except OSError:
        # Windows ACLs do not map cleanly to POSIX modes. The warning above and
        # .gitignore protection remain the portable safety boundary.
        pass


class SignalLayerClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.api_key = (api_key or load_api_key() or "").strip()
        if not self.api_key:
            raise SignalLayerError(
                "Missing API key. Set SIGNALLAYER_API_KEY or run --configure."
            )
        if not self.api_key.startswith("sl_"):
            raise SignalLayerError("Invalid API key format: expected an sl_ prefix.")

        configured_url = base_url or os.environ.get(
            "SIGNALLAYER_BASE_URL", DEFAULT_BASE_URL
        )
        self.base_url = configured_url.rstrip("/")
        self.session = session or requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "signallayer-backlinks-client/2.0",
            }
        )

    def request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        try:
            response = self.session.request(
                method,
                f"{self.base_url}{path}",
                timeout=(10, 30),
                **kwargs,
            )
        except requests.RequestException as error:
            raise SignalLayerError(f"Network error calling {path}: {error}") from error

        try:
            payload = response.json()
        except ValueError as error:
            content_type = response.headers.get("content-type", "unknown")
            raise SignalLayerError(
                f"SignalLayer returned non-JSON data "
                f"(HTTP {response.status_code}, content-type {content_type}). "
                "Check the Base URL and endpoint path."
            ) from error

        if not response.ok or not payload.get("success"):
            code = payload.get("code", "UNKNOWN_ERROR")
            message = payload.get("error", f"HTTP {response.status_code}")
            field = payload.get("field")
            suffix = f" (field: {field})" if field else ""
            raise SignalLayerError(
                f"SignalLayer API error {response.status_code} {code}: {message}{suffix}"
            )

        return payload

    def credits(self) -> dict[str, Any]:
        return self.request("GET", "/credits")

    def create_campaign(
        self,
        target_url: str,
        brand: str,
        quantity: int = 200,
        keywords: str = "",
        strategy: str = "safety",
        speed: str = "natural",
        drip_days: int = 14,
    ) -> dict[str, Any]:
        payload = {
            "targetUrl": target_url,
            "brandName": brand,
            "keywords": keywords,
            "linkCount": quantity,
            "strategy": strategy,
            "speed": speed,
            "dripDays": drip_days,
            "source": "openclaw-client",
        }
        result = self.request("POST", "/create-campaign", json=payload)
        update_memory(result)
        return result

    def campaign_status(self, campaign_id: str) -> dict[str, Any]:
        return self.request("GET", f"/campaign-status/{campaign_id}")

    def campaigns(self, limit: int = 20, offset: int = 0) -> dict[str, Any]:
        return self.request(
            "GET", "/campaigns", params={"limit": limit, "offset": offset}
        )


def update_memory(result: dict[str, Any]) -> None:
    """Append non-secret campaign metadata to the optional local history."""
    if not CONFIG_FILE.exists() or not result.get("success"):
        return

    campaign = result.get("campaign", {})
    content = CONFIG_FILE.read_text(encoding="utf-8")
    marker = "## Campaign 记录"
    if marker not in content:
        content += f"\n{marker}\n"

    campaign_numbers = [
        int(value) for value in re.findall(r"### Campaign #(\d+)", content)
    ]
    next_number = max(campaign_numbers, default=0) + 1
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    entry = f"""
### Campaign #{next_number}
- **Campaign ID**: {campaign.get('id', 'N/A')}
- **目标**: {campaign.get('targetUrl', 'N/A')}
- **品牌**: {campaign.get('brandName', 'N/A')}
- **关键词**: {campaign.get('keywords', '')}
- **外链数量**: {campaign.get('linkCount', 'N/A')}
- **策略**: {campaign.get('strategy', 'N/A')}
- **速度**: {campaign.get('speed', 'N/A')}
- **状态**: {campaign.get('status', 'N/A')}
- **创建时间**: {timestamp}
"""
    CONFIG_FILE.write_text(content.rstrip() + "\n" + entry, encoding="utf-8")


def configure() -> bool:
    print("SignalLayer API Key 配置")
    print("推荐方案：设置 SIGNALLAYER_API_KEY 环境变量。")
    print("当前操作会将 Key 明文保存到本 Skill 的 memory 目录。")
    api_key = input("请输入 SignalLayer API Key: ").strip()
    if not api_key.startswith("sl_"):
        print("❌ API Key 格式错误，应以 sl_ 开头", file=sys.stderr)
        return False

    try:
        client = SignalLayerClient(api_key=api_key)
        result = client.credits()
    except SignalLayerError as error:
        print(f"❌ API Key 验证失败: {error}", file=sys.stderr)
        return False

    save_config(api_key, result.get("email"))
    credits = result.get("credits", {})
    print(f"✅ Key 已通过服务端验证，可用积分：{credits.get('totalAvailable', 0)}")
    return True


def print_campaign(campaign: dict[str, Any]) -> None:
    progress = campaign.get("progress")
    print(f"Campaign ID: {campaign.get('id')}")
    print(f"状态: {campaign.get('status')}")
    if isinstance(progress, dict):
        print(
            "进度: "
            f"{progress.get('completed', 0)}/{progress.get('total', 0)} "
            f"({progress.get('percent', 0)}%)"
        )
        print(f"剩余: {progress.get('pending', 0)}")
    print(f"创建时间: {campaign.get('createdAt')}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="SignalLayer Backlinks Client",
        epilog=(
            "注意：--quantity 的 200 是客户端默认值；"
            "服务端 API 的 linkCount 始终为必填字段。"
        ),
    )
    parser.add_argument("--configure", action="store_true", help="验证并保存 API Key")
    parser.add_argument("--credits", action="store_true", help="验证 Key 并查询积分")
    parser.add_argument("--target", help="目标网站 URL")
    parser.add_argument("--brand", help="品牌名称")
    parser.add_argument("--keywords", default="", help="关键词文本")
    parser.add_argument(
        "--quantity", type=int, default=200, help="外链数量（客户端默认 200）"
    )
    parser.add_argument(
        "--strategy",
        default="safety",
        choices=["safety", "neutral", "aggressive"],
    )
    parser.add_argument(
        "--speed", default="natural", choices=["natural", "standard", "drip"]
    )
    parser.add_argument("--drip-days", type=int, default=14)
    parser.add_argument("--status", metavar="CAMPAIGN_ID", help="查询单个 Campaign")
    parser.add_argument("--list", action="store_true", help="从服务端查询 Campaign 列表")
    parser.add_argument("--limit", type=int, default=20, help="列表页大小（1-100）")
    parser.add_argument("--offset", type=int, default=0, help="列表偏移量")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.configure:
        return 0 if configure() else 1

    try:
        client = SignalLayerClient()
        if args.credits:
            print(json.dumps(client.credits(), ensure_ascii=False, indent=2))
            return 0

        if args.status:
            result = client.campaign_status(args.status)
            print_campaign(result["campaign"])
            return 0

        if args.list:
            if not 1 <= args.limit <= 100 or not 0 <= args.offset <= 100000:
                raise SignalLayerError(
                    "--limit must be 1-100 and --offset must be 0-100000"
                )
            result = client.campaigns(args.limit, args.offset)
            for campaign in result.get("campaigns", []):
                print_campaign(campaign)
                print("-")
            print(json.dumps(result.get("pagination", {}), ensure_ascii=False))
            return 0

        if args.target and args.brand:
            if args.speed == "drip" and not 10 <= args.drip_days <= 30:
                raise SignalLayerError("--drip-days must be 10-30 for drip speed")
            result = client.create_campaign(
                target_url=args.target,
                brand=args.brand,
                quantity=args.quantity,
                keywords=args.keywords,
                strategy=args.strategy,
                speed=args.speed,
                drip_days=args.drip_days,
            )
            print_campaign(result["campaign"])
            credits = result.get("credits", {})
            print(
                f"积分：免费 {credits.get('freeUsed', 0)}，"
                f"付费 {credits.get('paidUsed', 0)}"
            )
            return 0

        build_parser().print_help()
        return 2
    except SignalLayerError as error:
        print(f"❌ {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
