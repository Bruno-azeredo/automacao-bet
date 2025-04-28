from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar sem interface gráfica
chrome_options.add_argument("--no-sandbox")  # Evitar problemas de permissões
chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar problemas de memória compartilhada

service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.google.com")  # Teste de navegação
print(driver.title)
driver.quit()



