import pytest
from wasd.wd import Browser
from wasd.core import SettingsManager as Conf


# Define custom action here
from page.home_page import HomePage


class MyExtendedBrowser(Browser):
    def my_super_fn(self):
        print('Hello, World!')


@pytest.fixture(scope='session')
def _browser(request):
    b = MyExtendedBrowser()
    home_page = HomePage(b)
    home_page.navigate()
    home_page.login(Conf.get("username"), Conf.get("password"))
    yield b
    b.close_driver()
