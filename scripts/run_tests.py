# scripts/run_tests.py
import pytest

def run_tests():
    """
    Chạy tất cả các bài kiểm thử trong thư mục 'tests' bằng pytest.
    """
    print("Running all test cases in the 'tests' folder...")
    
    # Sử dụng pytest để tự động tìm và chạy tất cả các file kiểm thử trong 'tests'
    pytest.main(["tests/"])

if __name__ == '__main__':
    run_tests()
