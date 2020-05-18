import pytest
from selenium.webdriver.remote.file_detector import LocalFileDetector
from wasd.wd import Browser
from wasd.core import SettingsManager as Conf
from faker import Faker
# Define custom action here
from page.home import HomePage
from contextlib import contextmanager


class MyExtendedBrowser(Browser):
    def upload_file(self, input_elm, path_to):
        self._driver_instance.file_detector = LocalFileDetector()
        self.fill_field(input_elm, path_to)

    def upload_to_s3(self):
        pass

    def switch_to_window(self):
        windows_after = self._driver_instance.window_handles[1]
        self._driver_instance.switch_to.window(windows_after)

    @contextmanager
    def in_frame(self, frame):
        try:
            self.sleep(0.5)
            self.switch_to_iframe()
            self.switch_to_iframe(frame)
            yield
        finally:
            self.sleep(0.5)
            self.switch_to_iframe()


@pytest.fixture(scope='session')
def faker():
    return Faker('ru_RU')


@pytest.fixture(scope='session')
def _browser(request):
    b = MyExtendedBrowser()
    home_page = HomePage(b)
    home_page.navigate()
    home_page.login(Conf.get("username"), Conf.get("password"))
    yield b
    b.close_driver()
