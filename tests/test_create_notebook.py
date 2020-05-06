import pytest
from truth.truth import AssertThat
from page.my_notebook import MyNotebooks


class AiCloudTests:

    @pytest.mark.want_to('Create Notebook')
    def test_create_notebook(self, browser, faker):
        page = MyNotebooks(browser)
        page.navigate()
        tr = page.table_count()
        page.create_notebook()
        notebook_name = faker.lexify('??????').lower()
        page.fill_name(name = notebook_name)
        page.select_type()
        page.submit_create()
        page.finish_init()
        ftr = page.table_count()
        AssertThat(ftr).IsEqualTo(tr + 1)
        page.validate_created_notebook(notebook_name)
