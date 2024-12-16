import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QClipboard, QFont, QColor
from PyQt5.QtCore import QMimeData


def create_text_edit(read_only=False):
    text_edit = QTextEdit(readOnly=read_only)
    text_edit.setStyleSheet(
        "background-color: #ffffff; border: 1px solid #cccccc; padding: 10px; border-radius: 10px;")
    text_edit.setFont(QFont("微软雅黑", 12))
    return text_edit


def get_button_color(text):
    colors = {
        '转换': '#4CAF50',
        '清空': '#FF9800',
        '复制': '#2196F3'
    }
    return colors.get(text, '#4CAF50')


def create_button(text, on_click):
    button = QPushButton(text)
    button.setStyleSheet(
        f"background-color: {get_button_color(text)}; color: #ffffff; border: none; padding: 10px 20px; "
        f"border-radius: 5px;")
    button.setFont(QFont("微软雅黑", 12))
    button.clicked.connect(on_click)
    return button


def validate_input(input_text):
    # 这里可以添加更复杂的输入验证逻辑
    if not input_text:
        return False
    return True


class HeadersConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.copy_button = None
        self.convert_button = None
        self.clear_button = None
        self.output_text_edit = None
        self.input_text_edit = None
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Headers Converter')
        self.setStyleSheet("background-color: #f0f0f0;")

        self.input_text_edit = create_text_edit()
        self.output_text_edit = create_text_edit(read_only=True)

        self.convert_button = create_button('转换', self.convert_headers)
        self.clear_button = create_button('清空', self.clear_input)
        self.copy_button = create_button('复制', self.copy_output)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.copy_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_text_edit)
        main_layout.addWidget(self.output_text_edit)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def convert_headers(self):
        input_text = self.input_text_edit.toPlainText()
        if not input_text:
            output_text = 'headers = {\n'
            output_text += ('"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                            'like Gecko) Chrome/124.0.0.0 Safari/537.36",\n')
            output_text += '}'
            self.output_text_edit.setText(output_text)
        else:
            try:
                lines = input_text.split('\n')
                lines = [line for line in lines if line.strip() != '']
                formatted_headers = {}
                i = 0
                while i < len(lines):
                    line = lines[i]
                    if ':' in line:
                        parts = line.split(':', 1)
                        key = parts[0].strip().lower()
                        if parts[1].strip() != '':
                            value = parts[1].strip()
                            i += 1
                        else:
                            value = lines[i + 1].strip()
                            i += 2
                        formatted_headers[key] = value
                    else:
                        i += 1

                output_text = "headers = {\n"
                for key, value in formatted_headers.items():
                    output_text += f"    '{key}': '{value}',\n"
                output_text += "}"

                self.output_text_edit.setText(output_text)
            except Exception as e:
                QMessageBox.critical(self, '错误', f'转换失败: {str(e)}')

    def clear_input(self):
        self.input_text_edit.clear()
        self.output_text_edit.clear()

    def copy_output(self):
        clipboard = QApplication.clipboard()
        mime_data = QMimeData()
        mime_data.setText(self.output_text_edit.toPlainText())
        clipboard.setMimeData(mime_data)
        QMessageBox.information(self, '提示', '转换的headers已被复制!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HeadersConverter()
    ex.show()
    sys.exit(app.exec_())
