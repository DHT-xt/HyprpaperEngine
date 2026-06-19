import sys
import os
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, 
                               QFrame, QLabel, QVBoxLayout)
from PySide6.QtCore import Qt, QPointF, QPropertyAnimation, QEasingCurve, QRect, Signal
from PySide6.QtGui import QWheelEvent, QPainter, QPixmap, QPainterPath

try:
    from hypr_script import scrpt_hyprpaper
except ImportError:
    print("Error: No module named scrpt_hyprpaper")
    scrpt_hyprpaper = None


# ==========================================
# CLASSE 1: IMG CARD
# ==========================================
class ImageCard(QFrame):
    clicked = Signal(str)

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        card_width = 160
        card_height = 220
        corner_radius = 12
        self.setFixedSize(card_width, card_height)
        self.setCursor(Qt.PointingHandCursor)
        
        self.setStyleSheet("""
            QFrame {
                background-color: #00000000;            
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border-radius: 10px;")
        
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                self.size(), 
                Qt.KeepAspectRatioByExpanding, 
                Qt.SmoothTransformation
            )
            
            crop_x = (scaled_pixmap.width() - card_width) // 2
            crop_y = (scaled_pixmap.height() - card_height) // 2
            crop_rect = QRect(crop_x, crop_y, card_width, card_height)
            cropped_pixmap = scaled_pixmap.copy(crop_rect)
            
            rounded_pixmap = QPixmap(card_width, card_height)
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            path = QPainterPath()
            path.addRoundedRect(0, 0, card_width, card_height, corner_radius, corner_radius)
            
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, cropped_pixmap)
            painter.end() 
            
            self.label.setPixmap(rounded_pixmap)
        else:
            self.label.setText("Erro")
            self.label.setStyleSheet("color: white;")

        layout.addWidget(self.label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.image_path)
            event.accept()
        else:
            super().mousePressEvent(event)


# ==========================================
# CLASSE 2: GALLERY (Central)
# ==========================================
class HorizontalHoverCarousel(QGraphicsView):
    def __init__(self, folder_path):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        # Alinhamento essencial para a centralização funcionar
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop) 
        
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
        
        self.load_images_from_directory(folder_path)

    def load_images_from_directory(self, folder_path):
        # Limpa a cena antes de carregar novas imagens (Resolve o bug de múltiplas pastas)
        self.scene.clear()       
        self.items.clear()       
        self.animations.clear()  
        self.scroll_x = 0        
        
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
        
        if not os.path.exists(folder_path):
            print(f"Aviso: Pasta '{folder_path}' não encontrada.")
            return

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(valid_extensions):
                full_path = os.path.join(folder_path, filename)         
                
                widget = ImageCard(full_path)
                widget.clicked.connect(self.on_card_clicked)

                proxy = self.scene.addWidget(widget)
                
                self.items.append(proxy)
                self.animations.append(None)
                
        if not self.items:
            print("Nenhuma imagem encontrada na pasta.")
        else:
            self.update_layout(animated=False)

    def on_card_clicked(self, image_path):
        print(f"\n---> IMAGEM SELECIONADA: {image_path}")
        if scrpt_hyprpaper:
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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scene.setSceneRect(0, 0, self.viewport().width(), self.viewport().height())
        if self.items:
            self.update_layout(animated=False)

    def update_layout(self, animated=True):
        num_items = len(self.items)
        if num_items == 0:
            return

        x_spacing = 60  
        card_width = 160 
        card_height = 220 
        
        view_width = self.viewport().width()
        view_height = self.viewport().height()
        
        total_cards_width = ((num_items - 1) * x_spacing) + card_width
        
        # Lógica de Centralização Dinâmica
        start_x = (view_width - total_cards_width) / 2
        base_y = (view_height - card_height) / 2    
        
        for i in range(num_items):
            target_x = start_x + self.scroll_x + (i * x_spacing)
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
                anim.setDuration(150) 
                anim.setEasingCurve(QEasingCurve.OutQuad)
                self.animations[i] = anim
                anim.start()
            else:
                self.items[i].setPos(target_x, target_y)


# ==========================================
# SOLO APP EXEC (TEST ONLY)
# ==========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    IMG_FOLDER_PATH = "" 
    
    if not os.path.exists(IMG_FOLDER_PATH):
        os.makedirs(IMG_FOLDER_PATH)
        print(f"Created empty folder in {os.path.abspath(IMG_FOLDER_PATH)}")
        print("Shove some imgs there!")
    
    view = HorizontalHoverCarousel(IMG_FOLDER_PATH)
    view.resize(1000, 500)
    view.setWindowTitle("Image-gallery-test")
    view.show()
    sys.exit(app.exec())
