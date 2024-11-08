import os
import pytest
from scripts.cleanup import cleanup_reports
from scripts.run_tests import run_tests
from scripts.generate_reports import generate_statistics_charts

def main():
    print("Bắt đầu quá trình kiểm thử...")


    try:
        # Cleanup old reports
        cleanup_reports()
        print("Dọn dẹp báo cáo cũ thành công.")
    except Exception as e:
        print(f"Lỗi khi dọn dẹp báo cáo: {e}")

    # Run tests with pytest and generate reports
    try:
        # Chạy pytest và tạo báo cáo XML và HTML
        pytest.main(["tests/", "--junitxml=reports/test_report.xml", "--html=reports/test_report.html"])
        print("Kiểm thử API hoàn tất và báo cáo đã được tạo.")
    except Exception as e:
        print(f"Lỗi khi thực hiện kiểm thử hoặc tạo báo cáo: {e}")

    # Generate additional statistics charts
    try:
        generate_statistics_charts("reports/test_results.xlsx")
        print("Biểu đồ thống kê đã được tạo và lưu vào 'reports/test_results.xlsx'.")
    except Exception as e:
        print(f"Lỗi khi tạo biểu đồ thống kê: {e}")

    print("Kiểm thử hoàn tất. Báo cáo và biểu đồ đã được tạo trong thư mục 'reports/'.")

if __name__ == '__main__':
    main()
