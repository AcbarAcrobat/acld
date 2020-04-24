from page.base_page import BasePage
from wasd.wd import Element as E


class MyNotebooks(BasePage):

    URL = "/"

    create_button = E("#add-nb")
    notebook_row = E(".mat-row")
    connect_button = E(".mat-button")

    def create_notebook(self, name):
        b = self.browser