from playwright.async_api import async_playwright
import asyncio
from typing import Optional, Dict, Any

class PlaywrightBrowser:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
    
    async def start(self):
        """Start the browser"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        print(f"✅ Browser started (headless={self.headless})")
    
    async def navigate(self, url: str) -> Dict[str, Any]:
        """Navigate to a URL"""
        if not url.startswith('http'):
            url = f'https://{url}'
        
        try:
            print(f"🌐 Navigating to {url}")
            await self.page.goto(url, wait_until='domcontentloaded', timeout=30000)
            return {"status": "success", "url": url}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def click(self, selector: str) -> Dict[str, Any]:
        """Click an element"""
        try:
            print(f"🖱️  Clicking: {selector}")
            await self.page.click(selector, timeout=5000)
            return {"status": "success"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def type_text(self, selector: str, text: str) -> Dict[str, Any]:
        """Type text into an element"""
        try:
            print(f"⌨️  Typing '{text}' into {selector}")
            await self.page.fill(selector, text)
            return {"status": "success"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def extract_text(self, selector: str = "body") -> Dict[str, Any]:
        """Extract text from elements"""
        try:
            print(f"📄 Extracting text from: {selector}")
            elements = await self.page.query_selector_all(selector)
            texts = []
            for element in elements[:10]:  # Limit to first 10
                text = await element.inner_text()
                if text.strip():
                    texts.append(text.strip())
            return {"status": "success", "data": texts}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def extract_links(self) -> Dict[str, Any]:
        """Extract all links from the page"""
        try:
            print(f"🔗 Extracting links")
            links = await self.page.eval_on_selector_all(
                'a[href]',
                '(elements) => elements.map(e => ({text: e.innerText.trim(), href: e.href}))'
            )
            # Filter and limit
            links = [link for link in links if link['text']][:20]
            return {"status": "success", "data": links}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def screenshot(self, path: str = "screenshot.png") -> Dict[str, Any]:
        """Take a screenshot"""
        try:
            await self.page.screenshot(path=path)
            return {"status": "success", "path": path}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def close(self):
        """Close the browser"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("🔒 Browser closed")

# Helper function for sync usage
def run_async(coro):
    """Run async function in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)