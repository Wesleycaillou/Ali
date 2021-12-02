import speech_recognition as sp         #biblioteca de reconhecimento de voz
import pyttsx3 as pt                    #biblioteca que converte texto em voz
from random import choice               #importação do método choice() da biblioteca Random
import pandas as pd                     #biblioteca de leitura de planilhas no excel
import cv2                              #biblioteca de visão computacional
from pyzbar.pyzbar import decode        #importação do método decode() que decodifica códigos de barra ou QRCodes
import time                             #biblioteca que permite o controle e ativação de funções que dependem de tempo
import numpy as np                      #biblioteca matemática do Python
import pygame                           #biblioteca de Python para jogos, usada para a criação da interface
import sys                              #biblioteca que fornece funções e variáveis usadas para manipular diferentes partes do ambiente de tempo de execução do Python
from pygame.locals import *             #importação de arquivo local  

pygame.init()                           #início do Pygame

#Setup de Entrada - Definições ----------------------------------------------- #
mainClock = pygame.time.Clock()        
from pygame.locals import *

pygame.display.set_caption('Ali')
bg = pygame.image.load("Ali.png")
ab = pygame.image.load("Ali 2.png")
screen = pygame.display.set_mode((1320, 600),0,32)

#Definição de Fontes textuais--------------------------------------------------#
font = pygame.font.SysFont(None, 80)
fonte = pygame.font.SysFont(None, 30)
fonte1 = pygame.font.SysFont(None, 25)

#Definição de Escrita de Texto-------------------------------------------------#
def draw_text(text, font, color, surface, x, y):
    '''
    Define a função de escrita para a interface
    '''
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

#Definição de ações do Menu Inicial--------------------------------------------#

