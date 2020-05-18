import pytest
from truth.truth import AssertThat
from page.my_notebooks import MyNotebooks

from page.jupyter import JupyterPage
from page.my_tasks import MyTasks


class TestNotebooks:

    @pytest.mark.want_to('Create Notebook')
    def test_create_notebook(self, browser, faker):
        notebooks = MyNotebooks(browser)
        jupyter = JupyterPage(browser)
        tasks = MyTasks(browser)
        notebooks.navigate()
        count_before = notebooks.table_count()
        notebooks.create_notebook()
        notebook_name = faker.lexify('??????').lower()
        notebooks.fill_name(name=notebook_name)
        notebooks.select_type()
        notebooks.submit_create()
        notebooks.finish_init()
        count_after = notebooks.table_count()
        AssertThat(count_after).IsEqualTo(count_before + 1)
        notebooks.validate_created_notebook(notebook_name)
        notebooks.connect_to_notebook(notebook_name, timeout=20)
        jupyter.upload_to_nfs()
        p = jupyter.start_job()
        tasks.check_job_in_list()
        tasks.wait_with_refresh(p)
        notebooks.navigate()
        notebooks.connect_to_notebook(notebook_name, timeout=1)
        jupyter.delete_nfs_file()
        notebooks.navigate()
        notebooks.del_notebook(notebook_name)
        AssertThat(count_before).IsEqualTo(notebooks.table_count())
