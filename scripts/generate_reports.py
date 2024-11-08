import pandas as pd
import matplotlib.pyplot as plt

def generate_statistics_charts(results_file_path):
    # Đọc file Excel chứa kết quả kiểm thử
    df = pd.read_excel(results_file_path)

    # Biểu đồ 1: Tỷ lệ Pass/Fail
    pass_fail_counts = df['Result'].value_counts()
    plt.figure()
    pass_fail_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Tỷ lệ Pass/Fail')
    plt.ylabel('')
    plt.savefig('reports/pass_fail_pie_chart.png')
    print("Đã lưu biểu đồ tỷ lệ Pass/Fail vào reports/pass_fail_pie_chart.png")

    # Biểu đồ 2: Số lượng kiểm thử theo mã trạng thái mong đợi
    status_counts = df['Actual Status'].value_counts()
    plt.figure()
    status_counts.plot(kind='bar')
    plt.title('Số lượng kiểm thử theo mã trạng thái mong đợi')
    plt.xlabel('Mã trạng thái mong đợi')
    plt.ylabel('Số lượng kiểm thử')
    plt.savefig('reports/actual_status_bar_chart.png')
    print("Đã lưu biểu đồ số lượng kiểm thử theo mã trạng thái vào reports/actual_status_bar_chart.png")

    plt.close('all')  # Đóng tất cả các biểu đồ để giải phóng bộ nhớ
