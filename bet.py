from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuração do WebDriver (por exemplo, Chrome)
options = webdriver.ChromeOptions()
path = r'C:\Users\Pichau\Downloads\chromedriver-win64 (2)\chromedriver-win64\chromedriver.exe'
driver = webdriver.Chrome(path, options=options)

# URL do site
url = 'https://superbet.com/pt-br/sport-bets/football/today'
driver.get(url)

# Aguardar o carregamento da página e realizar login manualmente, se necessário
time.sleep(30)  # Ajuste o tempo conforme necessário para realizar o login

# Listas para armazenar odds e elementos já selecionados
selected_odds = []
selected_elements = []

# Função para monitorar e clicar
def monitor_and_click():
    repeat_count = 50  # Número de repetições do processo
    while repeat_count > 0:
        try:
            # Laço para selecionar 3 odds sem repetir
            for _ in range(3):
                # Localizar elementos com a classe especificada
                elements = WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'odd-button__odd-value-new') and contains(@class, 'e2e-odd-current-value')]"))
                )
                
                # Inicializa um índice para percorrer as odds
                idx = 0
                
                while idx < len(elements):
                    element = elements[idx]
                    odds_value = float(element.text.strip())
                    element_id = element.get_attribute("id")  # Usar o atributo ID ou outro identificador único
                    
                    if odds_value > 1.20 and odds_value < 1.56 and element_id not in selected_elements:
                        selected_odds.append(odds_value)
                        selected_elements.append(element_id)
                        
                        button = element.find_element(By.XPATH, ".//ancestor::button[contains(@class, 'odd-button')]")
                        button.click()
                        print(f"Elemento com valor {odds_value} e ID {element_id} clicado!")

                        # Esperar 20 segundos após o clique
                        time.sleep(10)

                        # Localizar o campo de entrada, limpar e inserir o número 5
                        stake_input = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, "stake-0"))
                        )
                        stake_input.clear()  # Limpar qualquer valor existente
                        stake_input.send_keys(Keys.BACKSPACE * 3)  # Apagar o valor existente
                        stake_input.send_keys("2")  # Inserir o número 5
                        print("Valor 2 inserido no campo de entrada!")

                        # Esperar 3 segundos antes de clicar no botão "Fazer aposta"
                        time.sleep(3)
                        submit_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'sds-button--primary-elevation') and contains(@class, 'e2e-betslip-submit')]"))
                        )
                        submit_button.click()
                        print("Botão 'Fazer aposta' clicado!")

                        # Esperar 3 segundos antes de atualizar a página
                        time.sleep(12)
                        driver.refresh()
                        print("Página recarregada com F5!")
                        time.sleep(3)
                        break
                    
                    # Incrementa o índice para verificar a próxima odd
                    idx += 1

            # Após o laço, imprimir o valor do saldo
            balance_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'balance') and contains(@class, 'e2e-balance')]"))
            )
            balance_value = balance_element.text.strip().split()[0]
            print(f"Saldo atual: {balance_value} R$")

            # Cronômetro de 20 minutos
            total_time = 10 * 60  # 20 minutos em segundos
            for remaining in range(total_time, 0, -1):
                mins, secs = divmod(remaining, 60)
                timer = f"{mins:02d}:{secs:02d}"
                print(f"\rTempo restante: {timer}", end="")
                time.sleep(1)
            print("\nTempo de espera concluído, atualizando a página...")

            driver.refresh()
            print("Página recarregada!")

            # Esperar 4 segundos após recarregar a página
            time.sleep(4)

            # Reduzir o contador de repetições
            repeat_count -= 1
            print(f"Processo repetido {50 - repeat_count} vezes!")

        except Exception as e:
            print(f"Erro: {e}")
        # Aguardar um intervalo antes de verificar novamente
        time.sleep(5)

if __name__ == "__main__":
    monitor_and_click()

# Fechar o navegador
driver.quit()
