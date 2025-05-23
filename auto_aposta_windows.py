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
import os

# Configuração do WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")  # Deixa o Selenium mais "invisível"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 60)  # Aumentei de 30 para 60 segundos

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Função para capturar screenshot ao errar
def take_screenshot(name="error"):
    try:
        driver.save_screenshot(f"{name}.png")
        logger.info(f"Screenshot salvo como {name}.png")
    except Exception as e:
        logger.error(f"Erro ao tirar screenshot: {e}")

# URL do site
url = 'https://superbet.com/pt-br/sport-bets/football/today'

def accept_cookies():
    try:
        accept_cookies_button = wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_cookies_button.click()
        logger.info("Cookies aceitos.")
    except Exception as e:
        logger.error(f"Erro ao aceitar cookies: {e}")
        take_screenshot("accept_cookies_error")

def login():
    try:
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'capitalize') and text()='entrar']"))
        ).click()

        username = os.getenv("SUPERBET_USERNAME", "bazeredo")
        password = os.getenv("SUPERBET_PASSWORD", "Bazeredo123-")

        username_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='sds-base-input__input']"))
        )
        username_input.send_keys(username)

        password_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='sds-base-input__input' and @type='password']"))
        )
        password_input.send_keys(password)

        login_button = wait.until(
            EC.element_to_be_clickable((By.ID, "login-modal-submit"))
        )
        login_button.click()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        logger.info("Login realizado com sucesso.")
    except Exception as e:
        logger.error(f"Erro no login: {e}")
        take_screenshot("login_error")

def capture_event_links():
    try:
        event_containers = wait.until(
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
        links = list(set(links))
        logger.info(f"Capturados {len(links)} links de eventos.")
        return links
    except Exception as e:
        logger.error(f"Erro ao capturar links de eventos: {e}")
        take_screenshot("capture_links_error")
        return []

def access_random_event_link(links):
    if not links:
        logger.warning("Nenhum link disponível.")
        return
    try:
        random_link = random.choice(links)
        driver.get(random_link)
        logger.info(f"Acessando evento: {random_link}")

        wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/aside/div[2]/div[3]/button[2]"))
        ).click()
        logger.info("Botão inicial clicado.")
    except Exception as e:
        logger.error(f"Erro ao acessar evento: {e}")
        take_screenshot("access_random_event_error")

def click_target_element():
    try:
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[4]/main/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/button"))
        ).click()
        logger.info("Primeiro elemento clicado.")
    except Exception as e:
        logger.error(f"Erro ao clicar no primeiro elemento: {e}")
        take_screenshot("click_target_element_error")

def click_element_in_div():
    try:
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/main/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[3]/div[1]/div[2]/div/button/div"))
        ).click()
        logger.info("Segundo botão clicado.")
    except Exception as e:
        logger.error(f"Erro no segundo botão: {e}")
        take_screenshot("click_element_in_div_error")

def click_element_based_on_condition():
    try:
        target = wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[4]/main/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div[31]/div[3]/div/div/div[1]/button/div"))
        )
        value = float(target.text.strip().replace(",", "."))

        if value <= 1.35:
            target.click()
            logger.info("Elemento clicado por condição.")
        else:
            logger.warning(f"Elemento não clicado, valor {value} maior que 1.35.")
    except Exception as e:
        logger.error(f"Erro no clique condicional: {e}")
        take_screenshot("click_element_based_on_condition_error")

def click_footer_button():
    try:
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[2]/div/aside/footer/button"))
        ).click()
        logger.info("Botão do rodapé clicado.")
    except Exception as e:
        logger.error(f"Erro ao clicar no botão do rodapé: {e}")
        take_screenshot("click_footer_button_error")

def enter_and_input_number():
    try:
        input_field = wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[2]/div/aside/footer/div/div/div/section/input"))
        )
        input_field.click()
        webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        input_field.send_keys("1")
        logger.info("Valor inserido no input.")
    except Exception as e:
        logger.error(f"Erro ao preencher valor: {e}")
        take_screenshot("enter_and_input_number_error")

def click_final_button():
    try:
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[2]/div/aside/footer/div/div/button"))
        ).click()
        logger.info("Botão final clicado.")
    except Exception as e:
        logger.error(f"Erro ao clicar no botão final: {e}")
        take_screenshot("click_final_button_error")

if __name__ == "__main__":
    driver.get(url)
    accept_cookies()
    time.sleep(5)
    login()
    time.sleep(10)
    links = capture_event_links()
    time.sleep(5)
    access_random_event_link(links)
    time.sleep(5)
    click_target_element()
    time.sleep(5)
    click_element_in_div()
    time.sleep(5)
    click_element_based_on_condition()
    time.sleep(5)
    click_footer_button()
    time.sleep(5)
    enter_and_input_number()
    time.sleep(5)
    click_final_button()
    logger.info("Automação finalizada com sucesso.")
    time.sleep(5)
    driver.quit()
