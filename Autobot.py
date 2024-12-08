from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Configuração para o modo headless
chrome_options = Options()
chrome_options.add_argument('--headless')

# Use o ChromeDriverManager para obter automaticamente a versão compatível
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

driver.get('https://blaze-4.com/pt/games/double')

# Mensagens Padrao
analise = ' '
win = '💵💵Vitoria💵💵'
win_branco = '💰💰⬜ Vitoria No branco ⬜💰💰'
loss = '📛Essa não deu!📛\n📛Tenha atençao com a Banca!📛'
nao_confirmacao = ' '


def esperar():
    # Vamos esperar até que o tempo seja atualizado
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'time-left')))

def retornar_historico():
    return [i['color'] for i in requests.get('https://blaze-4.com/api/roulette_games/recent').json()][::-1]

def retornar_ultimo():
    return requests.get('https://blaze-4.com/api/roulette_games/current').json()['color']

def martin_gale(gale, ultimo):
    enviar_mensagem(gale)
    esperar()
    sleep(1.5)
    ultimo_ = retornar_ultimo()
    if ultimo_ != ultimo and ultimo_ != 0:
        enviar_mensagem(win)
        return True
    elif ultimo_ == 0:
        enviar_mensagem(win_branco)
        return True

def enviar_mensagem(mensagem):
    bot_token = '6209018754:AAFPJUg-rVTMA8y3e2n7yLT5TIuFEXFiIjo'
    chat_id = '-1001965428039'
    url_blaze = ''
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={mensagem}\n{url_blaze}&parse_mode=Markdown'
    requests.get(url)

cor = ['Branco', 'Preto', 'Vermelho']
simbolo = ['⬜', '⬛', '🟥']

print('Bot Grupo de sinais iniciado ...')
enviar_mensagem('🤖🤖 BLazerWinner sinais iniciado 🤖🤖')
while True:
    try:
        print('ok')
        esperar()
        sleep(1.5)
        historico = retornar_historico()
        ultimo = retornar_ultimo()
        historico.append(ultimo)
        padrao = historico[-2:]
        print(padrao)
        confirmacao = f'{simbolo[padrao[0]]} Entrada confirmada no {cor[padrao[0]]}\n{simbolo[0]} E no branco'
        gale1 = f'Entre gale 1 \n{simbolo[padrao[0]]} {cor[padrao[0]]}\n{simbolo[0]} E no Branco'
        gale2 = f'Entre gale 2 \n{simbolo[padrao[0]]} {cor[padrao[0]]}\n{simbolo[0]} E no Branco'
        
        # Como as estratégias sempre jogam na cor contrária, resolvi colocar as cores
        # Vermelha e Preta em índices diferentes para aproveitar a lógica
        if padrao == [1,1] or padrao == [2,2] or padrao == [1,2] or padrao == [2,1]:                
            enviar_mensagem(analise)
            esperar()
            sleep(1.5)
            ultimo = retornar_ultimo()
            while True:
                if ultimo == padrao[0]:
                    enviar_mensagem(confirmacao)
                    esperar()
                    sleep(1.5)
                    ultimo_ = retornar_ultimo()
                    if ultimo_ != ultimo and ultimo_ != 0:
                        enviar_mensagem(win)
                        break
                    elif ultimo_ == 0:
                        enviar_mensagem(win_branco)
                        break
                    else:
                        if martin_gale(gale1,ultimo):
                            break
                        else:
                            if martin_gale(gale2,ultimo):
                                break
                            else:
                                enviar_mensagem(loss)
                                break
                else:
                    enviar_mensagem(nao_confirmacao)
                    break
    except Exception as e:
        print(e)
        driver.get('https://blaze-4.com/pt/games/double')
        sleep(10)
        pass
