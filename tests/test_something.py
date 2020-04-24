import pytest


class TestSomething:

    @pytest.mark.want_to('Test bla bla feature')
    def test_feature1(self, browser):
        browser.sleep(5)
