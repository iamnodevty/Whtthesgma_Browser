import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout,
    QWidget, QLabel, QToolBar, QListWidget, QDialog, QHBoxLayout
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QTimer, QUrl
class DevDialog(QDialog):
    def __init__(self):
        self.setWindowTitle("Dev Tools")
        self.setLayout(QVBoxLayout())
        self.ver_label = QLabel("Version 1.0\nVerName: BenchMark\nHTMLVER: com.html.5\n")
class HistoryDialog(QDialog):
    def __init__(self, history, clear_history_callback):
        super().__init__()
        self.setWindowTitle("Browsing History")
        self.setLayout(QVBoxLayout())
        
        self.history_list = QListWidget()
        self.history_list.addItems(history)
        
        self.clear_button = QPushButton("Clear History")
        self.clear_button.clicked.connect(clear_history_callback)

        self.layout().addWidget(self.history_list)
        self.layout().addWidget(self.clear_button)

class SettingsDialog(QDialog):
    def __init__(self, set_theme_callback, quit_callback):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setLayout(QVBoxLayout())

        self.light_button = QPushButton("Light Theme")
        self.light_button.clicked.connect(lambda: set_theme_callback("light"))
        self.dark_button = QPushButton("Dark Theme")
        self.dark_button.clicked.connect(lambda: set_theme_callback("dark"))
        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(quit_callback)
        self.ver_button = QPushButton("Dev Options");
        self.credits_label = QLabel("Made by SN");
        self.layout().addWidget(self.light_button)
        self.layout().addWidget(self.dark_button)
        self.layout().addWidget(self.quit_button)

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize browsing history
        self.history = []

        # Create a central widget for the home page
        self.home_widget = QWidget()
        
        self.home_layout = QVBoxLayout()

        # Adjust spacing and margins
        self.home_layout.setSpacing(5)  # Set the spacing between widgets
        self.home_layout.setContentsMargins(10, 10, 10, 10)  # Set margins (left, top, right, bottom)
        
        self.home_label = QLabel("Whtthesgma Browser")
        self.home_label.setStyleSheet("font-size: 36px; font-weight: bold;")
        
        self.sub_label = QLabel("Made by SN")
        self.sub_label.setStyleSheet("font-size: 18px; color: blue;")
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.navigate_to_url)

        # Add widgets to home layout
        self.home_layout.addWidget(self.home_label, alignment=Qt.AlignCenter)
        self.home_layout.addWidget(self.sub_label, alignment=Qt.AlignCenter)
        self.home_layout.addWidget(self.error_label, alignment=Qt.AlignCenter)
        self.home_layout.addWidget(self.url_bar, alignment=Qt.AlignCenter)
        self.home_layout.addWidget(self.ok_button, alignment=Qt.AlignCenter)

        self.home_widget.setLayout(self.home_layout)

        # Create the browser view
        self.browser = QWebEngineView()

        # Create buttons
        self.back_button = QPushButton("←")
        self.back_button.clicked.connect(self.go_back)

        self.refresh_button = QPushButton("🔄")
        self.refresh_button.clicked.connect(self.refresh_page)

        self.home_button = QPushButton("🏠")
        self.home_button.clicked.connect(self.go_home)

        self.history_button = QPushButton("🕒")
        self.history_button.clicked.connect(self.show_history)

        self.settings_button = QPushButton("⚙️")
        self.settings_button.clicked.connect(self.show_settings)

        # ToolBar for buttons
        toolbar = QToolBar()
        toolbar.addWidget(self.back_button)
        toolbar.addWidget(self.refresh_button)
        toolbar.addWidget(self.home_button)
        toolbar.addWidget(self.history_button)
        toolbar.addWidget(self.settings_button)

        self.addToolBar(toolbar)

        # Set central widget to the home page
        self.setCentralWidget(self.home_widget)
        self.setWindowTitle("Whtthesgma Browser")
        self.resize(1024, 768)  # Set initial size to be larger and resizable
        
        # Default theme
        self.current_theme = "light"
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2E2E2E;
                    color: white;
                }
                QToolBar {
                    background-color: #3E3E3E;
                    border: none;
                }
                QLineEdit {
                    background-color: #4E4E4E;
                    color: white;
                    border: 1px solid #777;
                }
                QPushButton {
                    background-color: #4E4E4E;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #5E5E5E;
                }
            """)
        else:  # light theme
            self.setStyleSheet("""
                QMainWindow {
                    background-color: white;
                    color: black;
                }
                QToolBar {
                    background-color: #f8f8f8;
                    border: none;
                }
                QLineEdit {
                    background-color: white;
                    color: black;
                    border: 1px solid #ccc;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    color: black;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
            """)

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if url:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url
            try:
                self.browser.setUrl(QUrl(url))  # Convert string to QUrl
                self.history.append(url)  # Save to history
                self.setCentralWidget(self.browser)  # Switch to browser view
            except Exception as e:
                self.show_error(f"Error loading page: {str(e)}")
                self.setCentralWidget(self.home_widget)  # Go back to home page
        else:
            self.setCentralWidget(self.home_widget)  # Stay on home if empty

    def refresh_page(self):
        self.browser.reload()

    def go_back(self):
        self.browser.back()

    def go_home(self):
        self.setCentralWidget(self.home_widget)  # Switch back to home page

    def show_history(self):
        history_dialog = HistoryDialog(self.history, self.clear_history)
        history_dialog.exec_()  # Show the history dialog

    def clear_history(self):
        self.history.clear()  # Clear the history list
        self.show_history()  # Refresh the history dialog to show an empty list

    def show_settings(self):
        settings_dialog = SettingsDialog(self.set_theme, self.quit_app)
        settings_dialog.exec_()  # Show the settings dialog

    def set_theme(self, theme):
        self.current_theme = theme
        self.apply_theme(self.current_theme)

    def quit_app(self):
        QApplication.quit()  # Quit the application

    def show_error(self, message):
        self.error_label.setText(message)
        QTimer.singleShot(3000, self.clear_error)  # Clear error after 3 seconds

    def clear_error(self):
        self.error_label.setText("")

app = QApplication(sys.argv)
window = Browser()
window.setStyleSheet("")  # Initial styles
window.show()
sys.exit(app.exec_())
