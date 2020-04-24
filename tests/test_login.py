from wasd.common import LOGGER
from datetime import datetime
from page.ac_login import AcLogin


class TestDummy:

    def test_login(self):
        AcLogin.auth()
