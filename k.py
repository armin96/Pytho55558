import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt

# استایل‌شیت (QSS) برای ظاهر تیره و مدرن برنامه
STYLESHEET = """
QWidget {
    background-color: #2b2b2b;
    color: #f0f0f0;
    font-family: Segoe UI;
    font-size: 14px;
}
/* استایل برای نوار کناری */
#Sidebar {
    background-color: #3c3c3c;
}
/* استایل دکمه‌ها */
QPushButton {
    background-color: transparent;
    border: none;
    text-align: left;
    padding: 8px;
    border-radius: 5px;
}
QPushButton:hover {
    background-color: #4a4a4a;
}
/* استایل دکمه فعال در نوار کناری */
#ActiveButton {
    background-color: #c00000;
}
#ActiveButton:hover {
    background-color: #a00000;
}
/* استایل دکمه رفرش */
#RefreshButton {
    background-color: #555555;
    text-align: center;
}
#RefreshButton:hover {
    background-color: #6a6a6a;
}
/* استایل کادر جستجو */
QLineEdit {
    background-color: #4a4a4a;
    border: 1px solid #555555;
    border-radius: 5px;
    padding: 5px;
}
/* استایل بخش اصلی */
#MainContent {
    background-color: #242424;
    border-radius: 8px;
}
/* استایل ردیف‌های ارز */
#CurrencyRow {
    background-color: #3c3c3c;
    border-radius: 5px;
}
/* استایل لیبل نرخ */
#RateLabel {
    font-weight: bold;
}
"""


class CurrencyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- تنظیمات اصلی پنجره ---
        self.setWindowTitle("QuickChange")
        self.setGeometry(100, 100, 850, 600)
        self.setStyleSheet(STYLESHEET)

        # --- ویجت اصلی و لایه افقی ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- ساخت نوار کناری و بخش اصلی ---
        self.create_sidebar(main_layout)
        self.create_main_content(main_layout)

    def create_sidebar(self, parent_layout):
        """نوار کناری برنامه را ایجاد می‌کند."""
        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(200)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(15)

        # عنوان برنامه
        title_label = QLabel("QuickChange")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        sidebar_layout.addWidget(title_label)

        # دکمه‌های منو
        exchange_button = QPushButton(" Exchange Rates")
        exchange_button.setObjectName("ActiveButton")  # شناسه برای استایل‌دهی
        sidebar_layout.addWidget(exchange_button)

        sidebar_layout.addWidget(QPushButton(" Converter"))
        sidebar_layout.addWidget(QPushButton(" History"))

        sidebar_layout.addStretch()  # فضای خالی ایجاد می‌کند تا دکمه بعدی به پایین برود
        sidebar_layout.addWidget(QPushButton(" Settings"))

        parent_layout.addWidget(sidebar)

    def create_main_content(self, parent_layout):
        """بخش اصلی محتوا را ایجاد می‌کند."""
        main_content = QWidget()
        main_content.setObjectName("MainContent")

        content_layout = QVBoxLayout(main_content)

        # --- نوار بالا (جستجو و رفرش) ---
        top_bar_layout = QHBoxLayout()
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search currencies...")
        refresh_button = QPushButton("Refresh")
        refresh_button.setObjectName("RefreshButton")

        top_bar_layout.addWidget(search_box)
        top_bar_layout.addWidget(refresh_button)
        content_layout.addLayout(top_bar_layout)

        # --- لیست ارزها (قابل اسکرول) ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")  # حذف حاشیه

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll_area.setWidget(scroll_content)
        content_layout.addWidget(scroll_area)

        # داده‌های نمونه برای نمایش
        currency_data = [
            {"flag": "🇮🇸", "pair": "USD/JPY", "rate": "1.0854", "change": "+0.05%", "is_up": True},
            {"flag": "🇪🇺", "pair": "EUR", "rate": "1.0854", "change": "+0.05%", "is_up": True},
            {"flag": "🇬🇧", "pair": "GBP/JPY", "rate": "1.2789", "change": "+0.02%", "is_up": True},
            {"flag": "🇬🇧", "pair": "GBP/JPY", "rate": "1.2789", "change": "-0.02%", "is_up": False},
            {"flag": "🇯🇵", "pair": "JPY/USD", "rate": "151.87", "change": "-0.02%", "is_up": False},
            {"flag": "🇺🇸", "pair": "USD/JPY", "rate": "151.87", "change": "-0.12%", "is_up": False},
            {"flag": "🇨🇦", "pair": "USD/CAD", "rate": "1.3590", "change": "+0.15%", "is_up": True},
        ]

        for data in currency_data:
            scroll_layout.addWidget(self.create_currency_row(data))

        # یک فاصله در انتهای لیست برای زیبایی بیشتر
        scroll_layout.addStretch()

        parent_layout.addWidget(main_content, stretch=1)

    def create_currency_row(self, data):
        """یک ویجت برای نمایش یک ردیف ارز ایجاد می‌کند."""
        row_widget = QWidget()
        row_widget.setObjectName("CurrencyRow")
        row_layout = QHBoxLayout(row_widget)

        # ویجت‌ها
        flag_pair_label = QLabel(f"{data['flag']}  {data['pair']}")
        rate_label = QLabel(data['rate'])
        rate_label.setObjectName("RateLabel")
        rate_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        change_label = QLabel(f"▲ {data['change'].strip('+-')}" if data["is_up"] else f"▼ {data['change'].strip('+-')}")
        change_label.setStyleSheet("color: green;" if data["is_up"] else "color: red;")
        change_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        # اضافه کردن ویجت‌ها به لایه ردیف
        row_layout.addWidget(flag_pair_label, stretch=2)
        row_layout.addWidget(rate_label, stretch=1)
        row_layout.addWidget(change_label, stretch=1)

        return row_widget


# --- اجرای برنامه ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyApp()
    window.show()
    sys.exit(app.exec())