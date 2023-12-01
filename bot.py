import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def fill_cpf_and_submit(browser, cpf):
    """Preenche o CPF e envia o formulário."""

    # Encontra o campo de input com o ID "identificador-otp"
    cpf_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "identificador-otp"))
    )

    # Preenche o campo de input com o CPF
    cpf_input.send_keys(cpf)

    # Encontra e clica no botão "Entrar"
    entrar_button = browser.find_element(By.ID, "envia-identificador-otp")
    entrar_button.click()

def fill_birthdate_and_submit(browser, birthdate):
    """Preenche a data de nascimento e envia o formulário."""

    # Aguarda até que o campo de input "senha-identificador" seja clicável
    birthdate_input = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "senha-identificador"))
    )

    # Preenche o campo de input com a data de nascimento
    birthdate_input.send_keys(birthdate)

    # Aguarda até que o botão "Entrar" seja clicável
    entrar_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "envia-identificador"))
    )

    # Encontra e clica no botão "Entrar"
    entrar_button.click()

def login(cpf, birthdate, url):
    """Faz o login em um site com as credenciais fornecidas."""

    # Inicializa o navegador
    browser = webdriver.Chrome()

    # Vai para a página de login
    browser.get(url)

    # Aguarda até que o botão "Continuar no site" seja clicável
    continue_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-default"))
    )

    # Encontra e clica no botão de login
    continue_button.click()

    # Aguarda até que o elemento com a classe "jconfirm-box" desapareça
    wait_for_disappearance = WebDriverWait(browser, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "jconfirm-box"))
    )

    # Aguarda até que o elemento com a classe "lgpd_content" seja visível
    lgpd_content = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "lgpd_content"))
    )

    # Encontra o checkbox e marca
    checkbox = lgpd_content.find_element(By.ID, "aviso_aceite")
    checkbox.click()

    # Encontra e clica no botão "Enviar"
    enviar_button = lgpd_content.find_element(By.ID, "lgpd_accept")
    enviar_button.click()

    # Preenche o CPF no formulário
    fill_cpf_and_submit(browser, cpf)

    # Aguarda 20 segundos
    time.sleep(20)

    # Preenche a data de nascimento e envia o formulário
    fill_birthdate_and_submit(browser, birthdate)

    # Aguarda 60 segundos
    time.sleep(10)

    return browser

def get_data(browser):
    """Pega dados do site."""

    # Encontra o elemento que contém os dados
    data_element = browser.find_element_by_id("data")

    # Extrai os dados do elemento
    soup = BeautifulSoup(data_element.get_attribute("innerHTML"), "html.parser")
    data = soup.find_all("div", class_="data")

    return data

if __name__ == "__main__":
    cpf = "###########"  # Adjust with your CPF 11 unmasked characters
    birthdate = "DD/MM/YYYY"  # Adjust with your birthdate in the format dia/mes/ano
    url = "https://pi.equatorialenergia.com.br"  # Adjust with the actual website URL
    states = ["ma", "pa", "pi", "al"];
    # Faz o login
    browser = login(cpf, birthdate, url)

    # Pega os dados
    data = get_data(browser)

    # Imprime os dados
    for item in data:
        print(item.text)
