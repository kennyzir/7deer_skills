#!/usr/bin/env python3
"""
Batch Submitter Script v3 - 完整版
支持从文件读取目录列表，批量提交
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from playwright.async_api import async_playwright

DEFAULT_DATA = {
    "name": "",
    "url": "",
    "description": "",
    "email": "",
    "category": "Developer Tools",
}


async def check_directory(page, url: str) -> dict:
    """检测目录状态"""
    result = {"url": url, "status": "unknown", "reason": ""}

    try:
        await page.goto(url, timeout=20000, wait_until="domcontentloaded")
        await asyncio.sleep(2)

        content = (await page.content()).lower()

        # 检测各种状态
        if "login" in content and ("required" in content or "sign in" in content):
            result["status"] = "needs_login"
            result["reason"] = "Requires login"
        elif "$" in content and ("payment" in content or "paid" in content or "premium" in content):
            result["status"] = "paid"
            result["reason"] = "Paid directory"
        elif "404" in content or "not found" in content:
            result["status"] = "not_found"
            result["reason"] = "Page not found"
        elif '<form' in content:
            result["status"] = "can_submit"
            result["reason"] = "Has form"
        else:
            result["status"] = "unknown"
            result["reason"] = "No form detected"

    except Exception as e:
        result["status"] = "error"
        result["reason"] = str(e)[:50]

    return result


async def submit_to_directory(page, url: str, data: dict) -> dict:
    """提交到目录"""
    result = {"url": url, "status": "failed", "message": ""}

    try:
        await page.goto(url, timeout=30000)
        await page.wait_for_load_state("networkidle", timeout=15000)
        await asyncio.sleep(2)

        # 尝试填写各字段
        filled = []

        # Name
        for sel in ['input[name*="name" i]', 'input[id*="name" i]', 'input[placeholder*="name" i]']:
            try:
                el = await page.query_selector(sel)
                if el and await el.is_visible():
                    await el.fill(data.get("name", ""))
                    filled.append("name")
                    break
            except:
                continue

        # URL
        for sel in ['input[name*="url" i]', 'input[name*="website" i]', 'input[name*="link" i]']:
            try:
                el = await page.query_selector(sel)
                if el and await el.is_visible():
                    await el.fill(data.get("url", ""))
                    filled.append("url")
                    break
            except:
                continue

        # Description
        for sel in ['textarea[name*="desc" i]', 'textarea[id*="desc" i]', 'textarea[placeholder*="desc" i]']:
            try:
                el = await page.query_selector(sel)
                if el and await el.is_visible():
                    await el.fill(data.get("description", ""))
                    filled.append("desc")
                    break
            except:
                continue

        # Email
        for sel in ['input[type="email"]', 'input[name*="email" i]', 'input[id*="email" i]']:
            try:
                el = await page.query_selector(sel)
                if el and await el.is_visible():
                    await el.fill(data.get("email", ""))
                    filled.append("email")
                    break
            except:
                continue

        if not filled:
            result["message"] = "No fields filled"
            return result

        # 点击提交
        for sel in ['button[type="submit"]', 'input[type="submit"]', 'button:has-text("Submit")']:
            try:
                btn = await page.query_selector(sel)
                if btn and await btn.is_visible():
                    await btn.click()
                    await asyncio.sleep(3)
                    break
            except:
                continue

        # 检测结果
        final = (await page.content()).lower()
        if "thank" in final or "success" in final or "submitted" in final:
            result["status"] = "success"
            result["message"] = f"Submitted! ({', '.join(filled)})"
        else:
            result["status"] = "partial"
            result["message"] = f"Filled only: {', '.join(filled)}"

    except Exception as e:
        result["status"] = "error"
        result["message"] = str(e)[:50]

    return result


async def batch_check(urls: list) -> dict:
    """批量检测目录"""
    print(f"\n[CHECK] Testing {len(urls)} directories...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        results = {"can_submit": [], "paid": [], "needs_login": [], "not_found": [], "error": [], "unknown": []}

        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] Checking {url[:50]}...", end=" ", flush=True)
            result = await check_directory(page, url)

            if result["status"] == "can_submit":
                print(f"[OK] {result['reason']}")
                results["can_submit"].append(url)
            elif result["status"] == "paid":
                print(f"[PAID] {result['reason']}")
                results["paid"].append(url)
            elif result["status"] == "needs_login":
                print(f"[LOGIN] {result['reason']}")
                results["needs_login"].append(url)
            elif result["status"] == "not_found":
                print(f"[404] {result['reason']}")
                results["not_found"].append(url)
            elif result["status"] == "error":
                print(f"[ERR] {result['reason']}")
                results["error"].append(url)
            else:
                print(f"[?] {result['reason']}")
                results["unknown"].append(url)

            await asyncio.sleep(1)

        await browser.close()

    return results


async def batch_submit(urls: list, data: dict) -> list:
    """批量提交"""
    print(f"\n[SUBMIT] Submitting to {len(urls)} directories...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        results = []

        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] {url[:50]}...", end=" ", flush=True)
            result = await submit_to_directory(page, url, data)
            results.append(result)

            if result["status"] == "success":
                print(f"[OK] {result['message']}")
            elif result["status"] == "partial":
                print(f"[PARTIAL] {result['message']}")
            else:
                print(f"[FAIL] {result['message']}")

            await asyncio.sleep(3)  # 间隔3秒

        await browser.close()

    return results


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Batch submit to directories")
    parser.add_argument("--site", required=True, help="Website URL")
    parser.add_argument("--name", default="", help="Tool name")
    parser.add_argument("--description", default="", help="Description")
    parser.add_argument("--email", default="", help="Email")
    parser.add_argument("--directories", default="", help="File with directory URLs")
    parser.add_argument("--check-only", action="store_true", help="Only check, don't submit")
    args = parser.parse_args()

    # 读取目录列表
    urls = []
    if args.directories and os.path.exists(args.directories):
        with open(args.directories, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    else:
        print("Error: Please provide --directories file")
        return

    print(f"[INFO] Loaded {len(urls)} directories")

    # 构建数据
    data = DEFAULT_DATA.copy()
    data["url"] = args.site
    data["name"] = args.name or input("Name: ")
    data["description"] = args.description or input("Description: ")
    data["email"] = args.email or input("Email: ")

    # 步骤1: 批量检测
    check_results = await batch_check(urls)

    print(f"\n[RESULT] Check complete:")
    print(f"  [OK] Can submit: {len(check_results['can_submit'])}")
    print(f"  [PAID] Paid: {len(check_results['paid'])}")
    print(f"  🔐 Needs login: {len(check_results['needs_login'])}")
    print(f"  ❌ Not found: {len(check_results['not_found'])}")
    print(f"  ⚠️ Error: {len(check_results['error'])}")

    # 步骤2: 提交到可用的
    if not args.check_only and check_results["can_submit"]:
        submit_results = await batch_submit(check_results["can_submit"], data)

        success = sum(1 for r in submit_results if r["status"] == "success")
        print(f"\n[SUBMIT RESULT] {success}/{len(submit_results)} submitted successfully")

        # 保存结果
        output = {
            "site": args.site,
            "check_results": check_results,
            "submit_results": submit_results,
            "timestamp": datetime.now().isoformat()
        }
    else:
        output = {
            "check_results": check_results,
            "timestamp": datetime.now().isoformat()
        }

    # 保存
    fname = f"batch_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n[SAVED] Results to {fname}")


if __name__ == "__main__":
    asyncio.run(main())