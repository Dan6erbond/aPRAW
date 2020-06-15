from apraw.utils import snake_case_keys
from apraw.utils.snake import camel_to_snake

class TestSnake:
    def test_snake_case_keys(self):
        d = {
            "testKey": 0,
            "TestKeyUpper": 0
        }

        assert "test_key" in snake_case_keys(d)
        assert "test_key_upper" in snake_case_keys(d)

    def test_camel_to_snake(self):
        assert camel_to_snake("TestCamelCase") == "test_camel_case"
