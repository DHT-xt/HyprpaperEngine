####

import os
import json

####

class MngrConfigs:
    def __init__(self, arquivo="config/config.json"):
        self.arquivo = arquivo
        self.dados = {
                "ultima_pasta": "",
                "Ultimo_Indice": 0,
                "Opacidade": "100",
                "Tema_claro": "False",
                "Wallpapers": [],
                "Monitores": []
                }
        self.carregar()

    def carregar(self):
        if os.path.exists(self.arquivo):
            try:
                with open (self.arquivo, 'r', encoding='UTF-8') as f:
                    self.dados = json.load(f)
            except Exception as e:
                print(f"Erro ao ler as confgs {e}")
    
    def salvar(self):
        try:
            with open(self.arquivo, "w", encoding='UTF-8') as f:
                json.dump(self.dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar as configs {e}")


