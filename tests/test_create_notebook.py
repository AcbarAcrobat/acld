import pytest
from truth.truth import AssertThat
from page.my_notebook import MyNotebooks


class TestNotebooks:

    @pytest.mark.want_to('Create Notebook')
    def test_create_notebook(self, browser, faker):
        page = MyNotebooks(browser)
        page.navigate()
        count_before = page.table_count()
        page.create_notebook()
        notebook_name = faker.lexify('??????').lower()
        page.fill_name(name=notebook_name)
        page.select_type()
        page.submit_create()
        page.finish_init()
        count_after = page.table_count()
        AssertThat(count_after).IsEqualTo(count_before + 1)
        page.validate_created_notebook(notebook_name)
        page.connect_to_notebook(notebook_name, timeout=20)
        page.upload_to_nfs()
        p = page.start_job()
        page.check_job_in_list()
        page.wait_with_refresh(p)
        page.navigate()
        page.switch_to_iframe()
        page.connect_to_notebook(notebook_name, timeout=1)
        page.delete_nfs_file()
        page.navigate()
        page.switch_to_iframe()
        page.del_notebook(notebook_name)
        AssertThat(count_before).IsEqualTo(page.table_count())
