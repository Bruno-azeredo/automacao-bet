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
url = 'https://superbet.com/pt-br/sport-bets/football/live'
driver.get(url)

# Função para realizar login
def login():
    time.sleep(5)
    try:
        # Clicar no botão "Entrar"
        entrar_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'capitalize') and text()='entrar']"))
        )
        entrar_button.click()
        time.sleep(1)  # Aguardar um tempo para garantir que a ação seja registrada

        # Digitar o nome de usuário no campo de entrada
        username_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'input__field')]"))
        )
        username_input.send_keys("bazeredo")
        time.sleep(1)  # Aguardar um tempo para garantir que a ação seja registrada

        # Digitar a senha no campo de entrada
        password_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'password-input__field')]//input[@type='password']"))
        )
        password_input.send_keys("Bazeredo123")
        time.sleep(1)  # Aguardar um tempo para garantir que a ação seja registrada

        # Clicar no botão "entrar"
        login_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "login-modal-submit"))
        )
        login_button.click()
        time.sleep(5)  # Aguardar um tempo para garantir que a ação seja registrada

    except Exception as e:
        print(f"Erro ao realizar login: {e}")

# Listas para armazenar odds e times já selecionados
selected_odds = []
selected_teams = []
processed_containers = []

# Valor inicial da aposta
initial_bet = 1.0
current_bet = initial_bet

def select_total_de_gols_odd(event_container):
    try:
        # Clicar para entrar no container
        event_container.click()
        time.sleep(10)  # Esperar 10 segundos

        # Encontrar todos os elementos "market-layout-card__row"
        row_elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, ".//div[contains(@class, 'market-layout-card__row')]"))
        )
        for row_element in row_elements:
            try:
                # Verificar se o elemento contém o número 4.5
                specifier = row_element.find_element(By.XPATH, ".//div[contains(@class, 'market-layout-card__row-specifier')]/div")
                if "4.5" in specifier.text:
                    # Encontrar todas as odds dentro do mesmo `market-layout-card__row`
                    odd_containers = row_element.find_elements(By.XPATH, ".//div[contains(@class, 'market-layout-card__odd-container')]")
                    for odd_container in odd_containers:
                        odd_value_element = odd_container.find_element(By.XPATH, ".//span[contains(@class, 'odd-button__odd-value-new')]")
                        odd_value = float(odd_value_element.text.strip())
                        if 1.20 <= odd_value <= 1.70:
                            odd_container.click()
                            print(f"Odd {odd_value} selecionada")
                            time.sleep(1)
                            return odd_value  # Retornar o valor da odd selecionada
            except Exception as e:
                print(f"Erro ao verificar elemento 4.5 ou selecionar odd: {e}")
                continue

    except Exception as e:
        print(f"Erro ao selecionar odd: {e}")

    return None  # Retornar None se nenhuma odd válida foi encontrada

def monitor_and_click():
    global current_bet  # Usar a variável global current_bet

    while True:
        try:
            # Voltar para a tela inicial (URL inicial) para garantir que estamos no ponto de partida correto
            driver.get(url)
            login()
            time.sleep(10)

            # Localizar todos os containers de eventos
            event_containers = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='event-row-container']"))
            )

            for index, event_container in enumerate(event_containers):
                if index in processed_containers:
                    continue  # Pular containers já processados
                
                try:
                    # Obter o nome do time
                    team_name_element = event_container.find_element(By.XPATH, ".//div[contains(@class, 'event-competitor__name')]")
                    team_name = team_name_element.text.strip()

                    if team_name in selected_teams:
                        continue  # Pular times já usados

                    # Selecionar a odd
                    odd_value = select_total_de_gols_odd(event_container)
                    if odd_value is None:
                        processed_containers.append(index)  # Adicionar container processado à lista
                        # Voltar para a tela inicial e passar para o próximo container
                        driver.get(url)
                        time.sleep(10)
                        break

                    selected_teams.append(team_name)
                    processed_containers.append(index)  # Adicionar container processado à lista

                    # Localizar o campo de entrada, limpar e inserir o valor da aposta
                    stake_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "stake-0"))
                    )
                    stake_input.clear()  # Limpar qualquer valor existente
                    stake_input.send_keys(Keys.BACKSPACE * 3)  # Apagar o valor existente
                    stake_input.send_keys(str(current_bet))  # Inserir o valor da aposta atual
                    print(f"Valor {current_bet} inserido no campo de entrada!")

                    # Atualizar o valor da próxima aposta
                    current_bet = current_bet * odd_value

                    # Esperar 3 segundos antes de clicar no botão "Fazer aposta"
                    time.sleep(3)
                    submit_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'sds-button--primary-elevation') and contains(@class, 'e2e-betslip-submit')]"))
                    )
                    submit_button.click()
                    print("Botão 'Fazer aposta' clicado!")

                    # Esperar 12 segundos antes de atualizar a página
                    time.sleep(12)
                    driver.refresh()
                    print("Página recarregada com F5!")
                    time.sleep(3)

                    # Voltar para a tela inicial após finalizar a aposta
                    driver.get(url)
                    time.sleep(10)
                    break  # Sair do loop dos containers para retornar à tela inicial

                except Exception as e:
                    print(f"Erro ao processar container de evento: {e}")
                    # Voltar para a tela inicial se houver um erro ao processar o container
                    driver.get(url)
                    time.sleep(10)
                    continue  # Tentar novamente se houver um erro

        except Exception as e:
            print(f"Erro ao localizar containers de eventos: {e}")
            driver.refresh()
            time.sleep(10)
            continue  # Tentar novamente se houver um erro

        # Esperar 30 minutos antes de fazer a próxima aposta
        total_time = 20 #30 * 60  # 30 minutos em segundos
        for remaining in range(total_time, 0, -1):
            mins, secs = divmod(remaining, 60)
            timer = f"{mins:02d}:{secs:02d}"
            print(f"\rTempo restante: {timer}", end="")
            time.sleep(1)
        print("\nTempo de espera concluído, atualizando a página...")

        driver.refresh()
        print("Página recarregada!")
        time.sleep(4)

if __name__ == "__main__":
    login()  # Realizar login primeiro
    monitor_and_click()

# Fechar o navegador
driver.quit()
