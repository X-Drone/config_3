import unittest
from unittest.mock import patch, mock_open
import json
from converter import *


class TestConfigFunctions(unittest.TestCase):

    def test_is_valid_name(self):
        self.assertTrue(is_valid_name("valid_name1"))
        self.assertTrue(is_valid_name("validName"))
        self.assertFalse(is_valid_name("1invalid_name"))
        self.assertFalse(is_valid_name("invalid-name"))
        self.assertTrue(is_valid_name("_validName"))
        self.assertFalse(is_valid_name("invalid name"))

    def test_to_config_format(self):
        constants = {"MY_CONST": "constant_value"}

        # Строки
        self.assertEqual(to_config_format("simple_string", constants), "simple_string")
        self.assertEqual(to_config_format("$MY_CONST", constants), "constant_value")

        # Числа
        self.assertEqual(to_config_format(123, constants), "123")

        # Списки
        self.assertEqual(to_config_format([1, 2, 3], constants), "(1, 2, 3)")

        # Словари
        self.assertEqual(to_config_format({"key1": "value1", "key2": "value2"}, constants),
                         "[\n  key1 => value1,\n  key2 => value2,\n]")

    def test_to_array_format(self):
        constants = {"MY_CONST": "constant_value"}

        # Проверка массивов
        self.assertEqual(to_array_format([1, "$MY_CONST", 3], constants), "(1, constant_value, 3)")
        self.assertEqual(to_array_format([{"a": 1}, {"b": 2}], constants),
                         "([\n  a => 1,\n], [\n  b => 2,\n])")

    def test_to_dict_format(self):
        constants = {"MY_CONST": "constant_value"}

        # Проверка вложенных словарей
        self.assertEqual(to_dict_format({"key1": "value1", "key2": {"nested_key": "$MY_CONST"}}, constants),
                         "[\n  key1 => value1,\n  key2 => [\n  nested_key => constant_value,\n],\n]")

    @patch("builtins.open", mock_open(read_data=json.dumps({"key1": "value1", "key2": [1, 2, 3]})))
    def test_json_to_config(self):
        # Проверка преобразования JSON в конфигурацию
        input_data = '{"key1": "value1", "key2": [1, 2, 3]}'
        expected_output = "key1 is value1;\nkey2 is (1, 2, 3);"

        json_data = read_json_file("fake_path")
        config_data = json_to_config(json_data)

        self.assertEqual(config_data, expected_output)

    @patch("builtins.open", mock_open())
    def test_write_config_file(self):
        config_data = "key1 is value1;\nkey2 is (1, 2, 3);"

        with patch("builtins.open", mock_open()) as mocked_file:
            write_config_file("fake_output_path", config_data)
            mocked_file.assert_called_once_with("fake_output_path", 'w', encoding='utf-8')
            mocked_file().write.assert_called_once_with(config_data)


if __name__ == '__main__':
    unittest.main()
