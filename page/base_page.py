class BasePage(object):

    URL = "/"

    def __init__(self, browser):
        self.browser = browser


    def navigate(self):
        self.browser.open(self.URL)
        self.validate()
        return self


    def validate(self):
        return self
