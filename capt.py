import pandas as pd
import pytesseract
from rich import print
import time
import numpy as np
from PIL import ImageGrab
import mousekey
import rapidfuzz

# --- Configurações e Instâncias ---
mkey = mousekey.MouseKey()
mkey.enable_failsafekill('ctrl+e')
pytesseract.pytesseract.tesseract_cmd = r"C:\Arquivos de Programas\Tesseract-OCR\tesseract.exe"


# --- Função de Captura (Tira print da tela inteira) ---
def get_screenshot_tesser(minlen=2):
    img_pil = ImageGrab.grab() # Tira o screenshot da tela principal inteira
    img = np.array(img_pil)
    df = pytesseract.image_to_data(img, lang='por', output_type=pytesseract.Output.DATAFRAME)
    df = df.dropna(subset=["text"])
    df = df.loc[df.text.str.len() > minlen].reset_index(drop=True)
    return df


# --- Execução Principal do Robô (Lógica Visual) ---
if __name__ == "__main__":
    print("Iniciando automação em 4 segundos... Deixe a página do CAPTCHA visível.")
    time.sleep(4)

    # 1. Captura e analisa a tela inteira
    df = get_screenshot_tesser()
    
    if df.empty:
        print("[ERRO] Tesseract não encontrou nenhum texto na tela. Verifique se a janela correta estava em foco.")
    else:
        print("Tela analisada. Procurando pelo alvo...")
        
        # 2. Procura pela palavra 'sou' com o RapidFuzz
        palavra_alvo, pontuacao, indice = rapidfuzz.process.extractOne("sou", df['text'])
        
        # 3. Verifica se a confiança é alta o suficiente para clicar
        if pontuacao > 60: # Usamos 70 como um bom nível de confiança
            info_alvo = df.iloc[indice]
            coord_x = info_alvo['left']
            coord_y = info_alvo['top']
            
            print(f"Alvo '{palavra_alvo}' encontrado com {pontuacao:.2f}% de certeza em ({coord_x}, {coord_y})")

            # 4. Calcula as coordenadas do clique (à esquerda da palavra 'sou')
            click_x = coord_x - 30 
            click_y = coord_y + 10 
            
            print(f"Movendo o mouse de forma humana para ({click_x}, {click_y}) e clicando...")
            
            # 5. Move o mouse e clica de forma natural
            mkey.left_click_xy_natural(
                x=click_x,
                y=click_y,
                delay=0.2,
                sleeptime=(0.008, 0.015)
            )
            
            print("CAPTCHA acionado!")
        else:
            print(f"[INFO] A pontuação encontrada ({pontuacao:.2f}%) foi menor que o mínimo. O mouse não foi movido.")
            print("[DICA] Verifique se a página do CAPTCHA estava totalmente visível na tela principal.")