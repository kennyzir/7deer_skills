#!/usr/bin/env python3
"""
Directory Detection Script
检测目录是否接受免费提交
"""

import asyncio
import aiohttp
import re
import sys
from typing import Dict, Optional

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


async def check_directory(url: str, timeout: int = 10) -> Dict:
    """检测目录是否可提交"""
    result = {
        "url": url,
        "can_submit": False,
        "status": "unknown",
        "has_form": False,
        "is_paid": False,
        "needs_login": False,
        "needs_backlink": False,
        "error": None
    }
    
    headers = {"User-Agent": USER_AGENT}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=timeout, ssl=False) as resp:
                result["status"] = resp.status
                html = await resp.text()
                
                # 检测表单
                if '<form' in html.lower():
                    result["has_form"] = True
                
                # 检测付费 (常见关键词)
                paid_patterns = [
                    r'\$\d+',  # $29, $99
                    r'payment',
                    r'paid.*submission',
                    r'submission.*fee',
                    r'premium',
                    r'pro.*submission',
                ]
                for pattern in paid_patterns:
                    if re.search(pattern, html, re.IGNORECASE):
                        result["is_paid"] = True
                        break
                
                # 检测需要登录
                login_patterns = [
                    r'login.*required',
                    r'signin.*required',
                    r'must.*login',
                    r'register.*first',
                ]
                for pattern in login_patterns:
                    if re.search(pattern, html, re.IGNORECASE):
                        result["needs_login"] = True
                        break
                
                # 检测需要反向链接
                backlink_patterns = [
                    r'backlink.*required',
                    r'reciprocal.*link',
                    r'link.*back.*required',
                ]
                for pattern in backlink_patterns:
                    if re.search(pattern, html, re.IGNORECASE):
                        result["needs_backlink"] = True
                        break
                
                # 综合判断
                result["can_submit"] = (
                    result["has_form"] and 
                    not result["is_paid"] and 
                    not result["needs_login"] and
                    not result["needs_backlink"]
                )
                
    except asyncio.TimeoutError:
        result["error"] = "timeout"
    except aiohttp.ClientError as e:
        result["error"] = str(e)
    except Exception as e:
        result["error"] = str(e)
    
    return result


async def main():
    if len(sys.argv) < 2:
        # 从stdin读取URL列表
        urls = [line.strip() for line in sys.stdin if line.strip()]
    else:
        urls = sys.argv[1:]
    
    tasks = [check_directory(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    for r in results:
        status = "✅" if r["can_submit"] else "❌"
        reason = []
        if r["is_paid"]: reason.append("paid")
        if r["needs_login"]: reason.append("login")
        if r["needs_backlink"]: reason.append("backlink")
        if r["error"]: reason.append(f"error:{r['error']}")
        
        print(f"{status} {r['url']}")
        if reason:
            print(f"   Reason: {', '.join(reason)}")


if __name__ == "__main__":
    asyncio.run(main())