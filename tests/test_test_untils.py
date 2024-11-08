# tests/test_test_utils.py
import pytest
from tests.test_untils import load_config, parse_json_string, compare_response

# Kiểm thử cho hàm load_config
def test_load_config():
    # Kiểm thử với file tồn tại
    config = load_config('data/config.json')  # Đảm bảo có file config.json mẫu
    assert isinstance(config, dict), "Config phải là một từ điển."

    # Kiểm thử với file không tồn tại
    config = load_config('data/non_existent_config.json')
    assert config == {}, "Khi file không tồn tại, kết quả phải là {}."

# Kiểm thử cho hàm parse_json_string
def test_parse_json_string():
    # Kiểm thử với chuỗi JSON hợp lệ
    json_string = '{"key": "value"}'
    result = parse_json_string(json_string)
    assert result == {"key": "value"}, "Chuỗi JSON hợp lệ phải được giải mã đúng."

    # Kiểm thử với chuỗi JSON không hợp lệ
    json_string = '{"key": "value"'
    result = parse_json_string(json_string)
    assert result == {}, "Chuỗi JSON không hợp lệ phải trả về {}."

    # Kiểm thử với chuỗi rỗng
    json_string = ''
    result = parse_json_string(json_string)
    assert result == {}, "Chuỗi rỗng phải trả về {}."

# Kiểm thử cho hàm compare_response
def test_compare_response(capsys):
    # Kiểm thử khi `expected_body` khớp `actual_body`
    expected_body = {"key1": "value1", "key2": "value2"}
    actual_body = {"key1": "value1", "key2": "value2"}
    compare_response(expected_body, actual_body)

    captured = capsys.readouterr()
    assert "key1: khớp giá trị (value1)" in captured.out
    assert "key2: khớp giá trị (value2)" in captured.out

    # Kiểm thử khi `expected_body` không khớp `actual_body`
    expected_body = {"key1": "value1", "key2": "value2"}
    actual_body = {"key1": "value1", "key2": "different_value"}
    compare_response(expected_body, actual_body)

    captured = capsys.readouterr()
    assert "Lỗi: key2 - Mong đợi: value2, Thực tế: different_value" in captured.out
