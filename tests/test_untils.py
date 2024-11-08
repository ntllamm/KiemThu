import json

def load_config(file_path='data/config.json'):
    try:
        with open(file_path, 'r') as config_file:
            return json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Lỗi khi đọc file config: {e}")
        return {}

def parse_json_string(json_string):
    if json_string:
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Lỗi khi giải mã JSON: {e}")
            return {}
    return {}

def compare_response(expected_body, actual_body):
    for key, value in expected_body.items():
        actual_value = actual_body.get(key)
        if actual_value != value:
            print(f"Lỗi: {key} - Mong đợi: {value}, Thực tế: {actual_value}")
        else:
            print(f"{key}: khớp giá trị ({value})")
