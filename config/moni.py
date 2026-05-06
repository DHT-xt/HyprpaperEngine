import sys, math
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                               QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QWidget)
from PySide6.QtCore import QSize, Qt
from hypr_script import scrpt_hyprpaper, log
import hypr_script

class PopupSelecaoMonitor(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Estilo do popup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.monitor_selecionado = None

        # Layout Principal do Popup
        layout_principal = QVBoxLayout(self)
        
        titulo = QLabel("Selecione um Monitor:")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo)

        # Layout Horizontal para colocar os "quadrados" dos monitores lado a lado
        layout_monitores = QHBoxLayout()
        layout_principal.addLayout(layout_monitores)

        # Iterando sobre as telas e criando um "quadrado" para cada uma
        self.telas = QApplication.screens()
        for index, tela in enumerate(self.telas):
            geometria = tela.geometry()
            
            # Criamos um botão para agir como o nosso "quadrado" do monitor
            btn_monitor = QPushButton()
            
            # O texto inclui o nome e a resolução
            btn_monitor.setText(f"{tela.name()}\n\n{geometria.width()}x{geometria.height()}")
            
            # Definindo um tamanho fixo (formato de monitor landscape)
            mdc = math.gcd(geometria.width(), geometria.height())
            h_form_btn_monitor = int(geometria.width()/mdc)*10
            v_form_btn_monitor = int(geometria.height()/mdc)*10
            btn_monitor.setFixedSize(h_form_btn_monitor,v_form_btn_monitor)
            
            # Estilizando o botão para parecer um monitor
            btn_monitor.setStyleSheet("""
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    font-weight: bold;
                    border-radius: 5px;
                    border: 2px solid #005a9e;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                    border: 2px solid #003cc8;
                }
            """)
            
            # Conectando o clique. 
            # Usamos o parâmetro default (t=tela) no lambda para garantir 
            # que o botão lembre da tela correta dentro do loop.
            btn_monitor.clicked.connect(lambda checked=False, t=tela: self.ao_selecionar_monitor(t))
            
            layout_monitores.addWidget(btn_monitor)

        # Adiciona um botão de cancelar no fundo
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("padding: 5px; border-radius: 3px;")
        btn_cancelar.clicked.connect(self.reject)
        layout_principal.addWidget(btn_cancelar, alignment=Qt.AlignmentFlag.AlignCenter)

    def ao_selecionar_monitor(self, tela):
        # Salva a tela selecionada e fecha o popup com status de Sucesso
        self.monitor_selecionado = tela
        #return self.monitor_selecionado
        self.accept()


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seleção Visual de Monitores")
        self.resize(600, 400)
        widget_central = QWidget(self)
        self.setCentralWidget(widget_central)
        layout = QVBoxLayout(widget_central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.botao = QPushButton("Detectar Monitores", self)
        self.botao.setFixedSize(120,40)
        layout.addWidget(self.botao, alignment=Qt.AlignmentFlag.AlignCenter)
        self.botao.clicked.connect(self.mostrar_popup)
        self.label_resultado = QLabel("Nenhum monitor selecionado ainda.", self)
        self.label_resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_resultado, alignment=Qt.AlignmentFlag.AlignCenter)

    def mostrar_popup(self):
        popup = PopupSelecaoMonitor(self)
        
        # Ajusta o tamanho do popup dinamicamente baseado no conteúdo
        popup.adjustSize()
        
        # Centraliza o popup
        centro_janela = self.geometry().center()
        popup.move(centro_janela.x() - popup.width() // 2, 
                   centro_janela.y() - popup.height() // 2)

        # Avalia o resultado
        if popup.exec() == QDialog.DialogCode.Accepted:
            tela = popup.monitor_selecionado
            if tela:
                self.label_resultado.setText(f"Você selecionou: {tela.name()}")
                self.informar_monitor_selecionado(tela.name())
                
    def informar_monitor_selecionado(self, monitor):
        scrpt_hyprpaper.monitor_selecionado = monitor

    def ultimo_monitor_selecionado(self, ultimo_monitor):
        self.label_resultado.setText(ultimo_monitor)
        print(f"Informado no moni {ultimo_monitor}")
        QApplication.processEvents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())
