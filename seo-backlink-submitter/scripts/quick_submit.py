#!/usr/bin/env python3
"""Quick submit to found directories"""
import asyncio
from playwright.async_api import async_playwright

data = {
    "name": "YourProductName",
    "url": "https://your-product.com",
    "description": "Your product description here",
    "email": "your_email@example.com"
}

# Directories with forms
URLS = [
    "https://submitaitools.org/submit-your-ai-tool/",
    "https://betalist.com/submissions/new",
    "https://www.launchingnext.com/submit/"
]

async def submit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for url in URLS:
            print(f"\n[TRY] {url}")
            page = await browser.new_page()
            try:
                await page.goto(url, timeout=30000)
                await page.wait_for_load_state("networkidle", timeout=15000)

                # Name
                for sel in ['input[name*="name" i]', 'input[id*="name" i]', 'input[placeholder*="name" i]']:
                    el = await page.query_selector(sel)
                    if el and await el.is_visible():
                        await el.fill(data["name"])
                        print(f"  [OK] name")
                        break

                # URL
                for sel in ['input[name*="url" i]', 'input[name*="website" i]', 'input[name*="link" i]']:
                    el = await page.query_selector(sel)
                    if el and await el.is_visible():
                        await el.fill(data["url"])
                        print(f"  [OK] url")
                        break

                # Description
                for sel in ['textarea[name*="desc" i]', 'textarea[id*="desc" i]', 'input[name*="description" i]']:
                    el = await page.query_selector(sel)
                    if el and await el.is_visible():
                        await el.fill(data["description"])
                        print(f"  [OK] description")
                        break

                # Email
                for sel in ['input[type="email"]', 'input[name*="email" i]', 'input[id*="email" i]']:
                    el = await page.query_selector(sel)
                    if el and await el.is_visible():
                        await el.fill(data["email"])
                        print(f"  [OK] email")
                        break

                # Submit button - try more selectors
                for sel in [
                    'button[type="submit"]',
                    'input[type="submit"]',
                    'button:has-text("Submit")',
                    'a:has-text("Submit")',
                    'button:has-text("submit")',
                ]:
                    btn = await page.query_selector(sel)
                    if btn and await btn.is_visible():
                        await btn.click()
                        await asyncio.sleep(3)
                        print(f"  [OK] submitted")
                        break
                else:
                    # Try JS click
                    try:
                        await page.evaluate('document.querySelector("button")?.click()')
                        print(f"  [OK] JS click")
                    except:
                        pass

            except Exception as e:
                print(f"  [ERR] {str(e)[:50]}")
            finally:
                await page.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(submit())