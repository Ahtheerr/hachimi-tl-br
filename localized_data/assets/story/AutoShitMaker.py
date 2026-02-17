import pyautogui
import keyboard
import time

# --- CONFIGURAÇÕES ---
# Tempo de segurança entre cada ação (para o PC não travar)
pyautogui.PAUSE = 0.05 

# Se der ruim, arraste o mouse bruscamente para o canto superior esquerdo da tela para parar
pyautogui.FAILSAFE = True 

def automacao():
    print("Posicione a janela e pressione 'F1' para COMEÇAR.")
    print("Segure 'F2' para PARAR.")
    
    # Espera apertar F1 para começar
    keyboard.wait('F1')
    
    while True:
        # Checa se deve parar
        if keyboard.is_pressed('F2'):
            print("Parando...")
            break

        # --- 1. CLICAR NA LISTA E DESCER ---
        # Clica na lista lateral (no item cinza ou área da lista)
        pyautogui.click(x=600, y=263) # <--- COORDENADA DA LISTA
        pyautogui.press('down')
        time.sleep(0.05) # Tempo extra para carregar o texto na tela

        # --- 2. COPIAR NOME (CIMA PARA BAIXO) ---
        # Clica no Nome Original (Cima)
        pyautogui.click(x=719, y=153) # <--- COORDENADA NOME ORIGINAL
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')

        # Clica no Nome Tradução (Baixo)
        pyautogui.click(x=714, y=595) # <--- COORDENADA NOME TRADUÇÃO
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'v')

        # --- 3. COPIAR TEXTO (CIMA PARA BAIXO) ---
        # Clica na Fala Original (Cima)
        pyautogui.click(x=711, y=216) # <--- COORDENADA FALA ORIGINAL
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')

        # Clica na Fala Tradução (Baixo)
        pyautogui.click(x=712, y=644) # <--- COORDENADA FALA TRADUÇÃO
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'v')

        # Pequena pausa antes de recomeçar o loop
        time.sleep(0.05)

if __name__ == "__main__":
    automacao()