import sys
from PySide6.QtWidgets import QApplication, QCheckBox, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QRect, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QGuiApplication

####

class SwitchButton(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 28)
        self.setCursor(Qt.PointingHandCursor)
        
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setDuration(1200)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

    @Property(float)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    def nextCheckState(self):
        super().nextCheckState()
        start = 3 if not self.isChecked() else 34
        end = 34 if self.isChecked() else 3
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        
        bg_color = QColor("#c5dbff") if self.isChecked() else QColor("#6f6f6f")
        
        p.setBrush(bg_color)
        p.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)
        
        if self.isChecked():
            p.setBrush(QColor("#ffffff"))

           
        else: 
            p.setBrush(QColor("#2e2e2e"))
            
        p.drawEllipse(int(self._circle_position), 3, 22, 22)
        p.end()

class Buttongr(QWidget):
    def __init__(self, Outrajanela, Tema_claro= False):
        super().__init__()
        layout = QVBoxLayout(self)
        self.switch = SwitchButton()
        if not Tema_claro:
            self.cor_fundo_inicial = cor_fundo(Outrajanela, self.switch.isChecked())
            self.temaclaro_atual = False
        else:
            self.cor_fundo_inicial = cor_fundo(Outrajanela, True)
            self.switch.setChecked(True)
            self.temaclaro_atual = True
        self.switch.clicked.connect(lambda: self.att_tema(Outrajanela))
        layout.addWidget(self.switch, alignment=Qt.AlignCenter)
        self.resize(200, 150)

    def att_tema(self, Outrajanela):
        cor_fundo(Outrajanela, self.switch.isChecked())
        if self.switch.isChecked():
            self.temaclaro_atual = True
        else:
            self.temaclaro_atual = False


def cor_fundo(janela_alvo, button_check=False):
    if not button_check:
        janela_alvo.setStyleSheet("""
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
                QMainWindow {
                    background-color: #101010;;
                }
                QMainWindow {
                    background-color: #101010;;
                }
                QLabel {
                    color: #ffffff;
                    font-size: 14px;
                    font-weight: bold;
                }
                    """)         
    else:
        janela_alvo.setStyleSheet("""
                QPushButton {
                    background-color: #c5dbff;
                    color: black;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0078d7;
                }
                QMainWindow {
                    background-color: #f0f0f0;;
                }
                QMainWindow {
                    background-color: #f0f0f0;;
                }
                QLabel {
                    color: #000000;
                    font-size: 14px;
                    font-weight: bold;
                }
                    """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Buttongr()
    w.show()
    sys.exit(app.exec())
