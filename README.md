# HyprpaperEngine

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Python](https://img.shields.io/badge/python-3572A5?style=for-the-badge&logo=python&logoColor=white)
![Qt](https://img.shields.io/badge/Qt-%2341CD52.svg?style=for-the-badge&logo=Qt&logoColor=white)

Seletor de wallpaper para o hyprpaper  
Ainda em desenvolvimento, mas grande parte funciona sem problema  

Utilizado Python e Shell Script  
O projeto tambem usa o Pyside6 do Qt framework  

As configuracoes sao salvas no .json  
Por padrao sera aberto no tema escuro  

## Funcionalidades

* 🔄 Alterna wallpapers instantaneamente sem reiniciar o Hyprpaper.
* 📂 Suporte para carregar imagens de uma pasta específica (`~/Pictures/Wallpapers`).
* ⚙️ Atualiza o arquivo de configuração automaticamente.

## Pré-requisitos

Antes de usar, garanta que você tem instalado:

* [Hyprland](https://hyprland.org/)
* [Hyprpaper](https://github.com/hyprwm/hyprpaper)

Para quem quiser desenvolver o projeto será preciso o Qt instalado

* [Qt](https://doc.qt.io/qt-6/linux-alternative-installers.html)

## Instalação

1. Baixe o executavel nas realeses 
    * [Realeses](https://github.com/DHT-xt/HyprpaperEngine/releases)

2. Execute o arquivo "HyprpaperEngine", mas se a caso nao abra use na pasta que salvou o executavel:
    ```bash
    chmod +x HyprpaperEngine


Ou caso preferir clonar o repositório

1. Clone este repositório:
   ```bash
   git clone [https://github.com/DHT-xt/HyprpaperEngine](https://github.com/DHT-xt/HyprpaperEngine.git)
   cd HyprpaperEngine

para executar

2. Execute com o python o arquivo main:
    ```bash
    python main.py


Ao executar deve aparecer um janela conforme o seguinte

<table border="0">
  <tr>
    <td>
      <p align="center"><b>Modo Claro</b></p>
      <img src="./Assets/imgs/593227979-7126c380-7e9d-4a34-ac6c-44ed450905de.png" width="944" height="1021" alt="Modo Claro">
    </td>
    <td>
      <p align="center"><b>Modo Escuro</b></p>
      <img src="./Assets/imgs/593228016-85a14c94-7a28-42bc-a17f-5ccd644735fd.png" width="944" height="1021" alt="Modo Escuro">
    </td>
  </tr>
</table>

Obs: Os cards de preview dos wallpapers serao gerados ao selecionar a pasta

## Utilizar

Apos executar e a janela aparecer, sera preciso:

* Informar qual monitor utilizar pela opcao de selecao de monitores

* Informar a pasta de imagens que deseja utilizar para a selecao de Wallpapers

IMPORTANTE:

 * O arquivo de configuracao json fica salvo em /home/{SeuUsuario}/config/config.json

 * Caso ja tenha um .conf do hyprpaper, eh feito o backup em /home/{SeuUsuario}/HyprpaperEngine/backup/

 * Suporta mais de uma pasta selecionada, porem mais de duas pastas podem causar problema na exibicao no layout (Esperado corrigir em breve)

Para selecionar o wallpaper, basta apenas clicar em cima da preview do mesmo

## Adicional

Atualmente eh uma versao alpha (Mais para prototipo)  
Bugs sao esperados

Enfim ;)
