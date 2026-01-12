
import logging
import psutil
import sys
import time
import os

lista_processo = {}

def main():
    limpa_tela()
    processo = escolher_programa()
    config_loggin()
    listar_processo(processo)
    validar_processo(processo)  

def escolher_programa():
    logger = logging.getLogger('monitoramento_processos')

    try:
        processo = input('Digite o nome do processo: ')
        return processo
    
    except KeyboardInterrupt:
        logger.warning('\nO usuário interrompeu o programa (CRTL+C).')
        sys.exit(0)

def listar_processo(processo):
    ram = 0

    for x in psutil.process_iter(['pid','name']):
        uso = psutil.Process(x.info['pid'])
        if processo == x.info['name']:
            ram += uso.memory_percent()

    for x in psutil.process_iter(['pid','name']):
        lista_processo.clear()
        uso = psutil.Process(x.info['pid'])
        if processo.lower() == x.info['name'].lower():
            pid = x.info['pid']
            name = x.info['name']
            lista_processo['proc'] = {
                'name': processo,
                'pid': pid,
                'ram': round(ram, 2)
            }
            return lista_processo
            break

def consultar_processo_ativo(processo):
    logger = logging.getLogger('monitoramento_processos')
    trava_loop = True
    try:

        while trava_loop:
            if processo in lista_processo.get('proc', {}).get('name',{}):
                logger.info(f'O processo {processo} continua ativo.')
                time.sleep(10)
                listar_processo(processo) 
            else:
                logger.info(f'O processo {processo} foi finalizado. Validando novamente...')
                time.sleep(10)
                listar_processo(processo)
                trava_loop = False
                validar_processo(processo)

    except KeyboardInterrupt:
        logger.warning('O usuário interrompeu o programa (CRTL+C).')
        sys.exit(0)

def validar_processo(processo):
    logger = logging.getLogger('monitoramento_processos')
    trava_loop = True
    try:

        while trava_loop:
            if processo in lista_processo.get('proc',{}).get('name', {}):
                logger.info(f'O processo {processo} está ativo no PID {lista_processo['proc']['pid']} com o consumo de {lista_processo['proc']['ram']} Mb de RAM.')
                trava_loop = False
                time.sleep(10)
                consultar_processo_ativo(processo)
            
            else:
                logger.info(f'O processo {processo} não foi encontrado. Procurando novamente em 10 segundos.')
                time.sleep(10)
                listar_processo(processo)
    
    except KeyboardInterrupt:
        logger.warning('O usuário interrompeu o programa (CRTL+C).')
        sys.exit(0)

def config_loggin():
    logger = logging.getLogger('monitoramento_processos')
    logger.setLevel(logging.INFO)

    logging.basicConfig(
        filename='app.log',
        filemode='a',
        format='[%(levelname)s] - %(asctime)s - %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        level=logging.INFO,
        encoding='utf-8'
    )

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(levelname)s] - %(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

    handler.setFormatter(formatter)

    logger.addHandler(handler)

def limpa_tela():
    return os.system('cls') if os.name == 'nt' else os.system('clear')

main()