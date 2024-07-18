from utils.text_tools import clean


def test_create_get_task_integration():

    assert clean(["test", "abcd"]) == "test\nabcd"
