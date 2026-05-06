from contextlib import nullcontext
from os.path import isdir
from hypr_script import scrpt_hyprpaper
import sys, os,hypr_script.scrpt_hyprpaper

####

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

####

from config import moni
from config.moni import JanelaPrincipal, PopupSelecaoMonitor
from ui.carrossel_config import Path_carrossel
from ui.tr_background import configurar_transparencia
from ui.UI_Configs import Buttongr 
from config.config_mgr import MngrConfigs
from hypr_script.scrpt_hyprpaper import conf, hyprpaper


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        check_hyprpaper_status = hyprpaper()
        if not check_hyprpaper_status.check_hyprpaper():
            check_hyprpaper_status.init_hyprpaper() 
        self.hypr_script = conf()
        self.hypr_script.check_init()
        self.imgcarrossel = Path_carrossel()
        self.selct_monitor = JanelaPrincipal()
        self.monitor_selected = PopupSelecaoMonitor()
        #self.testimg = HorizontalHoverCarousel("/home/michel/wallpaper/" )
        self.config_salva = MngrConfigs() 
        self.config_ui = Buttongr(self, self.config_salva.dados["Tema_claro"])
        #self.transparencia_config = configurar_transparencia(self) 
        if self.config_salva.dados["ultima_pasta"]:
            self.imgcarrossel.load_images_from_folder(self.config_salva.dados["ultima_pasta"])
        if self.config_salva.dados["Ultimo_monitor"]:
            self.selct_monitor.ultimo_monitor_selecionado(self.config_salva.dados["Ultimo_monitor"])
            scrpt_hyprpaper.monitor_selecionado = self.config_salva.dados["Ultimo_monitor"]
        #elif self.hypr_script.check_init():
            #monitores, wallpapers = self.hypr_script.check_init()
            #self.config_salva.dados["Wallpapers"] = wallpapers
            #self.config_salva.dados["Monitores"] = monitores
            #print("monitores e wallpapers salvos no json")
        self.setWindowTitle("Hyprpaper Engine")
        self.text = QLabel("Local dos wallpapers", self)       
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget) 
        layout.addWidget(self.config_ui)
        layout.addWidget(self.selct_monitor)
        layout.addWidget(self.text)
        layout.addWidget(self.imgcarrossel)

    def closeEvent(self, event):
        """Evento disparado quando o usuário fecha a janela"""
        self.config_salva.dados["ultima_pasta"] = self.imgcarrossel.pasta_atual
        self.config_salva.dados["Tema_claro"] = self.config_ui.temaclaro_atual
        if scrpt_hyprpaper.monitor_selecionado:
            self.config_salva.dados["Ultimo_monitor"] = scrpt_hyprpaper.monitor_selecionado
        self.hypr_script.check()
        self.config_salva.salvar()
        event.accept() 


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
