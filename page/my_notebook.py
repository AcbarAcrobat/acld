from page.base_page import BasePage
from wasd.wd import Element as E
from wasd.util import Locator


class MyNotebooks(BasePage):
    '''
    Свичнуться в iframe
    Создать ноутбук
    Ввести название
    Убедиться, что ноутбук появился в списке
    Дождаться инициализации
    Подключиться к нотбуку
    '''

    URL = "_/jupyter/"

    create_button = E("#add-nb")
    notebook_row = E(".mat-row")
    connect_button = E(".mat-button")
    name_field = E("[formcontrolname = 'name']")
    submit_button = E("[type='submit']")
    iframe = E("#iframe")
    table = E("app-resource-table table")
    table_row = E(".mat-row", table)
    f_init = E("[role='gridcell']")
    header = E(".header")

    def switch_to_iframe(self):
        b = self.browser
        b.switch_to_iframe(self.iframe)

    def wait_header(self):
        b = self.browser
        b.wait_for_element_visible(self.header, 5)

    def create_notebook(self):
        b = self.browser
        self.wait_header()
        self.switch_to_iframe()
        b.click(self.create_button)
        self.validate_name_field()

    def validate_name_field(self):
        b = self.browser
        self.switch_to_iframe()
        b.wait_for_element_visible(self.name_field, 5)

    def fill_name(self, name):
        b = self.browser
        b.fill_field(self.name_field, name)

    def submit_create(self):
        b = self.browser
        b.click(self.submit_button)

    def table_count(self):
        b = self.browser
        l = len(b.grab_multiple(self.table_row))
        b.switch_to_iframe()
        return l

    def validate_created_notebook(self, notebook_name):
        b = self.browser
        b.see_element(E(Locator.contains(".mat-cell", notebook_name)))

    def finish_init(self):
        b = self.browser
        b.wait_for_element_visible(self.f_init, 15)
