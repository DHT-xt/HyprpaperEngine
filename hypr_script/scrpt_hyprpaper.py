import os, subprocess, re
from config import moni
from hypr_script.log import info_log
from os.path import expanduser, isdir, isfile

monitor_selecionado = ""
wallpaper_selecionado = ""

monitor_data = []
wallpaper_data = []

class hyprpaper():
    def __init__(self):
        self.informar_erro = info_log()
        pass
    
    def alt_wallpaper(self):
        global monitor_selecionado, wallpaper_selecionado
        wallpaper = wallpaper_selecionado
        monitor = monitor_selecionado
        if not monitor:
            self.informar_erro.aviso("Monitor nao selecionado")
        else:
            comando_wallpaper = f"{monitor},{wallpaper}"
            subprocess.run(["hyprctl", "hyprpaper", "wallpaper", comando_wallpaper])
            self.data_conf(monitor, wallpaper)

    def data_conf(self, monitor_selecionado, wallpaper_selecionado):
        global monitor_data, wallpaper_data
        for i in range(len(monitor_data)):
            if monitor_data[i] == monitor_selecionado:
                wallpaper_data[i] = wallpaper_selecionado
    
    def monitor_check(self, monitores):
        global monitor_data, wallpaper_data
        wallpaper_ordem_errada = []
        monitores_ordem_errada = []
        
        if len(monitor_data) > len(monitores):
            #monitor_data = [item for item in monitor_data if item in monitores]
            un_monitores = [
                    (a1, a2)
                    for a1, a2 in zip(monitor_data, wallpaper_data)
                    if a1 in monitores
                    ]
            monitor_data = [x[0] for x in un_monitores]
            wallpaper_data = [x[1] for x in un_monitores]
            #monitor_data = monitores

        if monitor_data:
            for i, _ in enumerate(monitores):
                if not monitor_data[i] == monitores[i]:
                    monitores_ordem_errada.append(monitor_data[i])
                    wallpaper_ordem_errada.append(wallpaper_data[i])
                    monitor_data[i] = _
        else:
            monitor_data = monitores
            wallpaper_data = [None]*len(monitor_data)

        if monitores_ordem_errada:
            for i, _ in enumerate(monitor_data):
                for si, __ in enumerate(monitores_ordem_errada):
                    if monitor_data[i] == monitores_ordem_errada[si]:
                        wallpaper_data[i] = wallpaper_ordem_errada[si]
    
    def check_hyprpaper(self):
        try: 
            subprocess.check_output(["pgrep", "hyprpaper"])
            return True
        except subprocess.CalledProcessError:
            return False

    def init_hyprpaper(self):
        try:
            subprocess.Popen(
                ["hyprpaper"],
                stdout=subprocess.DEVNULL,  
                stderr=subprocess.DEVNULL,  
                start_new_session=True      
            )
        except Exception as e: 
            self.informar_erro.erro_msg(e)

class conf():
    def __init__(self):
        self.informar_erro = info_log()
        pass

    def check(self):
        self.hyprpaper_path = os.path.expanduser("~/.config/hypr")
        if not os.path.isdir(self.hyprpaper_path):
            os.mkdir(self.hyprpaper_path)
        self.arquivo = os.path.expanduser('~/.config/hypr/hyprpaper.conf')
        hyprpaper_path = os.path.expanduser("~/HyprpaperEngine")
        if not os.path.isdir(f'{hyprpaper_path}/backup'):
            os.mkdir(f'{hyprpaper_path}/backup')
        arquivo2 = os.path.expanduser('~/.config/hypr/hyprpaper.conf')
        texto_procurado = '# HYPRENGINE Version: 1.0'
        if not isfile(self.arquivo):
            self.criar()
        else:
            with open(arquivo2, 'r') as f:
                conteudo = f.read()
                if texto_procurado in conteudo: 
                    self.bckp_path = os.path.expanduser("~/HyprpaperEngine/backup/hyprpaperconf_backup")
                    self.run_arquivo()
                else:
                    self.bckp_path = os.path.expanduser("~/HyprpaperEngine/backup/hyprpaperconf_user")
                    self.run_arquivo()


    def run_arquivo(self):
        if isdir(self.bckp_path):

            arquivo_bckp = "hyprpaper_bckup.conf"
            path_arquivo_bckp = os.path.expanduser("~/.config/hypr/hyprpaper_bckup.conf")

            os.rename(self.arquivo, path_arquivo_bckp)
            os.replace(os.path.expanduser(path_arquivo_bckp), f'{self.bckp_path}/{arquivo_bckp}')
            self.criar()
        else:
            os.mkdir(self.bckp_path)
            self.run_arquivo()

    def criar(self):
        global monitor_data, wallpaper_data
        caminho_config = os.path.expanduser('~/.config/hypr/hyprpaper.conf')
        versao = "1.0"
        splash = "false"

        try:
            with open(caminho_config, 'w') as f:
                f.write(f"# HYPRENGINE Version: {versao}\n\n")

                for monitor, wallpaper in zip(monitor_data, wallpaper_data):
                    f.write(f"wallpaper {{\n")
                    f.write(f"    monitor = {monitor}\n")
                    f.write(f"    path = {wallpaper}\n")
                    f.write(f"    fit_mode = cover\n")
                    f.write(f"}}\n\n")
            
                f.write(f"splash = {splash}\n")
            

         
        except Exception as e:
            self.informar_erro.erro_msg(e)
    
    def check_init(self):
        hyprpaper_path = os.path.expanduser("~/.config/hypr")
        arquivo = os.path.expanduser('~/.config/hypr/hyprpaper.conf')
        if not os.path.isdir(hyprpaper_path):
            return
        if not isfile(arquivo):
            return
        else:
            with open(arquivo, 'r') as f:
                conteudo = f.read()
            monitores_conf = re.findall(r"monitor\s*=\s*(.+)", conteudo)
            wallpapers_conf = re.findall(r"path\s*=\s*(.+)", conteudo)
            global wallpaper_data, monitor_data
            wallpaper_data = wallpapers_conf
            monitor_data = monitores_conf
            return monitores_conf, wallpapers_conf
