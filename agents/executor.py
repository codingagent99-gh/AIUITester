from browser.playwright_tools import BrowserController

class Executor:

    def __init__(self):
        self.browser = BrowserController()

    def run_step(self, step):
        try:
            if "open" in step:
                url = step.split("open")[-1].strip()
                self.browser.goto(url)

            elif "click" in step:
                text = step.replace("click","").strip()
                self.browser.click(text)

            elif "type" in step:
                parts = step.split("into")
                value = parts[0].replace("type","").strip()
                field = parts[1].strip()
                self.browser.type(field, value)

            return "Passed", None

        except Exception as e:
            return "Failed", str(e)
