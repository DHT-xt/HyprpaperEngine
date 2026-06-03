import sys
import os

####

from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from shiboken6 import delete

####

#from ui.neo_carrosel import HorizontalHoverCarousel
from ui.carr_teste import HorizontalHoverCarousel


class Path_carrossel(QWidget):
    def __init__(self):
        super().__init__()
        self.pasta_quantidade = 0
        self.image_paths = []
        self.current_index = 0
        self.init_ui()
    def init_ui(self):

        # Layout Principal
        self.main_layout = QVBoxLayout(self)

        # Botão para selecionar pasta
        self.btn_open = QPushButton("Selecionar Pasta de Imagens")
        self.btn_close = QPushButton("Fechar as pastas")
        self.btn_open.clicked.connect(self.load_images_from_folder)
        self.btn_close.clicked.connect(self.delete_folder)
        self.main_layout.addWidget(self.btn_open)
        self.main_layout.addWidget(self.btn_close)

    def load_images_from_folder(self, folder=None):
    # Se 'folder' não for passado, ele abre a janela de seleção
        if not folder:
            folder = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
    
        if folder:
            # Armazena a pasta atual para podermos salvar no JSON depois
            self.pasta_atual = folder 
        
            extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')
            self.image_paths = [
                os.path.join(folder, f) for f in os.listdir(folder) 
                if f.lower().endswith(extensions)
            ]
        
            if self.image_paths:
                self.current_index = 0
                self.run_carro = HorizontalHoverCarousel(self.pasta_atual)
                self.pasta_quantidade = self.pasta_quantidade + 1
                self.main_layout.addWidget(self.run_carro)

    def delete_folder(self):
        if self.image_paths:
            self.main_layout.removeWidget(self.run_carro)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Path_carrossel()
    window.show()
    sys.exit(app.exec())
