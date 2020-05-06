from wasd.util import Locator
from page.base_page import BasePage
from wasd.wd import Element as E, ShadowElement


class MyNotebooks(BasePage):
    '''
    Свичнуться в iframe
    Создать ноутбук
    Ввести название
    Убедиться, что ноутбук появился в списке
    Дождаться инициализации
    Подключиться к нотбуку
    '''

    URL = "/"
    main_page = ShadowElement('main-page')
    app_drawer_layout = ShadowElement('app-drawer-layout', main_page)
    iframe_container = ShadowElement('iframe-container', main_page)
    iframe = E("#iframe", iframe_container)
    create_button = E("#add-nb")
    notebook_row = E(".mat-row")
    connect_button = E(".mat-button")
    name_field = E("[formcontrolname = 'name']")
    submit_button = E("[type='submit']")
    table = E(".mat-table")
    table_row = E(".mat-row", table)
    f_init = E("[role='gridcell']")
    drop_down_options = E(".mat-select-value")
    select_opt = E(Locator.contains('.mat-option'))

    # def connect_to(self):
    #     b=self.browser
    #     b.find_element("[role='gridcell']")
    #     delete_notebook = E(Locator.contains("tr.td", ))

    def switch_to_iframe(self):
        b = self.browser
        b.switch_to_iframe(self.iframe)

    def create_notebook(self):
        b = self.browser
        b.switch_to_iframe(self.iframe)
        b.js_click(self.create_button)

    def fill_name(self, name):
        b = self.browser
        b.fill_field(self.name_field, name)

    def submit_create(self):
        b = self.browser
        b.js_click(self.submit_button)

    def table_count(self):
        b = self.browser
        self.switch_to_iframe()
        l = len(b.grab_multiple(self.table_row))
        b.switch_to_iframe()
        return l

    def validate_created_notebook(self, notebook_name):
        b = self.browser
        b.see_element(E(Locator.contains(".mat-cell", notebook_name)))

    def select_type(self):
        b = self.browser
        b.js_click(self.drop_down_options)
        b.js_click(self.select_opt)

    def finish_init(self):
        b = self.browser
        b.wait_for_element_visible(self.f_init, 15)
