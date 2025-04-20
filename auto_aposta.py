from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random  # Biblioteca para escolha aleatória
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Configuração do WebDriver com webdriver-manager
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL do site
url = 'https://superbet.com/pt-br/sport-bets/football/today'

def accept_cookies():
    try:
        # Clicar no botão "Aceitar todos os cookies"
        accept_cookies_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_cookies_button.click()
        logger.info("Clicou no botão 'Aceitar todos os cookies'")
        time.sleep(3)  # Aguardar mais 3 segundos após clicar no botão
    except Exception as e:
        logger.error(f"Erro ao clicar no botão 'Aceitar todos os cookies': {e}")

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
            EC.presence_of_element_located((By.XPATH, "//input[@class='sds-base-input__input']"))
        )
        username_input.send_keys("bazeredo")
        time.sleep(1)

        # Digitar a senha no campo de entrada
        password_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='sds-base-input__input' and @type='password']"))
        )
        password_input.send_keys("Bazeredo123-")
        time.sleep(1)

        # Clicar no botão "entrar"
        login_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "login-modal-submit"))
        )
        login_button.click()
        time.sleep(5)

        # Pressionar ESC para fechar quaisquer pop-ups
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        # Clicar no botão "+3h"
        #plus_3h_button = WebDriverWait(driver, 30).until(
        #    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'sds-filter-bar-item sds-focus sds-filter-bar-item--brand') and contains(text(), '+3h')]"))
        #)
        #plus_3h_button.click()
        #time.sleep(3)
    except Exception as e:
        logger.error(f"Erro ao realizar login ou clicar no botão '+3h': {e}")

# Função para capturar links de eventos
def capture_event_links():
    time.sleep(10)  # Garantir que a página esteja totalmente carregada
    try:
        # Localizar todos os containers de eventos
        event_containers = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'event-row-container')]"))
        )

        event_links = []
        for event_container in event_containers:
            try:
                # Localizar o link dentro do container de evento
                link_element = event_container.find_element(By.XPATH, ".//a[contains(@class, 'bet-builder-event-card-link')]")
                link = link_element.get_attribute("href")
                event_links.append(link)
                logger.info(f"Link capturado: {link}")
            except Exception as e:
                logger.error(f"Erro ao capturar link no container de evento: {e}")

        # Remover links duplicados
        unique_event_links = list(set(event_links))
        logger.info(f"Total de links únicos capturados: {len(unique_event_links)}")
        return unique_event_links
    except Exception as e:
        logger.error(f"Erro ao localizar containers de eventos: {e}")
        return []

# Função para acessar um link aleatório (removendo duplicatas antes)
def access_random_event_link(event_links):
    if not event_links:  # Verificar se a lista de links está vazia
        logger.warning("Não há links disponíveis para acessar.")
        return
    
    try:
        # Remover duplicatas
        unique_event_links = list(set(event_links))
        logger.info(f"Total de links únicos disponíveis: {len(unique_event_links)}")

        # Escolher um link aleatório
        random_link = random.choice(unique_event_links)
        logger.info(f"Acessando o link aleatório: {random_link}")

        # Navegar para o link escolhido
        driver.get(random_link)
        time.sleep(5)  # Aguarde para garantir que a página carregue completamente
    except Exception as e:
        logger.error(f"Erro ao acessar o link: {e}")


# Função para clicar no elemento especificado após acessar o link
def click_target_element():
    time.sleep(5)
    try:
        # Esperar até que o elemento esteja presente e clicável
        target_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[4]/main/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/button"))
        )
        target_button.click()
        logger.info("Elemento clicado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao clicar no elemento: {e}")

# Função para clicar no novo elemento especificado
def click_element_in_div():
    try:
        # Esperar até que o novo elemento esteja presente e clicável
        target_element = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/main/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div[1]/div[2]/div/button/div"))
        )                                          
        target_element.click()
        logger.info("Novo elemento clicado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao clicar no novo elemento: {e}")

# Função para clicar no elemento, desde que o número seja menor ou igual a 1.10
def click_element_based_on_condition():
    try:
        # Localizar o elemento que contém o número
        target_element_value = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[4]/main/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div[31]/div[3]/div/div/div[1]/button/div"))
        )
        # Obter o texto ou valor do elemento
        value = float(target_element_value.text.strip())
        
        # Verificar a condição: número menor ou igual a 1.10
        if value <= 1.15:
            # Clicar no elemento, se a condição for satisfeita
            target_element_value.click()
            logger.info("Elemento clicado com sucesso, valor satisfaz condição!")
        else:
            logger.warning(f"Elemento não clicado. Valor ({value}) maior que 1.10.")
    except Exception as e:
        logger.error(f"Erro ao localizar ou interagir com o elemento: {e}")

# Função para clicar no botão no rodapé
def click_footer_button():
    try:
        # Esperar até que o elemento esteja presente e clicável
        footer_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[2]/div/aside/footer/button"))
        )
        footer_button.click()
        logger.info("Botão no rodapé clicado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao clicar no botão no rodapé: {e}")

# Função para entrar no elemento, selecionar tudo e digitar o número 5
def enter_and_input_number():
    try:
        # Esperar até que o elemento esteja presente
        input_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[2]/div/aside/footer/div/div/div/section/input"))
        )                                               

        # Selecionar tudo no campo usando o atalho Ctrl + A
        input_element.click()
        webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        
        # Digitar o número 5
        input_element.send_keys("5")
        logger.info("Número 5 digitado no elemento com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao interagir com o elemento e digitar o número 5: {e}")

# Função para clicar no botão após interagir com o campo anterior
def click_final_button():
    try:
        # Esperar até que o botão esteja presente e clicável
        final_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[2]/div/aside/footer/div/div/button"))
        )
        final_button.click()
        logger.info("Botão final clicado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao clicar no botão final: {e}")



if __name__ == "__main__":
    driver.get(url)
    time.sleep(5)
    accept_cookies()
    time.sleep(2)
    login()
    event_links = capture_event_links()
    access_random_event_link(event_links)
    click_target_element()  # Criar aposta
    click_element_in_div()  # Clicar no próximo botão
    click_element_based_on_condition()
    click_footer_button()
    enter_and_input_number()
    click_final_button()
    time.sleep(10)
    driver.quit()