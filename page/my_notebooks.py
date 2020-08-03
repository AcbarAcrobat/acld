from wasd.util import Locator
from page.base_page import BasePage
from wasd.wd import Element as E, ShadowElement


class MyNotebooks(BasePage):

    URL = "/_/jupyter/"
    main_page = ShadowElement('main-page')
    app_drawer_layout = ShadowElement('app-drawer-layout', main_page)
    iframe_container = ShadowElement('iframe-container', main_page)
    iframe = E("#iframe", iframe_container)
    create_button = E("#add-nb")
    connect_button = E(Locator.contains("button", 'Подключиться'))
    name_field = E("[formcontrolname = 'name']")
    submit_button = E("[type='submit']")
    TABLE = E(".mat-table")
    TABLE_ROW = E(".mat-row", TABLE)
    WAIT_INIT = E("[role='gridcell']")
    NOTEBOOK_OPTIONS = E(".mat-select-value")
    SELECT_OPTIONS = E(Locator.contains('.mat-option'))
    DELETE_BTN = E(Locator.contains("button", "delete"))
    PRELOADER = E("mat-spinner")
    my_job_table = E(".table-bordered")
    job_table = E("table#mon-table")
    jupiter_trash = E(".fa-trash")
    modal_dialog = E('.modal-dialog')
    submit_delete_file = E(".btn-danger", modal_dialog)

    def validate(self):
        b = self.browser
        with b.in_frame(self.iframe):
            b.wait_for_element_visible(self.TABLE)

    def notebook_row(self, notebook_name):
        return E(Locator.contains(self.TABLE_ROW.val, notebook_name))

    def create_notebook(self):
        b = self.browser
        with b.in_frame(self.iframe):
            b.js_click(self.create_button)

    def fill_name(self, name):
        b = self.browser
        with b.in_frame(self.iframe):
            b.sleep(2)
            b.fill_field(self.name_field, name)

    def submit_create(self):
        b = self.browser
        with b.in_frame(self.iframe):
            b.js_click(self.submit_button)

    def table_count(self):
        b = self.browser
        with b.in_frame(self.iframe):
            b.sleep(1)
            l = len(b.grab_multiple(self.TABLE_ROW))
            return l

    def validate_created_notebook(self, notebook_name):
        b = self.browser
        with b.in_frame(self.iframe):
            b.wait_for_element_visible(E(Locator.contains(".mat-cell", notebook_name)), 10)

    def select_type(self):
        b = self.browser
        with b.in_frame(self.iframe):
            b.js_click(self.NOTEBOOK_OPTIONS)
            b.js_click(self.SELECT_OPTIONS)

    def finish_init(self):
        b = self.browser
        with b.in_frame(self.iframe):
            b.wait_for_element_not_visible(self.PRELOADER, 10)

    def connect_to_notebook(self, notebook_name, timeout):
        b = self.browser
        with b.in_frame(self.iframe):
            b.wait_for_element_not_visible(self.PRELOADER)
            tr = self.notebook_row(notebook_name)
            b.sleep(timeout)
            b.js_click(E(self.connect_button, tr))

    def s3_to_nfs(self):
        pass

    def del_notebook(self, name):
        b = self.browser
        with b.in_frame(self.iframe):
            b.js_click(E(self.DELETE_BTN, self.notebook_row(name)))
            b.js_click(E(Locator.contains('button', 'УДАЛИТЬ'), E('app-confirm-dialog')))
            b.wait_for_element_not_visible(self.PRELOADER, 15)
            b.sleep(10)
