from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import actions
import os


driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com/')

time.sleep(15)

def bot():
    try:
        # PEGA A BOLINHA VERDE
        bolinha = driver.find_element_by_class_name('aumms1qt')
        bolinha = driver.find_elements_by_class_name('aumms1qt')
        clica_bolinha = bolinha[-1]
        acao_bolinha = webdriver.common.action_chains.ActionChains(driver)
        acao_bolinha.move_to_element_with_offset(clica_bolinha, 0, -20)
        acao_bolinha.click()
        acao_bolinha.perform()
        acao_bolinha.click()
        acao_bolinha.perform()

        # PEGA O TELEFONE DO CLIENTE
        telefone_cliente = driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div[1]/div/span')
        telefone_final = telefone_cliente.text

        # PEGA A MENSAGEM DO CLIENTE
        todas_as_msg = driver.find_elements_by_class_name('_1Gy50')
        todas_as_msg_texto = [e.text for e in todas_as_msg]
        msg = todas_as_msg_texto[-1]

        # REGISTRANDO CAMPO DE TEXTO
        campo_de_texto = driver.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')

        # RESPONDENDO
        actions.Decision(telefone_final, msg, campo_de_texto).reply()

        # VOLTAR PARA O CONTATO PADRÃO
        try:
            contato_padrao = driver.find_element_by_class_name('_2XH9R')
            acao_contato = webdriver.common.action_chains.ActionChains(driver)
            acao_contato.move_to_element_with_offset(contato_padrao, 0, -20)
            acao_contato.click()
            acao_contato.perform()
            acao_contato.click()
            acao_contato.perform()
        except:
            contato_padrao = driver.find_element_by_class_name('_2XH9R')
            acao_contato = webdriver.common.action_chains.ActionChains(driver)
            acao_contato.move_to_element_with_offset(contato_padrao, 0, -20)
            acao_contato.click()
            acao_contato.perform()
            acao_contato.click()
            acao_contato.perform()

        # CASO TIVER ALGUM CHAMADO FINALIZADO, ENVIARÁ MENSAGEM AO GRUPO!
        try:
            open("group.txt")
            with open('group.txt', 'r') as file:
                ler = file.read()
            file.close()
            time.sleep(0.5)
            campo_grupo = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')
            campo_grupo.click()
            campo_grupo.send_keys(ler, Keys.ENTER)
            os.remove('group.txt')
        except:
            pass

    except:
        time.sleep(1)

while True:
    bot()