def main_menu():
    '''
    Define as ações do Menu Inicial
    '''

    while True:

        screen.fill((245, 245, 220))
        screen.blit(bg, (0,0))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(497, 450, 350, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game()

        pygame.draw.rect(screen, (38, 63, 140), button_1)

        draw_text('CLIQUE PARA INICIAR', fonte, (255, 255, 255), screen, 560, 465)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update() 
   
#Definições dos Submenus dos Botões - Game - Opções - Sair --------------------#
def game():
    '''
    Define os submenus do botões (Game, Opções, Sair)
    '''
    running = True
    while running:

        y_text = 40

        screen.fill((245, 245, 220))
        screen.blit(ab, (0,0))
        
        draw_text('ALI', font, (122, 126, 191), screen, 20, 15)

  ################# importando planilha com os dados ##################
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        pygame.display.update()
        mainClock.tick(60)

        remedy_df = pd.read_excel("Banco de Dados remédios.xlsx")
        teste_df = pd.read_excel("Pasta1.xlsx")

        ################## Inicialização da biblioteca responsável pela voz ##################

        reproducao = pt.init()

        ################## Função Responsável pela "fala" ##################

        def sai_som(resposta):
            '''
            Função responsável pela fala
            '''
            reproducao.say(resposta)
            reproducao.runAndWait()

        ################## Mensagem com informações do programa ##################

        y_text = 580
        msg = "Assistente ALI - version 1.0.0 / by: Ana, Bruna, Derick, Gustavo e Wesley"
        draw_text(msg, fonte1, (132, 112, 255), screen, 380, y_text)
        y_text = y_text+40
        pygame.display.update()

        ################## FAZER CÂMERA FUNCIONAR/fechar ##################
        cap = cv2.VideoCapture (0) #definiçãod de variável para funcionar o CV2

        #Leitura do código de QR
        def get_qr_data (input_frame):
            '''
            Função de decodificação do código QR
            '''
            try:
                return decode (input_frame)
            except:
                return[]

        #desenha um quadrado em volta
        def draw_polygon(frame_in, qrobj):
            '''
            Função que cria um quadrado delimitando, na imagem da câmera, 
            o código QR
            '''
            if len(qrobj)==0:
                return frame_in
            else: 
                for obj in qrobj:
                    text = obj.data.decode("utf-8")
                    pts = obj.polygon
                    pts = np.array([pts], np.int32)
                    pts = pts.reshape((4,1,2))
                    cv2.polylines (frame_in, [pts], True, (255, 55, 5 ), 2)
                    cv2.putText (frame_in, text, (50, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 200, 1), 2)
                    return frame_in 

        #Função responsável por retornar o valor lido do QR code
        def CameraPfvFunfa():
            '''
            Função que permite ligar a câmera e ler 
            as informações do código QR
            '''

            i = True

            while i == True:
                i, frame = cap.read ()

                qr_obj = get_qr_data (frame)
                frame = draw_polygon(frame, qr_obj)

                for code in decode(frame):
                    return int(code.data.decode("utf-8"))
                    print("Número do ítem:")

                cv2.imshow ("Leitor", frame)
                cv2.waitKey(1)

        ################## Selecionar remédio ##################

        ent = CameraPfvFunfa()#valor retornado da função lido da câmera.
        print(ent)# ver qual remédio foi selecionado

        ################### Desligar câmera ##################
        cap.release()
        cv2.destroyAllWindows()
        ################## Mensagem padrão para acessar informações do produto ##################
        y_text = 100
        
        inst = "Escolha 1 para saber o remédio, 2 para as indicações, 3 para contraindicações e 4 para cuidados ao utilizar"
        draw_text(inst, fonte1, (38, 63, 140), screen, 80, y_text)
        pygame.display.update()
        sai_som("Escolha 1 para saber o remédio, 2 para as indicações, 3 para contraindicações e 4 para cuidados ao utilizar")


        ################## Definição de listas de informações ##################

        lista_erros = [
            'Não entendi, repita',
            'Repita, por favor',
            'Desculpa, não entendi'
         ]

        conversas = {
            '1' : remedy_df.loc[ent,"Remédio/ Produto"],
            '2' : remedy_df.loc[ent,"Indicação "],
            '3' : remedy_df.loc[ent,"CONTRAINDICAÇÕES"],
            '4' : remedy_df.loc[ent,"CUIDADOS AO UTILIZAR"],
            "Olá": "Olá, tudo bem?",
            'Tudo e com você': 'Estou ótima, como posso ajudar?'
        }

        escritas = {
            '1' : teste_df.loc[ent,"numero"],
            '2' : teste_df.loc[ent,"blala"],
            '3' : teste_df.loc[ent,"bshbf"],
            '4' : teste_df.loc[ent,"behbe"]
        }

        draw_text("Ouvindo...", fonte1, (0,0,0), screen, 80, 120) #Indicação que o programa está funcionando
        pygame.display.update()

        ################## Função responsável pelo reconhecimento da mensagem falada ##################
        def reconhecer (resposta_erro_aleatorio):
            '''
            Essa função é responsável por fazer o reconhecimento 
            da solicitação do usuário por voz
            '''
            y_text = 160
            rec = sp.Recognizer()

            with sp.Microphone() as m:
                rec.adjust_for_ambient_noise(m)

                while True:
                    try:
                        audio = rec.listen(m)

                        entrada = rec.recognize_google(audio, language='pt')
                
                        resposta = conversas[entrada]
                        escrita = escritas[entrada]

                        fala = "{}".format(resposta)
                        escreve = '{}'.format(escrita)
                        draw_text(escreve, fonte1, (122, 126, 19), screen, 80, y_text)
                        y_text = y_text + 40
                        pygame.display.update()
                        sai_som(fala)

                    except sp.UnknownValueError:
                        #return resposta_erro_aleatorio
                        sai_som(resposta_erro_aleatorio)
                        draw_text(resposta_erro_aleatorio, fonte1, (122, 126, 19), screen, 80, y_text)
                        y_text = y_text+ 40
                        pygame.display.update()


        ################## Responsável pelo programa voltar a funcionar ################## 

        resposta_erro_aleatorio = choice(lista_erros)
        reconhecer(resposta_erro_aleatorio)
        pygame.display.update()
        mainClock.tick(60)
        

           
main_menu()