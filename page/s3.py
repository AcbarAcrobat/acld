from wasd.util import Locator
from page.base_page import BasePage
from wasd.wd import Element as E, ShadowElement
from wasd.core.settings_manager import SettingsManager

class S3(BasePage):

    URL = "/_/uploadings/"
    main_page = ShadowElement('main-page')
    app_drawer_layout = ShadowElement('app-drawer-layout', main_page)
    iframe_container = ShadowElement('iframe-container', main_page)
    iframe = E("#iframe", iframe_container)
    SETTINGS_FORM = E("[name='settings_form']")
    NAMESPACE = E("[name='namespace']", SETTINGS_FORM)
    BUCKET = E("[name='bucket']", SETTINGS_FORM)
    ACCESSKEY = E("[name='accesskey']", SETTINGS_FORM)
    SECRETKEY = E("[name='secretkey']", SETTINGS_FORM)
    CONFIRM_ADD_BUCKET_btn = E("[type='submit']", SETTINGS_FORM)
    TABLE = E("#s3objects-table")
    TABLE_ROW = E("tbody>tr", TABLE)
    BUCKET_UPLOAD_btn = E("input[type='file']")
    MODAL_CONTENT = E('.modal-content')
    SUBMIT_UPLOAD = E('#upload-btn-upload')
    CLOSE_UPLOAD_FORM_BUTTON = E("#upload-btn-cancel")

    def validate(self):
        b = self.browser
        with b.in_frame(self.iframe):
            b.wait_for_element_visible(self.SETTINGS_FORM, 15)

    def add_bucket(self):
        b = self.browser
        with b.in_frame(self.iframe):
            b.fill_field(self.NAMESPACE, SettingsManager.get("creds")["namespace"])
            b.fill_field(self.BUCKET,    SettingsManager.get("creds")["bucket"])
            b.fill_field(self.ACCESSKEY, SettingsManager.get("creds")["accesskey"])
            b.fill_field(self.SECRETKEY, SettingsManager.get("creds")["secretkey"])
            b.js_click(self.CONFIRM_ADD_BUCKET_btn)

    def s3_row(self, notebook_name):
        return E(Locator.contains(self.TABLE_ROW.val, notebook_name))

    def upload_to_s3(self):
        b = self.browser
        with b.in_frame(self.iframe):
            b.set_style(self.BUCKET_UPLOAD_btn, 'display', 'block')
            b.attach_file(self.BUCKET_UPLOAD_btn, "test_file.ipynb")
            b.wait_for_element_visible(self.SUBMIT_UPLOAD, 10)
            b.js_click(self.SUBMIT_UPLOAD)
            b.wait_for_element_visible(self.CLOSE_UPLOAD_FORM_BUTTON, 10)
            b.js_click(self.CLOSE_UPLOAD_FORM_BUTTON)
            b.wait_for_element_visible(E(Locator.contains(self.TABLE_ROW.val, 'test_file.ipynb')), 15)

    def wait_upload_file(self, elm_name):
        b = self.browser
        with b.in_frame(self.iframe):
            elm = E(Locator.contains(".list_item", elm_name))
            b.wait_for_element_visible(elm, 15)

    def submit_upload(self):
        b = self.browser
        with b.in_frame(self.iframe):
            b.js_click(self.SUBMIT_UPLOAD)

    def move_file_to_nfs(self):
        pass
