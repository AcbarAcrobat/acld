import pytest
import allure
from wasd.core import SettingsManager as Conf
from wasd.wd import Browser
from faker import Faker
from wasd.common import log_step
from page.ac_login import AcLogin


class MyExtendedBrowser(Browser):
    def __init__(self):
        super().__init__()


@pytest.fixture(scope='session')
def _browser(request):
    b = MyExtendedBrowser()
    AcLogin(b).auth()
    yield b
    b.close_driver()


@pytest.fixture(scope='class')
def faker():
    return Faker('ru_RU')


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        allure.attach(
            item.screenshot_binary,
            "Screenshot",
            allure.attachment_type.PNG,
        )
