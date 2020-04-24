from wasd.util import Locator
from wasd.wd import Element as E
from wasd.common import LOGGER
from hamcrest import *


class Menu(object):

    def __init__(self, browser):
        self.browser = browser
        self.struct = {}
        self.sidebar = E('sc-sidebar')

    def assert_struct(self, expected):
        self.get_struct()
        assert_that(self.struct, equal_to(expected))

    def toggle(self):
        if not self.browser.element_has_attribute(self.sidebar, 'class', '_is-open'):
            self.browser.click(E(".bar__actions"))

    def get_struct(self, cache=True):
        if self.struct and cache is True:
            return self.struct

        self.toggle()

        menu_len = len(self.browser.grab_multiple(E('.menu mat-expansion-panel')))

        for i in range(menu_len):
            e = E(Locator.element_at('.menu mat-expansion-panel', i + 1))
            if not self.browser.element_has_attribute(e, 'class', 'mat-expanded'):
                self.browser.click(e)
            top_lvl = self.browser.grab_text_from(E('mat-panel-title', e)).strip()
            self.struct[top_lvl] = self.browser.grab_multiple(E('.submenu__link', e))

        return self.struct