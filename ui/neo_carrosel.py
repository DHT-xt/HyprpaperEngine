import sys
import os
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, 
                               QFrame, QLabel, QVBoxLayout)
from PySide6.QtCore import Qt, QPointF, QPropertyAnimation, QEasingCurve, QRect, Signal
from PySide6.QtGui import QWheelEvent, QPainter, QPixmap, QPainterPath

from hypr_script import scrpt_hyprpaper

class ImageCard(QFrame):

    clicked = Signal(str)

    def __init__(self, image_path):
        super().__init__()
        # O tamanho fixo do preview do card
        self.image_path = image_path
        card_width = 160
        card_height = 220
        corner_radius = 12
        self.setFixedSize(card_width, card_height)

        self.setCursor(Qt.PointingHandCursor)
        
        # Estilo do frame com borda arredondada e um fundo escuro caso a imagem não carregue
        self.setStyleSheet("""
            QFrame {
                background-color: #00000000;            
                }
        """)
        
        # Removemos as margens do layout para a imagem colar nas bordas
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        
        # Para arredondar as bordas internas do QLabel também
        self.label.setStyleSheet("border-radius: 10px;")
       
        
        # --- Lógica de Carregamento e Crop da Imagem ---
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            # 1. Escala a imagem (mesma lógica anterior)
            scaled_pixmap = pixmap.scaled(
                self.size(), 
                Qt.KeepAspectRatioByExpanding, 
                Qt.SmoothTransformation
            )
            
            # 2. Corta o centro (Crop)
            crop_x = (scaled_pixmap.width() - card_width) // 2
            crop_y = (scaled_pixmap.height() - card_height) // 2
            crop_rect = QRect(crop_x, crop_y, card_width, card_height)
            cropped_pixmap = scaled_pixmap.copy(crop_rect)
            
            # --- O SEGREDO DO ARREDONDAMENTO AQUI ---
            # 3. Cria um Pixmap em branco transparente do tamanho do card
            rounded_pixmap = QPixmap(card_width, card_height)
            rounded_pixmap.fill(Qt.transparent)
            
            # 4. Usa o QPainter para desenhar a imagem recortada dentro de uma forma arredondada
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            path = QPainterPath()
            path.addRoundedRect(0, 0, card_width, card_height, corner_radius, corner_radius)
            
            # Aplica o formato arredondado como "molde"
            painter.setClipPath(path)
            # Desenha a imagem dentro desse molde
            painter.drawPixmap(0, 0, cropped_pixmap)
            painter.end() # Importante finalizar o painter
            # ----------------------------------------
            
            self.label.setPixmap(rounded_pixmap)
        else:
            self.label.setText("Erro")
            self.label.setStyleSheet("color: white;")

        layout.addWidget(self.label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Emite o sinal avisando que foi clicado e manda o caminho da imagem
            self.clicked.emit(self.image_path)
            event.accept()
        else:
            super().mousePressEvent(event)

class HorizontalHoverCarousel(QGraphicsView):
    def __init__(self, folder_path):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(-2000, -1000, 4000, 2000)
        self.setScene(self.scene)
        
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setStyleSheet("background: #121212; border: none;")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.setMouseTracking(True)
        
        self.items = []
        self.animations = []
        self.hovered_index = None
        self.scroll_x = 0
        
        # Carrega as imagens da pasta
        self.load_images_from_directory(folder_path)
        self.update_layout(animated=False)

    def load_images_from_directory(self, folder_path):
        """Lê a pasta e cria um card para cada imagem encontrada"""
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
        
        if not os.path.exists(folder_path):
            print(f"Aviso: Pasta '{folder_path}' não encontrada.")
            return

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(valid_extensions):
                full_path = os.path.join(folder_path, filename)         
                # Cria o card com a imagem
                widget = ImageCard(full_path)

                widget.clicked.connect(self.on_card_clicked)

                proxy = self.scene.addWidget(widget)
                
                self.items.append(proxy)
                self.animations.append(None)
                
        if not self.items:
            print("Nenhuma imagem encontrada na pasta.")

    def on_card_clicked(self, image_path):
        # Aqui você faz o que quiser com a imagem selecionada!
        print(f"\n---> IMAGEM SELECIONADA: {image_path}")
        alterar_wallpaper = scrpt_hyprpaper.hyprpaper()
        scrpt_hyprpaper.wallpaper_selecionado = image_path
        alterar_wallpaper.alt_wallpaper()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self._check_hover(event.pos())

    def leaveEvent(self, event):
        self.hovered_index = None
        self.update_layout(animated=True)
        super().leaveEvent(event)

    def _check_hover(self, pos):
        scene_pos = self.mapToScene(pos)
        items_at_pos = self.scene.items(scene_pos)
        new_hover = None
        
        for item in items_at_pos:
            if item in self.items:
                new_hover = self.items.index(item)
                break
            elif item.parentItem() in self.items:
                new_hover = self.items.index(item.parentItem())
                break
                
        if new_hover != self.hovered_index:
            self.hovered_index = new_hover
            self.update_layout(animated=True)

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        if delta == 0:
            delta = event.angleDelta().x()
            
        self.scroll_x += delta * 0.8
        self._check_hover(event.position().toPoint())
        self.update_layout(animated=False)
        event.accept()

    def update_layout(self, animated=True):
        num_items = len(self.items)
        x_spacing = 60  # Distância entre os cards (sobreposição)
        base_y = 200    
        
        for i in range(num_items):
            target_x = self.scroll_x + (i * x_spacing)
            target_y = base_y
            z_val = i 
            
            if self.hovered_index is not None:
                rel = i - self.hovered_index
                z_val = 100 - abs(rel)
                push_up = max(0, 3 - abs(rel)) * 25
                target_y = base_y - push_up

            self.items[i].setZValue(z_val)
            
            if animated:
                anim = QPropertyAnimation(self.items[i], b"pos")
                anim.setEndValue(QPointF(target_x, target_y))
                anim.setDuration(150) # Animação levemente mais rápida (150ms)
                anim.setEasingCurve(QEasingCurve.OutQuad)
                self.animations[i] = anim
                anim.start()
            else:
                self.items[i].setPos(target_x, target_y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # IMPORTANTE: Coloque aqui o caminho de uma pasta com fotos do seu PC
    PASTA_DE_IMAGENS = "/home/michel/wallpaper/" 
    
    # Cria a pasta temporariamente só para o código não quebrar se não existir
    if not os.path.exists(PASTA_DE_IMAGENS):
        os.makedirs(PASTA_DE_IMAGENS)
        print(f"Criei uma pasta vazia em {os.path.abspath(PASTA_DE_IMAGENS)}")
        print("Coloque algumas imagens lá para testar!")
    
    view = HorizontalHoverCarousel(PASTA_DE_IMAGENS)
    view.resize(1000, 500)
    view.setWindowTitle("Galeria de Imagens Dinâmica")
    view.show()
    sys.exit(app.exec())
