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
url = 'https://superbet.com/pt-br/sport-bets/live'
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

# Valor inicial da aposta
initial_bet = 1
current_bet = initial_bet

def select_resultado_final_and_chance_dupla():
    print('voltamos aqui')
    time.sleep(10)

    try:
        # Encontrar todos os botões "Resultado Final"
        resultado_final_buttons = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'market-filters')]"))
        )
        for button in resultado_final_buttons:
            try:
                # Verificar se o botão contém o texto "Resultado Final"
                span_text = button.find_element(By.XPATH, ".//span").text
                if "Resultado Final" in span_text:
                    button.click()
                    time.sleep(3)  # Aguardar um tempo para garantir que a ação seja registrada

                    # Tentar encontrar "Empate Anula Aposta"
                    try:
                        empate_anula_aposta_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'selection-row__title') and text()='Escanteios 1X2']"))
                        )
                        empate_anula_aposta_element.click()
                        time.sleep(3)
                    except:
                        # Tentar encontrar "Chance Dupla"
                        try:
                            chance_dupla_element = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'selection-row__title') and text()='3º Falta']"))
                            )
                            chance_dupla_element.click()
                            time.sleep(3)
                        except:
                            # Tentar encontrar "Total de Gols"
                            try:
                                total_gols_element = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'selection-row__title') and text()='Total de Gols']"))
                                )
                                total_gols_element.click()
                                time.sleep(3)
                            except:
                                try:
                                    chance_dupla_element = WebDriverWait(driver, 5).until(
                                        EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'selection-row__title') and text()='3º Quarto - Total de Pontos']"))
                                    )
                                    chance_dupla_element.click()
                                    time.sleep(3)
                                except Exception as e:
                                    print(f"Erro ao localizar 'Empate Anula Aposta', 'Chance Dupla' ou 'Total de Gols': {e}")
                                    # Pressionar a tecla "Esc" caso não encontre nenhum dos elementos
                                    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                                    time.sleep(3)
            except Exception as e:
                print(f"Erro ao clicar em 'Resultado Final': {e}")
    except Exception as e:
        print(f"Erro ao localizar botões 'Resultado Final': {e}")

def monitor_and_click():
    global current_bet  # Usar a variável global current_bet
    time.sleep(10)
    select_resultado_final_and_chance_dupla()  # Realizar seleção antes de procurar odds

    try:
        # Localizar todos os containers de eventos
        time.sleep(20)
        event_containers = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='event-row-container']"))
        )
    except Exception as e:
        print(f"Erro ao localizar containers de eventos: {e}")
        driver.refresh()
        time.sleep(20)
        return  # Encerrar a execução se houver erro

    for event_container in event_containers:
        try:
            # Obter o nome do time
            team_name_element = event_container.find_element(By.XPATH, ".//div[contains(@class, 'event-competitor__name')]")
            team_name = team_name_element.text.strip()

            if team_name in selected_teams:
                continue  # Pular times já usados

            # Localizar todos os botões de odds dentro do container do evento
            odd_buttons = event_container.find_elements(By.XPATH, ".//button[contains(@class, 'odd-button')]")

            # Adicionar um índice para controle dentro do loop de botões de odd
            for index, button in enumerate(odd_buttons):
                try:
                    # Verificar se o botão ainda está presente e visível
                    if button.is_displayed():
                        # Obter o valor da odd
                        odd_value_element = button.find_element(By.XPATH, ".//span[contains(@class, 'odd-button__odd-value-new')]")
                        odds_value = float(odd_value_element.text.strip())

                        if 1.10 <= odds_value <= 1.90:
                            selected_teams.append(team_name)
                            
                            button.click()
                            print(f"Botão com valor {odds_value} e time {team_name} clicado!")

                            # Esperar 10 segundos após o clique
                            time.sleep(10)

                            # Localizar o campo de entrada, limpar e inserir o valor da aposta
                            stake_input = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.ID, "stake-0"))
                            )
                            stake_input.clear()  # Limpar qualquer valor existente
                            stake_input.send_keys(Keys.BACKSPACE * 3)  # Apagar o valor existente
                            stake_input.send_keys(str(current_bet))  # Inserir o valor da aposta atual
                            print(f"Valor {current_bet} inserido no campo de entrada!")

                            # Atualizar o valor da próxima aposta
                            current_bet = current_bet * odds_value

                            # Esperar 3 segundos antes de clicar no botão "Fazer aposta"
                            time.sleep(5)
                            submit_button = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'sds-button--primary-elevation') and contains(@class, 'e2e-betslip-submit')]"))
                            )
                            submit_button.click()
                            print("Botão 'Fazer aposta' clicado!")

                            # Esperar 12 segundos antes de atualizar a página
                            time.sleep(15)
                            driver.refresh()
                            print("Página recarregada com F5!")
                            time.sleep(3)

                            break  # Sair do loop após selecionar e apostar em uma odd

                except Exception as e:
                    print(f"Erro ao processar botão de odd {index}: {e}")

        except Exception as e:
            print(f"Erro ao processar container de evento: {e}")

    # Esperar 30 minutos antes de fazer a próxima aposta
    total_time = 10 * 60  # 30 minutos em segundos
    for remaining in range(total_time, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"\rTempo restante: {timer}", end="")
        time.sleep(5)
    print("\nTempo de espera concluído, atualizando a página...")

    driver.refresh()
    print("Página recarregada!")
    time.sleep(4)

    monitor_and_click()  # Repetir o processo

if __name__ == "__main__":
    login()  # Realizar login primeiro
    monitor_and_click()

# Fechar o navegador
driver.quit()