from wasd.util import Locator
from page.base_page import BasePage
from wasd.wd import Element as E, ShadowElement
import re


class JupyterPage(BasePage):

    URL = "/"
    main_page = ShadowElement('main-page')
    app_drawer_layout = ShadowElement('app-drawer-layout', main_page)
    iframe_container = ShadowElement('iframe-container', main_page)
    iframe = E("#iframe", iframe_container)
    UPLOAD_BUTTON = E("input.fileinput")
    CONFIRM_UPLOAD_FILE = E("button.upload_button")
    jupiter_trash = E(".fa-trash")
    modal_dialog = E('.modal-dialog')
    submit_delete_file = E(".btn-danger", modal_dialog)

    def upload_to_nfs(self):
        b = self.browser
        with b.in_frame(self.iframe):
            b.attach_file(self.UPLOAD_BUTTON, "test_file.ipynb")
            b.wait_for_element_visible(self.CONFIRM_UPLOAD_FILE)
            b.js_click(self.CONFIRM_UPLOAD_FILE)
            self.wait_upload_file("test_file.ipynb")

    def wait_upload_file(self, elm_name):
        b = self.browser
        with b.in_frame(self.iframe):
            elm = E(Locator.contains(".list_item", elm_name))
            b.wait_for_element_visible(elm, 15)

    def delete_nfs_file(self):
        b = self.browser
        with b.in_frame(self.iframe):
            item = E(Locator.contains('.list_item', 'test_file.ipynb'))
            b.js_click(item)
            b.js_click(self.jupiter_trash)
            b.wait_for_element_visible(self.modal_dialog)
            b.js_click(self.submit_delete_file)

    def start_job(self):
        b = self.browser
        with b.in_frame(self.iframe):
            job = E(Locator.contains(".item_link", "test_file.ipynb"))
            b.js_click(job)
            b.sleep(5)
            b.switch_to_window()
            b.js_click(E("#run_all_cells"))
            b.wait_for_element_visible(E(Locator.contains(".output_wrapper", "Out[14]")), 20)
            a = b.grab_text_from(E(Locator.element_at(".cell .output_result", -1)))
            v = self.parse_regexp(a)
            return v

    def parse_regexp(self, text):
        r = re.search('"(.+)"', text)
        return r.group(1)
