from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton

class info_log(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hyprpaper Engine")
        self.resize(300, 200)

    # 🔴 Para ERROS GRAVES 
    def erro_msg(self, mensagem):
        QMessageBox.critical(
            self, 
            "Error", # Título da Janela
            f"Critical error:\n\n{mensagem}" # Corpo do texto
        )

    # 🟡 Para AVISOS 
    def aviso(self, mensagem):
        QMessageBox.warning(
            self, 
            "Atenção", 
            mensagem
        )

    # 🔵 Para INFORMAÇÕES 
    def sucesso(self, mensagem):
        QMessageBox.information(
            self, 
            "Concluído", 
            mensagem
        )
