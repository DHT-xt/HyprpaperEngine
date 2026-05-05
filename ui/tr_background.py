from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout

#app = QApplication([])
#window = QMainWindow()


def configurar_transparencia(janela_alvo):
    """
    Esta função transforma qualquer QMainWindow em uma janela 
    transparente com bordas arredondadas.
    """
    # 1. Aplica as Flags e Atributos
    janela_alvo.setAttribute(Qt.WA_TranslucentBackground)
    janela_alvo.setWindowFlags(Qt.FramelessWindowHint)

    # 2. Criamos o container central que você precisará para o CSS
    container = QWidget()
    janela_alvo.setCentralWidget(container)
    
    # Armazenamos o container na janela para facilitar o acesso depois
    janela_alvo.corpo = container 
    
    # Criamos um layout padrão para o corpo
    janela_alvo.layout_principal = QVBoxLayout(container)

    # 3. Aplicamos o estilo
    janela_alvo.corpo.setStyleSheet(f"""
        QWidget {{
            background-color: rgba(16, 16, 16, 230); 
            border-radius: 15px;
            border: 1px solid #333;
        }}
    """)

#configurar_transparencia(window)


#window.resize(400, 300)
#window.show()
#app.exec()
