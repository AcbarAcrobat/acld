from wasd.util import Locator
from page.base_page import BasePage
from wasd.wd import Element as E, ShadowElement


class S3(BasePage):

    URL = "/"
    main_page = ShadowElement('main-page')
    app_drawer_layout = ShadowElement('app-drawer-layout', main_page)
    iframe_container = ShadowElement('iframe-container', main_page)
    iframe = E("#iframe", iframe_container)

    def upload_to_s3(self):
        pass

    def submit_upload(self):
        pass
