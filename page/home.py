from page.base_page import BasePage
from wasd.wd import Element as E


class HomePage(BasePage):

    URL = "/"

    login_form      = E(".login-form__content")
    username_field  = E('#username', login_form)
    password_field  = E("#password", login_form)
    login_button    = E("#kc-login", login_form)

    def login(self, username, password):
        b = self.browser
        b.fill_field(self.username_field, username)
        b.fill_field(self.password_field, password)
        b.click(self.login_button)

    def validate(self):
        b = self.browser
        b.wait_for_element_visible(self.login_form, 5)
