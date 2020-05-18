from selenium.common.exceptions import TimeoutException
from wasd.util import Locator
from page.base_page import BasePage
from wasd.wd import Element as E, ShadowElement


class MyTasks(BasePage):

    URL = '/'
    main_page = ShadowElement('main-page')
    app_drawer_layout = ShadowElement('app-drawer-layout', main_page)
    iframe_container = ShadowElement('iframe-container', main_page)
    iframe = E("#iframe", iframe_container)
    job_table = E("table#mon-table")

    def check_job_in_list(self):
        b = self.browser
        b.open("_/monitoring/")
        b.switch_to_iframe(self.iframe)

    def wait_with_refresh(self, text, attempts=20, timeout=10):
        b = self.browser
        row = E(Locator.contains("[role='row']", text), self.job_table)

        for i in range(attempts):
            try:
                b.wd_wait(timeout).until(
                    lambda wd: len(b.grab_visible(row)) > 0
                )
                return row
            except TimeoutException:
                b.refresh()
                b.switch_to_iframe(self.iframe)
                b.sleep(1)
                continue

        raise TimeoutException(
            f"Waited for {attempts} attempts ({timeout} seconds each) "
            f"but text `{text}` still not found")
