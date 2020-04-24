import allure
from page.base_page import BasePage
from wasd.wd import Element as E
from support import config as Conf
from wasd.common import log_step


class AcLogin(BasePage):

    URL = "/"

    loader          = E("#kc-login")
    login_form      = E(".login-form__content")
    username_field  = E("#username", login_form)
    password_field  = E("#password", login_form)
    submit_button   = E("#kc-login", login_form)

    def auth(self, username=None, password=None):
        creds = (username or Conf.get('username'), password or Conf.get('password'))
        log_step(f"Авторизуемся под {creds[0]} / {creds[1]}")
        with allure.step(f"Авторизуемся под {creds[0]} / {creds[1]}"):
            B = self.browser
            self.navigate()
            B.fill_field(self.username_field, creds[0])
            B.fill_field(self.password_field, creds[1])
            B.click(self.submit_button)
            B.wait_for_element_visible(E('.bar__actions'), 15) # Ждём бургер
            B.save_session_snapshot(username)


    def validate(self):
        b = self.browser
        b.wait_for_element_not_visible(self.loader, 5)
        b.wait_for_element_visible(self.login_form, 5)
        self.follow_mouse()
