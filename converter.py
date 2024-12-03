import json
import re
import argparse

# Функция для проверки имени (имя должно состоять из букв и цифр, начинаться с буквы или цифры)
def is_valid_name(name):
    # Имя не должно начинаться с цифры, но может содержать цифры
    return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name))

# Функция для преобразования значения в конфигурационный формат
def to_config_format(value, constants):
    if isinstance(value, dict):
        return to_dict_format(value, constants)
    elif isinstance(value, list):
        return to_array_format(value, constants)
    elif isinstance(value, str):
        # Проверяем на наличие переменной для вычисления константы
        if value.startswith('$') and value[1:] in constants:
            return constants[value[1:]]
        else:
            return value
    else:
        return str(value)

# Функция для преобразования массива в конфигурационный формат
def to_array_format(arr, constants):
    return f"({', '.join(to_config_format(item, constants) for item in arr)})"

# Функция для преобразования словаря в конфигурационный формат
def to_dict_format(dct, constants):
    return f"[\n" + "\n".join(f"  {key} => {to_config_format(value, constants)}," for key, value in dct.items()) + "\n]"

# Основная функция преобразования JSON в конфигурационный формат
def json_to_config(json_data):
    constants = {}

    def process_item(key, value):
        if isinstance(value, dict):
            result = to_dict_format(value, constants)
        elif isinstance(value, list):
            result = to_array_format(value, constants)
        else:
            result = to_config_format(value, constants)

        # Если ключ невалиден, но число, добавляем его как строку
        if is_valid_name(key):
            return f"{key} is {result};"
        else:
            return f"{key} is {result};"

    output = []

    if isinstance(json_data, dict):
        for key, value in json_data.items():
            item = process_item(key, value)
            output.append(item)

    return "\n".join(output)

# Функция для чтения JSON файла
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Функция для записи конфигурационного текста в файл
def write_config_file(file_path, config_data):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(config_data)

# Функция для обработки командной строки
def main():
    parser = argparse.ArgumentParser(description="Преобразование JSON в конфигурационный формат.")
    parser.add_argument('input_file', type=str, help="Путь к входному JSON файлу")
    parser.add_argument('output_file', type=str, help="Путь к выходному файлу конфигурации")

    args = parser.parse_args()

    try:
        json_data = read_json_file(args.input_file)
        config_data = json_to_config(json_data)
        write_config_file(args.output_file, config_data)
        print(f"Конфигурация успешно записана в {args.output_file}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
