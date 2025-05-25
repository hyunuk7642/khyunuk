import sys
import time
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, 
                            QPushButton, QTextBrowser, QMessageBox, QTableWidget, 
                            QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class GoogleNewsSearcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("구글 뉴스 검색기")
        self.setGeometry(200, 200, 1000, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("검색어를 입력하세요...")

        self.search_button = QPushButton("뉴스 검색")
        self.search_button.clicked.connect(self.search_news)

        # 테이블 위젯 생성
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["순번", "제목", "URL", "내용 불러오기"])
        self.result_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.result_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.result_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.result_table.setStyleSheet("""
            QTableWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                gridline-color: #dee2e6;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 5px;
                border: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)

        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_table)

        self.setLayout(layout)

    def search_news(self):
        print("검색 시작")
        keyword = self.search_input.text().strip()
        if not keyword:
            QMessageBox.warning(self, "입력 오류", "검색어를 입력해주세요.")
            return

        # 브라우저 설정
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        try:
            search_url = f"https://www.google.com/search?q={keyword}&tbm=nws"
            driver.get(search_url)
            
            wait = WebDriverWait(driver, 10)
            news_items = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.dbsr, div.SoaBEf"))
            )

            self.result_table.setRowCount(0)  # 테이블 초기화

            if not news_items:
                QMessageBox.information(self, "알림", "검색 결과가 없습니다.")
                return

            for idx, item in enumerate(news_items[:10], 1):
                try:
                    title = item.find_element(By.CSS_SELECTOR, "div.n0jPhd").text
                    link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    
                    # 새 행 추가
                    row_position = self.result_table.rowCount()
                    self.result_table.insertRow(row_position)
                    
                    # 순번
                    self.result_table.setItem(row_position, 0, QTableWidgetItem(str(idx)))
                    
                    # 제목
                    title_item = QTableWidgetItem(title)
                    title_item.setData(Qt.UserRole, link)  # 링크 저장
                    self.result_table.setItem(row_position, 1, title_item)
                    
                    # URL
                    url_item = QTableWidgetItem(link)
                    self.result_table.setItem(row_position, 2, url_item)
                    
                    # 내용 불러오기 버튼
                    load_button = QPushButton("내용 불러오기")
                    load_button.clicked.connect(lambda checked, row=row_position: self.load_content(row))
                    self.result_table.setCellWidget(row_position, 3, load_button)
                    
                except Exception as e:
                    print(f"항목 처리 중 오류: {str(e)}")
                    continue

        except Exception as e:
            QMessageBox.critical(self, "오류", f"검색 중 오류 발생:\n{str(e)}")
        finally:
            driver.quit()

    def load_content(self, row):
        try:
            url = self.result_table.item(row, 2).text()
            QDesktopServices.openUrl(QUrl(url))
        except Exception as e:
            QMessageBox.critical(self, "오류", f"내용을 불러오는 중 오류 발생:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoogleNewsSearcher()
    window.show()
    sys.exit(app.exec_())
