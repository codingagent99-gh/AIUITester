def validate(step, browser):
    if "verify" in step:
        text = step.replace("verify","").strip()
        if browser.exists(text):
            return True
        return False
    return True
