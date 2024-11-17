**Chương trình kiểm thử API sử dụng pytest**
  data: Thư mục chứa dữ liệu của dự án gồm:
    config.json: File cấu hình cho dự án, chứa các thông tin như URL API, thông tin xác thực cho kiểm thử.
    test_cases.csv: File chứa các test case cho API, bao gồm thông tin về đầu vào, đầu ra mong đợi và các điều kiện để chạy test, như đã mô tả trước đó.
  reports: Thư mục chứa các báo cáo và biểu đồ liên quan đến kết quả kiểm thử.
  assets: Thư mục con chứa file style.css là tệp định dạng CSS dùng để tạo style cho báo cáo.
    actual_status_bar_chart.png và pass_fail_pie_chart.png: Biểu đồ trạng thái và biểu đồ tròn để mô hình hoá kết quả thành công/thất bại của các test case.
    test_report.html, test_report.xml: Báo cáo kiểm thử ở định dạng HTML và XML.
    test_results.xlsx: Báo cáo kết quả kiểm thử dưới dạng bảng tính Excel.
  scripts: Thư mục chứa các file script hỗ trợ cho quy trình kiểm thử.
    cleanup.py: Script dùng để dọn dẹp dữ liệu, các báo cáo cũ trước khi kiểm thử.
    generate_reports.py: Script để tạo báo cáo kiểm thử.
    run_tests.py: Script để chạy các bài kiểm thử.
  tests: Thư mục chứa các file kiểm thử chính.
    test_api.py: File kiểm thử cho các API của dự án.
    test_test_untils.py và test_untils.py: Các file chứa các kiểm thử và tiện ích hỗ trợ cho việc kiểm thử.
  main.py: File chính là điểm khởi đầu của chương trình.
**Chạy chương trình bằng cách nhập lệnh "python main.py" vào terminal**
