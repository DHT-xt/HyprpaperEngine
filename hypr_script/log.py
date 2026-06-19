from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton

class info_log(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hyprpaper Engine")
        self.resize(300, 200)

    # 🔴 
    def erro_msg(self, mensagem):
        QMessageBox.critical(
            self, 
            "Error", #Title
            f"Critical error:\n\n{mensagem}" #msg
        )

    # 🟡
    def aviso(self, mensagem):
        QMessageBox.warning(
            self, 
            "warning", 
            mensagem
        )

    # 🔵
    def sucesso(self, mensagem):
        QMessageBox.information(
            self, 
            "Sucess", 
            mensagem
        )
