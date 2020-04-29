import pytest
from page.my_notebook import MyNotebooks
from truth.truth import AssertThat


class TestCreateNotebook:

    @pytest.mark.want_to('Create Notebook')
    def test_create_notebook(self, browser, faker):
        page = MyNotebooks(browser)
        page.navigate()
        tr = page.table_count()
        page.create_notebook()
        notebook_name = faker.lexify('??????')
        page.fill_name(name = notebook_name)
        page.submit_button()
        page.finish_init()
        ftr = page.table_count()
        AssertThat(ftr).IsEqualTo(tr + 1)
        page.validate_created_notebook(notebook_name)
