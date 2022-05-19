# Base extraida do video (memory game):
# https://www.youtube.com/watch?v=Xpvf9lwRERU
#


from inspect import currentframe, getframeinfo

import os
import pygame
import random
from PIL import Image


# A classe Tile vai conter as imagens
class Tile(pygame.sprite.Sprite):
    # Recebendo o nome do arquivo a ser carregado e suas coordenadas desejadas
    def __init__(self, filename, x, y):
        # Chamando o inicializador da classe Sprite
        super().__init__()

        # Pegando soh o nome do arquivo, sem a extensao '.png'
        # A funcao 'split' divide o nome do arquivo pelo separador '.' e pegamos
        #    o item '0' (que eh o nome do arquivo)
        self.name = filename.split('.')[0]

        # Carregando a imagem ...
        self.image = pygame.image.load(os.path.join(Atipical_folder, filename))

        self.rect = self.image.get_rect( topleft = (x, y) )


class Game():
    # inicia com 2 x 2
    def __init__(self, linhas=2, colunas=2):

        # Controle dos niveis de dificuldade
        self.level = 1
        self.level_complete = False

        # Criando algumas variaveis ..
        self.padding = 10
        self.margin_top = 160
        #self.cols = colunas-1
        #self.rows = linhas-1
        self.cols_ini = colunas
        self.rows_ini = linhas

        # Musica
        # self.inicia_musica()

        self.images_group = pygame.sprite.Group()

        # Tenho que bloquear o jogo para nao permitir clicar em outras figuras
        self.block_game = False

        # Gerar o primeiro nivel, jah que estou no metodo __init__
        self.generate_level(self.level)

    def generate_level(self, level):
        self.level_complete = False
        # Aumento uma linha e uma coluna para o proximo nivel ..
        if level == 1:
            self.rows = self.rows_ini
            self.cols = self.cols_ini
        else:
            self.rows += 1
            self.cols += 1

        self.carregar_imagens()

        # Gerando o conjunto de imagens ..
        self.generate_image_set(self.all_images)


    def generate_image_set(self, img_array):

        # Pelo meu desenho da tela, nao posso ter mais de XXX linhas (rows)
        # Preciso me certificar disto ..

        # Me certificando que estah centralizado horizontalmente
        TILES_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARGIN = RIGHT_MARGIN = (WIDTH - TILES_WIDTH) // 2

        # 'images_group' eh do tipo 'pygame.sprite.Group()'
        self.images_group.empty()

        for i in range(len(img_array)):
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows) * (self.img_height + self.padding)
            imagem = Tile(img_array[i], x, y)
            self.images_group.add(imagem)


    def update(self, event_list):
        # Onde a acao vai acontecer

        # Testando um conjunto de eventos de usuario
        self.user_input(event_list)

        # Ao final, desenho ..
        self.desenhar()

        # Testando conjunto de eventos do jogo .. poderia ser um unico metodo, lah no 'user_input'
        self.check_level_complete(event_list)

    def user_input(self, event_list):
        # Varrendo os eventos ... a atualizacao da tela ocorrera no metodo desenhar()
        for e in event_list:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == MOUSEBUTTON_LEFT:
                #print('Hi')
                '''if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    #print("colidiu .. mouse com o botao de chavear a musica")
                    # Como colidiu, vou chavear o estado da musica ..
                    if self.is_music_playing == True:
                        self.is_music_playing = False
                        # Trocando o icone para o icone de 'off/desligada' a musica
                        self.music_toggle = self.sound_off
                        pygame.mixer.music.pause()  # pausando, de fato, a musica
                    else:
                        self.is_music_playing = True
                        # Trocando o icone para o icone de 'on/ligada' a musica
                        self.music_toggle = self.sound_on
                        pygame.mixer.music.unpause()  # retornando, de fato, a musica, onde ela estava'''
            # Foi pressionada uma tecla ..
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and self.level_complete:
                    self.block_game = False
                    self.level += 1
                    if self.level > MAX_LEVEL:
                        self.level = 1
                    # Gerando o proximo nivel do jogo ..
                    self.generate_level(self.level)


    def check_level_complete(self, event_list):
        # Verificar se o jogo estah bloqueado para eventos
        if self.block_game == False:
            for e in event_list:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == MOUSEBUTTON_LEFT:
                    # Preciso iterar com as 'imagens'
                    for img in self.images_group:
                        if img.rect.collidepoint(e.pos) and img.name == 'a':
                            print('Mouse colidiu com a imagem atipica: a[.png]')
                            # 'function' imprime o nome da funcao, semelhante a __FUNCTION__ em 'C'
                            # 'lineno' imprime o numero da linha, semelhante a __LINE__ em 'C'
                            print("( {}-{} ) Mouse colidiu com a imagem atipica: a[.png]".format(getframeinfo(currentframe()).function, str(getframeinfo(currentframe()).lineno)))
                            self.level_complete = True
                            self.block_game = True
                            break
                        else:
                            self.level_complete = False
        '''
        else:
            self.frame_count += 1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False
                for img in self.images_group:
                    if img.name in self.flipped:
                        img.esconder()
                self.flipped = []
        '''

    def desenhar(self):
        # Desenha tudo ..
        Screen.fill(BLACK)

        # Fontes
        title_font = pygame.font.Font(os.path.join(Font_folder, 'Little Alien.ttf'), 44)
        content_font = pygame.font.Font(os.path.join(Font_folder, 'Little Alien.ttf'), 20)

        # Texto com o titulo .. usando o tipo 'title_font'
        title_text = title_font.render(GAME_TITLE, True, WHITE)
        # Colocar o texto, com o titulo, num retangulo (o Pygame trabalha com retangulos)
        title_rect = title_text.get_rect(midtop=(WIDTH // 2, MARGEM_SUP))

        # Incluindo o nivel sendo jogado pelo usuario .. usando o tipo 'content_font'
        level_text = content_font.render('Nível ' + str(self.level) + ' de ' + str(MAX_LEVEL), True, WHITE)
        # Colocando nun retanglo ..
        level_rect = level_text.get_rect( midtop=(WIDTH // 2, 8*MARGEM_SUP) )

        # Texto informativo .. usando o tipo 'content_font'
        info_text = content_font.render('Encontre o diferente', True, WHITE)
        info_rect = info_text.get_rect( midtop=(WIDTH // 2, 12*MARGEM_SUP) )

        if self.level == MAX_LEVEL:
            msg = 'Parabéns, você chegou ao último nível | Pressione espaço para começar novamente.'
        else:
            msg = 'Nível completado | Pressione espaço para o próximo nível.'
        next_text = content_font.render(msg, True, WHITE)
        next_rect = next_text.get_rect( midbottom=(WIDTH // 2, HEIGHT-MARGEM_INF) )

        #
        # 'blit()' eh como um 'commit' para desenhar na tela visivel do jogo
        Screen.blit(title_text, title_rect)
        Screen.blit(level_text, level_rect)
        Screen.blit(info_text, info_rect)

        # Desenhando o conjunto de 'tiles'
        self.images_group.draw(Screen)
        self.images_group.update()

        # Soh mostro a mensagem se houve mudanca de nivel ..
        if self.level_complete == True:
            Screen.blit(next_text, next_rect)

        # Atualizando o icone do controle do som .. caso o jogador tenha clicado nele
        # No caso dos controles, vamos colocar um retangulo branco para destacar ..
        #    (x_ini, y_ini, tam_x, tam_y)
        '''retang_branco = (WIDTH-90, 0, 90)
        pygame.draw.rect(Screen, WHITE, retang_branco)
        Screen.blit(self.music_toggle, self.music_toggle_rect)'''

    '''def inicia_musica(self):
        # Tratando da carga inicial da musica e criando as variaveis para controlah-la

        # Carregando arquivo de musica
        pygame.mixer.music.load(os.path.join(Sound_folder, 'bg-music.mp3'))
        pygame.mixer.music.set_volume(SOUND_VOLUME_INITIAL)
        pygame.mixer.music.play()

        # Criando/carregando os icones on-off para ligar/desligar a musica
        self.sound_on = pygame.image.load(os.path.join(Img_folder, 'speaker.png')).convert_alpha()
        self.sound_off = pygame.image.load(os.path.join(Img_folder, 'mute.png')).convert_alpha()

        # Comecando com a musica: True
        # Para comecar desligada (sem musica), basta trocar para 'False'
        self.is_music_playing = False

        if self.is_music_playing == True:
            self.music_toggle = self.sound_on
        else:
            self.music_toggle = self.sound_off
            pygame.mixer.music.pause()

        # Criando um retangulo para a figura do icone ..
        self.music_toggle_rect = self.music_toggle.get_rect(topright=(WIDTH - MARGEM_SUP, MARGEM_SUP))'''



    def carregar_imagens(self):
        # Carregando a imagem 'linhas x colunas' vezes
        # Criar um array com as imagens
        self.all_images = []

        #self.img_normal = os.path.join(Atipical_folder, 'n.png')
        #self.img_atipica = os.path.join(Atipical_folder, 'a.png')
        self.img_normal = 'n.png'
        self.img_atipica = 'a.png'

        # Pegando o tamanho da imagem atipica. Estamos supondo qur todas as
        #    imagens tem o mesmo tamanho, entao nao importa de qual imagem pegar o tamanho
        img = Image.open(os.path.join(Atipical_folder, self.img_atipica))
        self.img_width, self.img_height = img.size  # largura e altura
        img.close()

        # Posicao do arquivo/imagem atipica - randomica ..
        self.posicao_img_atipica = random.randint(0, (self.cols*self.rows-1) )

        for i in range(0, self.rows*self.cols):
            img_anexar = self.img_normal
            if i == self.posicao_img_atipica:
                img_anexar = self.img_atipica
            self.all_images.append((img_anexar))

        # 'function' imprime o nome da funcao, semelhante a __FUNCTION__ em 'C'
        # 'lineno' imprime o numero da linha, semelhante a __LINE__ em 'C'
        print("( {}-{} ) Posica da imagem atipica: {}; Imagens= {}"
              .format(getframeinfo(currentframe()).function, str(getframeinfo(currentframe()).lineno),
                      str(self.posicao_img_atipica), self.all_images)
              )
        # 'function' imprime o nome da funcao, semelhante a __FUNCTION__ em 'C'
        # 'lineno' imprime o numero da linha, semelhante a __LINE__ em 'C'
        print("( {}-{} ) Imagem: Largura={}; Altura={}"
              .format(getframeinfo(currentframe()).function, str(getframeinfo(currentframe()).lineno),
                      str(self.img_width), str(self.img_height))
              )



if __name__ == '__main__':

    #
    # Letras maiusculas nas variaveis, vou usar como variaveis Globais ...
    #
    # Folders com os 'assets' (art, sound, etc) .. global
    root_folder = os.path.dirname(__file__)  # diretorio corrente
    #Game_folder = os.path.join(root_folder, 'game')
    Game_folder = root_folder
    Img_folder = os.path.join(Game_folder, 'img')
    Font_folder = os.path.join(Game_folder, 'fonts')
    Sound_folder = os.path.join(Game_folder, 'sounds')
    Atipical_folder = os.path.join(Game_folder, 'atipical')
    #Video_folder = os.path.join(game_folder, 'video')  # nao estou conseguindo importar o cv2 .. entao nao vou usar

    # Tamanho da tela do jogo
    WIDTH = 1024
    HEIGHT = 800

    # Margem, em pixels
    MARGEM_SUP = 10
    MARGEM_INF = 40

    # Algumas cores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)

    MOUSEBUTTON_LEFT = 1
    MOUSEBUTTON_WHEEL = 2
    MOUSEBUTTON_RIGHT = 3

    # Como o jogo vai fazer o refresh, independentemente do computador
    #    ser mais rapido que o atual
    FPS = 20

    # Titulo da janela e do jogo
    GAME_TITLE = 'Atípico'

    # Numero maximo de niveis
    MAX_LEVEL = 4

    # Volume inicial da musica
    SOUND_VOLUME_INITIAL = 0.20

    pygame.init()
    Screen = pygame.display.set_mode( (WIDTH, HEIGHT) ) # variavel global ..
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    #
    # Loop principal do jogo
    #
    game = Game(linhas=2, colunas=2)
    #game = Game()
    running = True
    while running:

        # Manter o jogo fazendo refresh numa mesma taxa,
        #    independente da velocidade da maquina onde o jogo roda
        clock.tick(FPS)

        event_list = pygame.event.get()
        for event in event_list:
            # Clicou no 'X' da janela
            if event.type == pygame.QUIT:
                running = False  # saindo do looping principál

        # Atualizar, de fato, a tela do usuario
        pygame.display.update()

        # Tratar outros eventos (relativos ao jogo mesmo) que nao o de saida do jogo ..
        game.update(event_list)

    # Fim do looping principal
    pygame.quit()