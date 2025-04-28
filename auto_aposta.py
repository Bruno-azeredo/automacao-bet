from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import logging
import os  # Para pegar variáveis de ambiente

# Configuração do WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless=new")  # Novo modo headless
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# URL do site
url = 'https://superbet.bet.br/apostas/ao-vivo'

def accept_cookies():
    try:
        accept_cookies_button = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_cookies_button.click()
        logger.info("Cookies aceitos.")
    except Exception as e:
        logger.error(f"Erro ao aceitar cookies: {e}")

def login():
    try:
        WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'capitalize') and text()='entrar']"))
        ).click()

        username = os.getenv("SUPERBET_USERNAME", "bazeredo")  # Pega usuário da variável de ambiente
        password = os.getenv("SUPERBET_PASSWORD", "Bazeredo123-")  # Mesma coisa para a senha

        username_input = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='sds-base-input__input']"))
        )
        username_input.send_keys(username)

        password_input = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='sds-base-input__input' and @type='password']"))
        )
        password_input.send_keys(password)

        login_button = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.ID, "login-modal-submit"))
        )
        login_button.click()

        # Fecha popups se aparecer
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        logger.info("Login realizado com sucesso.")
    except Exception as e:
        logger.error(f"Erro no login: {e}")

def print_page_source():
    # Imprime o HTML completo da página
    page_source = driver.page_source
    logger.info("HTML da página carregada:")
    logger.info(page_source)  # Isso imprimirá o código HTML da página carregada

def capture_event_links():
    try:
        event_containers = WebDriverWait(driver, 50).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'event-row-container')]"))
        )
        links = []
        for container in event_containers:
            try:
                link = container.find_element(By.XPATH, ".//a[contains(@class, 'bet-builder-event-card-link')]").get_attribute("href")
                if link:
                    links.append(link)
            except Exception:
                pass
        links = list(set(links))  # Remove duplicados
        logger.info(f"Capturados {len(links)} links de eventos.")
        return links
    except Exception as e:
        logger.error(f"Erro ao capturar links de eventos: {e}")
        return []

def access_random_event_link(links):
    if not links:
        logger.warning("Nenhum link disponível.")
        return
    try:
        random_link = random.choice(links)
        driver.get(random_link)
        logger.info(f"Acessando evento: {random_link}")

        WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/aside/div[2]/div[3]/button[2]"))
        ).click()
        logger.info("Botão inicial clicado.")
    except Exception as e:
        logger.error(f"Erro ao acessar evento: {e}")

def click_target_element():
    try:
        WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[4]/main/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/button"))
        ).click()
        logger.info("Primeiro elemento clicado.")
    except Exception as e:
        logger.error(f"Erro ao clicar no primeiro elemento: {e}")

def click_element_in_div():
    try:
        WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/main/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div[1]/div[2]/div/button/div"))
        ).click()
        logger.info("Segundo botão clicado.")
    except Exception as e:
        logger.error(f"Erro no segundo botão: {e}")

def click_element_based_on_condition():
    try:
        target = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[4]/main/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div[31]/div[3]/div/div/div[1]/button/div"))
        )
        value = float(target.text.strip().replace(",", "."))  # Corrigir caso seja vírgula

        if value <= 1.15:
            target.click()
            logger.info("Elemento clicado por condição.")
        else:
            logger.warning(f"Elemento não clicado, valor {value} maior que 1.15.")
    except Exception as e:
        logger.error(f"Erro no clique condicional: {e}")

def click_footer_button():
    try:
        WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[2]/div/aside/footer/button"))
        ).click()
        logger.info("Botão do rodapé clicado.")
    except Exception as e:
        logger.error(f"Erro ao clicar no botão do rodapé: {e}")

def enter_and_input_number():
    try:
        input_field = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[2]/div/aside/footer/div/div/div/section/input"))
        )
        input_field.click()
        webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        input_field.send_keys("1")
        logger.info("Valor inserido no input.")
    except Exception as e:
        logger.error(f"Erro ao preencher valor: {e}")

def click_final_button():
    try:
        WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[2]/div/aside/footer/div/div/button"))
        ).click()
        logger.info("Botão final clicado.")
    except Exception as e:
        logger.error(f"Erro ao clicar no botão final: {e}")

if __name__ == "__main__":
    driver.get(url)
    accept_cookies()
    print_page_source()  # Imprime o HTML após carregar a página
    login()
    links = capture_event_links()
    access_random_event_link(links)
    click_target_element()
    click_element_in_div()
    click_element_based_on_condition()
    click_footer_button()
    enter_and_input_number()
    click_final_button()
    logger.info("Automação finalizada com sucesso.")
    time.sleep(5)
    driver.quit()
