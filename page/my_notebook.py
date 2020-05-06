from wasd.util import Locator
from page.base_page import BasePage
from wasd.wd import Element as E, ShadowElement
from wasd.core import session

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
    connect_button = E(Locator.contains("button", 'Подключиться'))
    name_field = E("[formcontrolname = 'name']")
    submit_button = E("[type='submit']")
    table = E(".mat-table")
    table_row = E(".mat-row", table)
    f_init = E("[role='gridcell']")
    drop_down_options = E(".mat-select-value")
    select_opt = E(Locator.contains('.mat-option'))
    delete_btn = E(Locator.contains("button", "delete"))
    upload_button_nfs = E("input.fileinput")
    confirm_upload_button = E("button.upload_button")
    loader = E("mat-spinner")

    def t_row(self, notebook_name):
        return E(Locator.contains(".mat-row", notebook_name))

    def switch_to_iframe(self):
        b = self.browser
        b.switch_to_iframe(self.iframe)

    def create_notebook(self):
        b = self.browser
        self.switch_to_iframe()
        b.js_click(self.create_button)

    def fill_name(self, name):
        b = self.browser
        b.fill_field(self.name_field, name)

    def submit_create(self):
        b = self.browser
        b.js_click(self.submit_button)

    def table_count(self):
        b = self.browser
        b.switch_to_iframe()
        self.switch_to_iframe()
        l = len(b.grab_multiple(self.table_row))
        b.switch_to_iframe()
        return l

    def validate_created_notebook(self, notebook_name):
        b = self.browser
        self.switch_to_iframe()
        b.see_element(E(Locator.contains(".mat-cell", notebook_name)))

    def select_type(self):
        b = self.browser
        b.js_click(self.drop_down_options)
        b.js_click(self.select_opt)

    def finish_init(self):
        b = self.browser
        b.wait_for_element_visible(self.f_init, 15)

    def delete_notebook(self, notebook_name):
        b = self.browser
        d = self.t_row(notebook_name)
        b.js_click(self.delete_btn, d)

    def connect_to_notebook(self, notebook_name):
        b = self.browser
        b.wait_for_element_not_visible(self.loader)
        tr = self.t_row(notebook_name)
        b.js_click(E(self.connect_button, tr))

    def upload_to_nfs(self):
        b = self.browser
        self.switch_to_iframe()
        files = session.root_dir.joinpath("files", "test_file.ipynb")
        b.upload_file(str(files))
        b.js_click(self.confirm_upload_button)
        self.wait_upload_file(str(files))

    def wait_upload_file(self, elm_name):
        b = self.browser
        elm = E(Locator.contains(".list_item", elm_name))
        b.wait_for_element_visible(elm, 15)

    def delete_from_nfs(self):
        pass

    def start_job(self):
        pass

    def check_job_in_list(self):
        pass

    def s3_to_nfs(self):
        pass
