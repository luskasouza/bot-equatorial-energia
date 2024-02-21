import time
import random  # Importe a biblioteca random para gerar pausas aleatórias
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fill_cpf_and_submit(browser, cpf):
    """Preenche o CPF e envia o formulário."""
    cpf_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "identificador-otp"))
    )
    cpf_input.send_keys(cpf)
    entrar_button = browser.find_element(By.ID, "envia-identificador-otp")
    entrar_button.click()

def fill_birthdate_and_submit(browser, birthdate):
    """Preenche a data de nascimento e envia o formulário."""
    birthdate_input = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "senha-identificador"))
    )
    birthdate_input.send_keys(birthdate)
    entrar_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "envia-identificador"))
    )
    entrar_button.click()

def login(cpf, birthdate, url):
    """Faz o login em um site com as credenciais fornecidas."""
    # Inicializa as opções do navegador Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # Desativa a aceleração de hardware
    options.add_argument("--disable-software-rasterizer")  # Desativa o rasterizador de software
    options.add_argument("--disable-web-security")  # Desativa a segurança da web para permitir CORS
    options.add_argument("--allow-running-insecure-content")  # Permite a execução de conteúdo inseguro
    options.add_argument("--ignore-certificate-errors")  # Ignora erros de certificado SSL
    options.add_argument("--disable-dev-tools")  # Impede a abertura automática das DevTools
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")  # Modifica o user-agent

    browser = webdriver.Chrome(options=options)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
        """
    })
    browser.get(url)
    continue_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-default"))
    )
    continue_button.click()
    WebDriverWait(browser, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "jconfirm-box"))
    )
    lgpd_content = WebDriverWait(browser, 70).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "lgpd_content"))
    )
    checkbox = lgpd_content.find_element(By.ID, "aviso_aceite")
    checkbox.click()
    enviar_button = lgpd_content.find_element(By.ID, "lgpd_accept")
    enviar_button.click()
    fill_cpf_and_submit(browser, cpf)
    # Adicione uma pausa aleatória entre 1 e 3 segundos
    time.sleep(random.uniform(1, 3))
    fill_birthdate_and_submit(browser, birthdate)
    # Adicione uma pausa aleatória entre 2 e 5 segundos
    time.sleep(random.uniform(2, 5))
    return browser

def get_data(browser):
    """Pega dados do site após a próxima tela ser carregada.""" 
    # Espera até que a nova página seja carregada
    time.sleep(10)
    
if __name__ == "__main__":
    cpf = "0000000000"  # Ajuste com seu CPF de 11 caracteres não mascarados
    birthdate = "00/00/00000"  # Ajuste com sua data de nascimento no formato dia/mês/ano
    url = "https://pi.equatorialenergia.com.br"  # Ajuste com a URL real do site

    # Faz o login
    browser = login(cpf, birthdate, url)
    # Obtém os dados
    get_data(browser)
