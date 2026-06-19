from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout

def configurar_transparencia(janela_alvo):
    
    janela_alvo.setAttribute(Qt.WA_TranslucentBackground)
    janela_alvo.setWindowFlags(Qt.FramelessWindowHint)

    container = QWidget()
    janela_alvo.setCentralWidget(container)
    
    
    janela_alvo.corpo = container 
    
    janela_alvo.layout_principal = QVBoxLayout(container)

    # 3. Aplicamos o estilo
    janela_alvo.corpo.setStyleSheet(f"""
        QWidget {{
            background-color: rgba(16, 16, 16, 230); 
            border-radius: 15px;
            border: 1px solid #333;
        }}
    """)
