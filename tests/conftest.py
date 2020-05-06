import pytest
from selenium.webdriver.remote.file_detector import LocalFileDetector
from wasd.wd import Browser, Element as E
from wasd.core import SettingsManager as Conf
from faker import Faker
# Define custom action here
from page.home_page import HomePage


class MyExtendedBrowser(Browser):
    def upload_file(self, input_elm, path_to):
        self._driver_instance.file_detector = LocalFileDetector()
        self.fill_field(input_elm, path_to)

    def upload_to_s3(self):
        pass

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
