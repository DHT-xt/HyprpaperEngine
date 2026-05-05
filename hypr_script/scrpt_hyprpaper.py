import os, configparser, shutil, subprocess, re
from os.path import expanduser, isdir, isfile

monitor_selecionado = ""
wallpaper_selecionado = ""

class hyprpaper():
    def __init__(self):
        pass
    
    def alt_wallpaper(self):
        global monitor_selecionado, wallpaper_selecionado
        wallpaper = wallpaper_selecionado
        monitor = monitor_selecionado
        try:
            # Nas versões novas do Hyprpaper, o preload foi removido.
            # O comando 'wallpaper' já faz todo o trabalho diretamente.
            comando_wallpaper = f"{monitor},{wallpaper}"
            
            # Executa o comando e usa check=True para capturar falhas
            #subprocess.run(["hyprctl", "hyprpaper", "preload", wallpaper])
            subprocess.run(["hyprctl", "hyprpaper", "wallpaper", comando_wallpaper])
            #subprocess.run(["hyprctl", "hyprpaper", "unload", "unused"])

            # Feedback de sucesso (se monitor for vazio, é fallback em todos)
            nome_monitor = monitor if monitor else "todos (fallback)"
            print(f"Sucesso: Papel de parede alterado no monitor: {nome_monitor}")
            
        except subprocess.CalledProcessError as e:
            # Vai capturar caso a imagem não exista ou o hyprpaper rejeite o pedido
            print(f"Erro ao executar o comando hyprctl: {e}")
            
        except FileNotFoundError:
            print("Erro: O comando 'hyprctl' não foi encontrado. O Hyprland está rodando?")

class conf():
    def __init__(self):
        monitores_teste = []
        wall_teset = ["home/wall/1"]
        #self.check(monitores_teste, wall_teset)
        
    def check(self, monitores=None, wallpapers=None):
        self.wall_path = wallpapers
        self. monitores_id = monitores
        self.hyprpaper_path = os.path.expanduser("~/.config/hypr")
        if not os.path.isdir(self.hyprpaper_path):
            os.mkdir(self.hyprpaper_path)
        self.arquivo = os.path.expanduser('~/hyprengine/hyprpaper.conf')
        texto_procurado = '# HYPRENGINE Version: 1.0'
        #texto_procurado como validador da gen da conf pelo hyprengine
        if not isfile(self.arquivo):
            self.criar()
        else:
            with open('hyprpaper.conf', 'r') as f:
                conteudo = f.read()
                if texto_procurado in conteudo:
                    print("O texto existe no arquivo!")
                    self.bckp_path = os.path.expanduser("~/hyprengine/hyprpaper_bckup")
                    self.run_arquivo()
                else:
                    print("Texto não encontrado.")
                    self.bckp_path = os.path.expanduser("~/hyprengine/hyprpaper_conf_nongen")
                    self.run_arquivo()


    def run_arquivo(self):
        if isdir(self.bckp_path):
            os.rename(self.arquivo, "hyprpaper_bckup.conf")
            os.replace(os.path.expanduser("~/hyprengine/hyprpaper_bckup.conf"), f'{self.bckp_path}/hyprpaper_bckup.conf')
            self.criar()
        else:
            os.mkdir(self.bckp_path)
            self.run_arquivo()

        print("pac")
    
    def criar(self):
        caminho_config = os.path.expanduser('~/hyprengine/hyprpaper.conf')
        versao = "1.0"
        splash = "false"

        try:
            with open(caminho_config, 'w') as f:
                f.write(f"# HYPRENGINE Version: {versao}\n\n")

                for monitor, path in zip(self.monitores_id, self.wall_path):
                    f.write(f"wallpaper {{\n")
                    f.write(f"    monitor = {monitor}\n")
                    f.write(f"    path = {path}.png\n")
                    f.write(f"    fit_mode = 1\n")
                    f.write(f"}}\n\n")
            
                f.write(f"splash = {splash}\n")

            print(f"Arquivo {caminho_config} criado com sucesso!")
        
        except Exception as e:
            print(f"Erro ao criar arquivo: {e}")
    
    #def check_init(self):
    def check_init(self):
        hyprpaper_path = os.path.expanduser("~/.config/hypr")
        arquivo = os.path.expanduser('~/hyprengine/hyprpaper.conf')
        if not os.path.isdir(hyprpaper_path):
            return
        else:
            with open(arquivo, 'r') as f:
                conteudo = f.read()
            monitores_conf = re.findall(r"monitor\s*=\s*(.+)", conteudo)
            wallpapers_conf = re.findall(r"path\s*=\s*(.+)", conteudo)
            return monitores_conf, wallpapers_conf

conf() 
