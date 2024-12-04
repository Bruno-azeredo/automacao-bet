import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import pyautogui
import pytesseract
import pyscreenshot as ImageGrab
import time

def capture_screen():
    # Captura uma região específica da tela onde o número aparece
    # Ajuste as coordenadas (left, top, right, bottom) conforme necessário
    screenshot = ImageGrab.grab(bbox=(100, 200, 300, 400))
    return screenshot

def process_image(image):
    # Converte a imagem para texto usando pytesseract
    text = pytesseract.image_to_string(image)
    return text

def find_number_and_click(text):
    # Procura por números na string e realiza a ação se algum for menor que 2
    try:
        numbers = [float(num) for num in text.split() if num.replace('.', '', 1).isdigit()]
        for number in numbers:
            if number < 2:
                # Realiza a ação de clique
                # Ajuste as coordenadas (x, y) conforme necessário
                pyautogui.click(x=150, y=250)
                print("Número menor que 2 encontrado e clique realizado!")
                break
    except Exception as e:
        print(f"Erro ao processar número: {e}")

def main():
    while True:
        # Captura a tela
        screenshot = capture_screen()

        # Processa a imagem e extrai texto
        text = process_image(screenshot)

        # Procura pelo número e realiza ação
        find_number_and_click(text)

        # Aguardar um intervalo antes de capturar novamente
        time.sleep(2)

if __name__ == "__main__":
    main()
