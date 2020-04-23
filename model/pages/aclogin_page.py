import allure
from model.pages.base_page import AcLogin
from wasd.wd import Element as E
from wasd.core import SettingsManager as Conf
from wasd.common import log_step


class HomePage(AcLogin):

    URL = "/"

    loader          = E(".app-loading")
    login_form      = E("#signin-card")
    username_field  = E("[formcontrolname='login']", login_form)
    password_field  = E("[formcontrolname='password']", login_form)
    submit_button   = E("[type='submit']", login_form)


    def auth(self, username=None, password=None):
        creds = (username or Conf.get('username'), password or Conf.get('password'))
        log_step(f"Авторизуемся под {creds[0]} / {creds[1]}")
        with allure.step(f"Авторизуемся под {creds[0]} / {creds[1]}"):
            B = self.browser
            if B.load_session_snapshot("login"):
                return
            self.navigate()
            B.fill_field(self.username_field, creds[0])
            B.fill_field(self.password_field, creds[1])
            B.click(self.submit_button)
            B.wait_for_element_visible(E('.bar__actions'), 5) # Ждём бургер
            B.save_session_snapshot("login")


    def validate(self):
        b = self.browser
        b.wait_for_element_not_visible(self.loader, 5)
        b.wait_for_element_visible(self.login_form, 5)
        self.follow_mouse()
