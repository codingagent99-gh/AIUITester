from playwright.sync_api import sync_playwright

class BrowserController:

    def __init__(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def goto(self, url):
        self.page.goto(url)

    def click(self, text):
        self.page.get_by_text(text).click()

    def type(self, placeholder, value):
        self.page.get_by_placeholder(placeholder).fill(value)

    def exists(self, text):
        return self.page.get_by_text(text).is_visible()

    def close(self):
        self.browser.close()
        self.p.stop()
