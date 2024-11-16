import os
import glob

def cleanup_reports(report_dir='reports'):
    """
    Dọn dẹp các báo cáo cũ trước khi chạy kiểm thử mới.
    Xóa tất cả các file báo cáo có đuôi mở rộng như .json, .xml, .png, .html, .xlsx trong thư mục chỉ định,
    ngoại trừ file template_report.html.
    """
    file_patterns = ['*.json', '*.xml', '*.png', '*.html']
    
    for pattern in file_patterns:
        files = glob.glob(os.path.join(report_dir, pattern))
        for file_path in files:
            # Kiểm tra nếu file không phải là template_report.html
            if os.path.basename(file_path) != 'template_report.html':
                try:
                    os.remove(file_path)
                    print(f"Deleted {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

if __name__ == '__main__':
    cleanup_reports()
