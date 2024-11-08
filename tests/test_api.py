import csv
import requests
import json
import pandas as pd
import pytest

# Danh sách toàn cục để lưu kết quả các test case
results = []

# Hàm đăng nhập để lấy token
def get_login_token():
    url = "https://admin.ubo.anvita.com.vn/api/v1/account/user/login"  # URL cho API đăng nhập
    headers = {"Content-Type": "application/json"}
    payload = {"username": "admin", "password": "admin"}  # Thông tin đăng nhập

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        token = data.get("token")
        if token:
            print(f"Token nhận được: {token}")
            return token
        else:
            print("Không có token trong phản hồi.")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi đăng nhập để lấy token: {e}")
        return None

# Hàm để load test case từ file CSV
def load_test_cases(test_cases_file):
    with open(test_cases_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        test_cases = list(reader)
    return test_cases

# Hàm kiểm thử với pytest
@pytest.mark.parametrize("test_case", load_test_cases("data/test_cases.csv"))
def test_api_case(test_case):
    token = get_login_token()  # Lấy token từ API đăng nhập
    assert token, "Không lấy được token, dừng quá trình kiểm thử."

    url = test_case['URL']
    
    # Parse headers và thêm Authorization từ cột `Authorization`
    try:
        headers = json.loads(test_case['Headers']) if test_case['Headers'] else {}
        headers["Authorization"] = test_case['Authorization'].replace("Bearer your_token_here", f"{token}")
    except json.JSONDecodeError:
        pytest.fail(f"Lỗi giải mã JSON trong Headers: {test_case['Headers']}")

    # Parse body của yêu cầu
    try:
        payload = json.loads(test_case['Body']) if 'Body' in test_case and test_case['Body'] else {}
    except json.JSONDecodeError:
        pytest.fail(f"Lỗi giải mã JSON trong Body: {test_case.get('Body', '')}")

    # Phương thức HTTP
    method = test_case['Method'].strip().upper()
    assert method in ['GET', 'POST', 'PUT', 'DELETE'], f"Phương thức HTTP '{method}' không hợp lệ"

    # Mã trạng thái mong đợi
    expected_status = int(test_case['Expected Status Code'])
    expected_result = test_case.get('Expected Response', '')

    # Gửi yêu cầu HTTP
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=payload)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, json=payload)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers, json=payload)

    # Kiểm tra kết quả
    actual_status = response.status_code
    actual_body = response.json() if response.headers.get("Content-Type") == "application/json" else response.text

    # So sánh kết quả và lưu vào danh sách
    pass_fail = "Pass" if actual_status == expected_status and str(actual_body) == expected_result else "Fail"
    results.append({
        "Test Case ID": test_case['Test Case ID'],
        "Expected Status": expected_status,
        "Expected Result": expected_result,
        "Actual Status": actual_status,
        "Actual Result": actual_body,
        "Result": pass_fail
    })

# Hàm ghi kết quả vào file Excel
def update_results_excel(results_file_path):
    df = pd.DataFrame(results)
    df.to_excel(results_file_path, index=False, engine='openpyxl')
    print(f"Kết quả đã được ghi vào {results_file_path}")

# Hàm pytest fixture để lưu kết quả sau khi toàn bộ kiểm thử hoàn tất
@pytest.fixture(scope="session", autouse=True)
def write_results_to_excel():
    yield  # Đợi cho đến khi tất cả kiểm thử hoàn thành
    update_results_excel("reports/test_results.xlsx")  # Ghi kết quả vào file Excel

# Hàm pytest fixture để lưu kết quả sau khi toàn bộ kiểm thử hoàn tất
@pytest.fixture(scope="session", autouse=True)
def write_results_to_excel():
    yield  # Đợi cho đến khi tất cả kiểm thử hoàn thành
    update_results_excel("reports/test_results.xlsx")  # Ghi kết quả vào file Excel

