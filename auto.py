from selenium import webdriver
from datetime import datetime, timedelta
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import json
#usuario
user = ''
#Senha
senha = ''
valor_cor = 0.10 # valor que ele vai apostar no preto ou vermelho
banca = 0.36 # Inic2ializa a variável de banca
valor_white = 0 # valor que ele vai entrar no branco
stopwin = 500
stoploss = 0
reiniciar = 0.10 # valor que ele vai inicial sempre que uma rodada for iniciada
  
max_tentativas_martingale = 0 # aqui vc escolhe quantos martigales vc quer fazer 

def login_to_blaze(driver, user, senha):
    isCaptcha = True
    driver.get("https://blaze.com/pt/")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='unauthed-buttons']//div[1]")))
    driver.find_element(By.XPATH, "//div[@class='unauthed-buttons']//div").click()
    time.sleep(1)
    login_box = driver.find_element(By.XPATH, "//input[@name='username']")
    login_box.send_keys(user)
    senha_box = driver.find_element(By.XPATH, "(//input[@name='password'])")
    senha_box.send_keys(senha)
    time.sleep(1)
    driver.find_element(By.XPATH, "(//button[normalize-space()='Entrar'])").click()
    time.sleep(3)

def goto_double_page(driver):
    driver.get("https://blaze.com/pt/games/double")

def esperar(driver):
    while True:
        try:
            driver.find_element(By.CLASS_NAME, 'time-left').find_element(By.TAG_NAME, 'span').text
            break
        except:
            pass

    while True:
        try:
            driver.find_element(By.CLASS_NAME, 'time-left').find_element(By.TAG_NAME, 'span').text
        except:
            break

def retornar_historico():
    return [i['color'] for i in requests.get('https://blaze.com/api/roulette_games/recent').json()][::-1]

def retornar_ultimo():
    return requests.get('https://blaze.com/api/roulette_games/current').json()['color']

def fazer_aposta(driver, padrao, valor):
    time.sleep(7)  # Aguarda 6 segundos antes de fazer a aposta

    if padrao == [1, 1] or padrao == [2, 2] or padrao == [2, 1] or padrao == [1, 2] or padrao == [1, 0]:
        cor_oposta = determinar_cor_oposta(padrao)
        if cor_oposta is not None:
            print("Hora de fazer entrada")
            make_bet(driver, valor, cor_oposta)
            time.sleep(1)
            make_bet(driver, valor_white, "white")
        else:
            print("Não foi possível determinar a cor oposta.")

def determinar_cor_oposta(padrao):
    cor_caiu = padrao[-1]
    if cor_caiu == 1:
        return "black"
    elif cor_caiu == 2:
        return "red"
    else:
        return None

def make_bet(driver, quantia, cor=None):
    quantia_input = driver.find_element(By.XPATH, "//input[@type='number']")
    quantia_input.clear()
    quantia_input.send_keys(str(quantia))

    if cor:
        cor_options = driver.find_elements(By.XPATH, f"//div[@class='input-wrapper select']//div[contains(@class, '{cor.lower()}')]")
        for option in cor_options:
            option.click()
            break

    wait = WebDriverWait(driver, 8)
    comecar_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Começar o jogo']")))
    comecar_button.click()

def get_last_result_double():
    today, yesterday = today_date()
    cur_time = get_current_time_hours()
    results = []
    try:
        url = f"https://blaze.com/api/roulette_games/history?startDate={yesterday}T{cur_time}.000Z&endDate={today}T{cur_time}.000Z&page=1"
        r = requests.get(url)
        data = json.loads(r.text)
        for i, v in enumerate(data["records"]):
            val = v["color"]
            if i < 2:
                results.append(val)
        if estrategia(results) < 2:
            return True
        return False
    except (ValueError) as e:
        print("Erro ao obter os resultados do histórico:", e)
        return False

# Função para obter o valor da banca em tempo real
def get_banca(driver):
    try:
        # Esperar até que o elemento da banca seja visível
        wait = WebDriverWait(driver, 12)
        banca_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "wallet")))

        # Obter o texto do elemento da banca
        banca_text = banca_element.text.strip()

        # Extrair o valor da banca (removendo o símbolo 'R$' e convertendo para float)
        valor_banca = float(banca_text.split()[-1].replace('R$', '').replace(',', '.'))

        return valor_banca

    except Exception as e:
        print("Erro ao obter valor da banca:", e)
        return None

def get_current_time_hours():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def today_date():
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    return today.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d")

def estrategia(result_array):
    color_count = 0
    last = None
    for color in result_array:
        if last is None:
            last = color
        if color == last:
            color_count += 1
        else:
            return color_count
    return color_count

def check_stop_conditions(banca):
    if banca >= stopwin:
        print("Stop win atingido! Encerrando o script.")
        return True
    elif banca <= stoploss:
        print("Stop loss atingido! Encerrando o script.")
        return True
    return False

def retornar_cor(numero):
    if numero == 1:
        return "red"
    elif numero == 2:
        return "black"

if __name__ == "__main__":
    try:
        driver = webdriver.Chrome()
        login_to_blaze(driver, user, senha)
        goto_double_page(driver)

        wins = 0  # Contador de wins
        loss = 0  # Contador de loss
        num_apostas = 0  # Contador de apostas

        while True:
            esperar(driver)
            historico = retornar_historico()
            ultimo = retornar_ultimo()
            historico.append(ultimo)
            padrao = historico[-2:]
            print(padrao)

            fazer_aposta(driver, padrao, valor_cor)

            # Aguardar próximo roll
            time.sleep(17)

            # Obter o valor atual da banca
            banca = get_banca(driver)
            if banca is not None:
                print("Valor da Banca:", banca)

                # Verificar condições de stop win e stop loss
                if banca >= stopwin:
                    print("Stop win atingido! Encerrando o script.")
                    break
                elif banca <= stoploss:
                    print("Stop loss atingido! Encerrando o script.")
                    break

            cor_atual = retornar_ultimo()
            if cor_atual == padrao[1]:
                print("Loss!")

                # Estratégia de Martingale limitado a quanto voce pos tentativas
                tentativas_martingale = 0
                while tentativas_martingale < max_tentativas_martingale:
                    tentativas_martingale += 1
                    print(f"Tentativa {tentativas_martingale} de Martingale")
                    valor_cor *= 2  # Dobrar o valor da aposta
                    fazer_aposta(driver, padrao, valor_cor)

                    # Aguardar próximo roll
                    time.sleep(17)

                    cor_atual = retornar_ultimo()
                    if cor_atual == padrao[1]:
                        print("Martingale Loss!")
                    else:
                        print("Martingale Win!")
                        time.sleep(30)
                        valor_cor = reiniciar
                        wins += 1  # contador de wins
                        break

                # Verifica se a segunda tentativa de Martingale também resultou em perda
                if tentativas_martingale == max_tentativas_martingale:
                    time.sleep(60)
                    valor_cor = reiniciar

                loss += 1  # contador de loss

            else:
                print("Win")
                time.sleep(40)
                valor_cor = reiniciar
                wins += 1  #  contador de wins

            num_apostas += 1  #  contador de apostas

    except Exception as e:
        print("Ocorreu um erro:", e)
    finally:
        driver.quit()

    print("Total de wins:", wins)
    print("Total de loss:", loss)
    print("Total de apostas:", num_apostas)
