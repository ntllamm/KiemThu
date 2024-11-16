import csv
import requests
import json
import pandas as pd
import pytest
import matplotlib.pyplot as plt
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

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

@pytest.fixture(scope="session")
def token():
    return get_login_token()

# Hàm kiểm thử với pytest
@pytest.mark.parametrize("test_case", load_test_cases("data/test_cases.csv"))
def test_api_case(test_case, token):
    assert token, "Không lấy được token, dừng quá trình kiểm thử."

    url = test_case['URL']
    
    # Parse headers và thêm Authorization từ cột Authorization
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

      #  Sử dụng try-except cho ghi nhận kết quả, đồng thời cho phép pytest xử lý assert để tạo báo cáo HTML chính xác
    pass_fail = "Pass"
    error_message = ""
    try:
        assert actual_status == expected_status, f"Lỗi: Mã trạng thái thực tế ({actual_status}) không khớp với mong đợi ({expected_status})"
    except AssertionError as e:
        pass_fail = "Fail"
        error_message = str(e)
    # Thêm vào danh sách kết quả để ghi vào Excel
    results.append({
        "Test Case ID": test_case['Test Case ID'],
        "Expected Status": expected_status,
        "Expected Result": expected_result,
        "Actual Status": actual_status,
        "Actual Result": actual_body,
        "Result": pass_fail,
        "Error Message": error_message
    })
     # Dùng pytest.fail để đảm bảo báo cáo HTML ghi nhận các test case fail
    if pass_fail == "Fail":
        pytest.fail(error_message)
@pytest.fixture(scope="session", autouse=True)
def record_start_time():
    global start_time
    start_time = datetime.now()  # Lưu thời gian bắt đầu
    print(f"Thời gian bắt đầu kiểm thử: {start_time}")
# Hàm ghi kết quả vào file Excel với 2 sheet
def update_results_excel(results_file_path):
    # Ghi chi tiết test case vào sheet "Kết quả kiểm thử"
    results_df = pd.DataFrame(results)

    # Tạo dữ liệu cho sheet "Tổng quan"
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["Result"] == "Pass")
    failed_tests = total_tests - passed_tests
    global start_time
    end_time = datetime.now()
    overview_data = {
        "Tổng số Test Case": [total_tests],
        "Số Test Case Pass": [passed_tests],
        "Số Test Case Fail": [failed_tests],
         "Thời gian bắt đầu": [start_time.strftime("%Y-%m-%d %H:%M:%S")],
        "Thời gian kết thúc": [end_time.strftime("%Y-%m-%d %H:%M:%S")]
    }
    overview_df = pd.DataFrame(overview_data)

    # Tạo biểu đồ Pass/Fail
    plt.figure(figsize=(6, 4))
    plt.bar(["Pass", "Fail"], [passed_tests, failed_tests], color=["green", "red"])
    plt.title("Tỷ lệ Pass/Fail")
    plt.ylabel("Số lượng Test Case")
    plt.savefig("reports/pass_fail_chart.png")  # Lưu biểu đồ dưới dạng ảnh

    # Ghi dữ liệu vào Excel với nhiều sheet
    with pd.ExcelWriter(results_file_path, engine="openpyxl") as writer:
        results_df.to_excel(writer, sheet_name="Kết quả kiểm thử", index=False)
        overview_df.to_excel(writer, sheet_name="Tổng quan", index=False)

    # Chèn biểu đồ vào sheet "Tổng quan"
    workbook = load_workbook(results_file_path)
    worksheet = workbook["Tổng quan"]
    img = Image("reports/pass_fail_chart.png")
    worksheet.add_image(img, "B5")  # Chèn biểu đồ tại ô B5
    workbook.save(results_file_path)
    print(f"Kết quả đã được ghi vào file: {results_file_path}")

# Hàm pytest fixture để lưu kết quả sau khi toàn bộ kiểm thử hoàn tất
@pytest.fixture(scope="session", autouse=True)
def write_results_to_excel():
    yield  # Đợi cho đến khi tất cả kiểm thử hoàn thành
    update_results_excel("reports/test_results.xlsx")  # Ghi kết quả vào file Excel