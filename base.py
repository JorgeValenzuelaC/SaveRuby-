import pygame as pg
import sys
from random import randint
from pygame.locals import *
import math
from pygame.constants import BUTTON_X1, KEYDOWN, KEYUP, K_DOWN, K_ESCAPE, K_LEFT, K_LSHIFT, K_RIGHT, K_RSHIFT, K_UP, K_a, K_s, K_d, K_w, K_LSHIFT, K_SPACE, MOUSEBUTTONDOWN

pg.init()
size=(1920,1080)
clock = pg.time.Clock()
# crear ventana
pg.display.set_caption("Pygame Window")
screen = pg.display.set_mode(size)
COLOR_INACTIVE = pg.Color((0,0,0))
COLOR_ACTIVE = pg.Color((33, 27, 207))

#cargadores de imagenes
ruby_image=pg.image.load("sprites/Ruby.png").convert()
ruby_game_image=pg.image.load("sprites/Ruby_game.png").convert()
ganbaruby_image=pg.image.load("sprites/ganbaruby.png").convert()
ruby_ganbaruby_image=pg.image.load("sprites/Ruby_ganbaruby.png").convert()
player1_image=pg.image.load("sprites/Dia.png").convert()
Dia_armada_image=pg.image.load("sprites/Dia_armada.png").convert_alpha()
Dia_armada_image=pg.transform.scale(Dia_armada_image,(170,200))
candycorn_image=pg.image.load("sprites/candycorn.png").convert_alpha()
candycorn_image=pg.transform.scale(candycorn_image,(40,40))
idolpower_image=pg.image.load("sprites/lightstick2.png").convert_alpha()
idolpower_image=pg.transform.scale(idolpower_image,(600,600))
background=pg.image.load("sprites/fondo.png").convert()
background=pg.transform.scale(background,size)
cotton_image=pg.image.load("sprites/cottoncandy.gif").convert()
cotton_image=pg.transform.scale(cotton_image,(80,80))
play=pg.image.load("sprites/play.png").convert_alpha()
easy=pg.image.load("sprites/easy.png").convert_alpha()
normal=pg.image.load("sprites/normal.png").convert_alpha()
hard=pg.image.load("sprites/hard.png").convert_alpha()
wasd=pg.image.load("sprites/wasd.png").convert_alpha()
rubymuerta=pg.image.load("sprites/rubymuerta.png").convert_alpha()
ruby_muriendo=pg.image.load("sprites/Ruby_muriendo.png").convert_alpha()
#creador de rectangulos con opacidad
def draw_rect_alpha(surface, color, rect):
    shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
    pg.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def get_center(image):
    return image.get_width()/2,image.get_height()/2

def dist_eucl(pos1,pos2):
    x=math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
    return x
def rot_center(image, angle):
    """rotate an image while keeping its center"""
    rot_image = pg.transform.rotate(image, angle)
    return rot_image
#colores
SHADOW = (192, 192, 192)
WHITE = (255, 255, 255)
LIGHTGREEN = (0, 255, 0 )
GREEN = (0, 200, 0 )
BLUE = (0, 0, 128)
LIGHTBLUE= (0, 0, 255)
RED= (200, 0, 0 )
LIGHTRED= (255, 100, 100)
PURPLE = (102, 0, 102)
LIGHTPURPLE= (153, 0, 153)

#contador de puntos
font = pg.font.Font("sprites/font.otf", 24)
font_menu=pg.font.Font("sprites/font.otf", 56)
font_color = (0,0,0)
rect = pg.Rect(5*(size[0]/7), size[1]/6,0,0)
#contador poder
rect_poder = pg.Rect(1*(size[0]/7), size[1]/6,0,0)
#letras menu
rect_menu=pg.Rect(size[0]/2-300,size[1]/4,0,0)
#letras prologo
rect_prologo=pg.Rect(size[0]/2-400,size[1]/2-50,0,0)
#musica

pg.mixer.music.set_volume(0.05)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event,asesinados,nombrearchivo):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    SCORE=open("files/"+nombrearchivo,"a")
                    SCORE.write(self.text+" "+str(asesinados)+"\n")
                    print(self.text)
                    self.text = ''
                    SCORE.close()
                    main_menu()
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)



def main_menu():
    pg.mixer.music.load("audio/musiquita.mp3")
    pg.mixer.music.play(-1)
    mult_vel=0.66
    click=False
    while True:
        screen.fill((202, 255, 191))
        screen.blit(player1_image,(size[0]/4-100,size[1]/2))
        screen.blit(ruby_image,(3*(size[0]/4)-100,size[1]/2))
        mx, my = pg.mouse.get_pos()
        txt_surf = font_menu.render("Save Ruby!",True,font_color)
        screen.blit(txt_surf, (rect_menu.right+50, rect_menu.top))
       
        button_1 = pg.Rect(size[0]/2-100,size[1]/2-25,200,50)
        button_2 = pg.Rect(1*size[0]/5-get_center(easy)[0],9*size[1]/12-get_center(easy)[1],150,50)
        button_3 = pg.Rect(1*(size[0]/2)-get_center(normal)[0],9*size[1]/12-get_center(normal)[1],150,50)
        button_4 = pg.Rect(4*(size[0]/5)-75,9*size[1]/12,150,50)
        if button_1.collidepoint((mx, my)):
            if click:
                pg.mixer.music.stop()
                musica=pg.mixer.music.load("audio/game.mp3")
                prologo(mult_vel)
        if button_2.collidepoint((mx, my)):
            if click:
                mult_vel=0.33
                click=False
        if button_3.collidepoint((mx, my)):
            if click:
                mult_vel=0.66
                click=False
        if button_4.collidepoint((mx, my)):
            if click:
                mult_vel=1
                click=False
        
        for event in pg.event.get():
            if event.type== pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
            if event.type==MOUSEBUTTONDOWN:
                if event.button == 1:
                    click=True
                #actualizar pantalla
        screen.blit(play, (size[0]/2-get_center(play)[0], size[1]/2-get_center(play)[1]))
        screen.blit(easy, (1*size[0]/5-get_center(easy)[0],9*size[1]/12-get_center(easy)[1]))
        screen.blit(normal, (1*(size[0]/2)-get_center(normal)[0],9*size[1]/12-get_center(normal)[1]))
        screen.blit(hard, (4*(size[0]/5)-get_center(hard)[0],9*size[1]/12-get_center(hard)[1]))
        if mult_vel == 0.33:
            draw_rect_alpha(screen, (229, 255, 59, 127), (1*size[0]/5-get_center(easy)[0],9*size[1]/12-get_center(easy)[1],150,50))
        elif mult_vel== 0.66:
            draw_rect_alpha(screen, (229, 255, 59, 127),(1*(size[0]/2)-get_center(normal)[0],9*size[1]/12-get_center(normal)[1],150,50))
        else:
            draw_rect_alpha(screen, (229, 255, 59, 127),(4*(size[0]/5)-get_center(hard)[0],9*size[1]/12-get_center(hard)[1],150,50))
        pg.display.update()
        clock.tick(60)
def prologo(mult_vel):
    contadorprologo=0
    while True:
        screen.fill((202, 255, 191))
        screen.blit(wasd,[size[0]/2-370,size[1]/2])
        texto_prologo1 = font.render("Ruby ha comido demasiados caramelos y ahora ellos quieren asesinarla!", True, font_color)
        texto_prologo2 = font.render("Ayuda a Dia a destruirlos >:D", True, font_color)
        texto_prologo3 = font.render("Presiona cualquier botón para comenzar", True, font_color)
        screen.blit(texto_prologo1, (rect_prologo.right-300, rect_prologo.top-200))  
        screen.blit(texto_prologo2, (rect_prologo.right+100, rect_prologo.top))  
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                game(mult_vel)
        if contadorprologo%100<=55:
            screen.blit(texto_prologo3,(rect_prologo.right, rect_prologo.top+400))
        pg.display.update()
        clock.tick(60)
        contadorprologo+=1

def pause(tiempo,mult_vel,asesinados,player2_location):
    pg.mixer.music.play(-1)
    n=0
    
    while True:
        if n>tiempo:
            game_over(mult_vel,asesinados)
        else:
            n+=1
        screen.blit(ruby_muriendo,player2_location)
        pg.display.update()
        clock.tick(60)
def game(mult_vel):
    pg.mixer.music.play(-1)
    numero_corns=1
    numero_cotton=1

    corns_locations=[[randint(0,size[0]),size[1]-20]]

    cotton_locations=[[randint(0,size[0]),size[1]-20]]

    asesinados=0
    moving1_right = False
    moving1_left = False
    moving1_up = False
    moving1_down = False
    moving2_right = False
    moving2_left = False
    moving2_up = False
    moving2_down = False
    shifting1=False
    player1_location = [size[0]/2-100,250]
    player2_location = [size[0]/2-100,150]
    speed1=1
    speed2=1
    direccion=1
    poder_contador=0
    poder_activado=0
    angulo=0

    
    while True:
        #fondo
        screen.blit(background,(0,0))
        #
        #randomizadores
        contador1=randint(1,300) #cambio de direccion ruby
        contador2=randint(1,150) #aparición de enemigos


        if contador1<=3:
            direccion=direccion*-1
        
        #enemy spawner
        if contador2<=5+2*3*mult_vel and numero_corns<12:
            numero_corns+=1
            corns_locations.append([randint(50,size[0]-50),size[1]-20])
        if contador2<=2+2*3*mult_vel and numero_cotton<6:
            numero_cotton+=1
            cotton_locations.append([randint(50,size[0]-50),size[1]-20])
        # idol power
        if poder_contador>= 60:
            
            if poder_activado<=400:
                screen.blit(rot_center(idolpower_image,angulo),[player1_location[0]-get_center(rot_center(idolpower_image,angulo))[0]+80,player1_location[1]-get_center(rot_center(idolpower_image,angulo))[1]+100])
                angulo+=2
                poder_activado+=1
            else:
                poder_contador=0
                poder_activado=0

        #colisiones con enemigos
        if len(cotton_locations)!=0:
            c=0
            while c<len(cotton_locations):
                # juego se reinicia por chocar con ruby
                if abs(cotton_locations[c][0]-player2_location[0]-100)<=70 and abs(cotton_locations[c][1]-player2_location[1]-100)<110 :
                    pg.mixer.music.load('audio/gameover.mp3')
                    pause(75,mult_vel,asesinados,player2_location)
                
                distancia=player2_location[0]+100-cotton_locations[c][0]
                if distancia<=0:
                    cotton_locations[c][0]-=2
                else:
                    cotton_locations[c][0]+=2
                screen.blit(cotton_image,cotton_locations[c])    
                cotton_locations[c][1]-=5*mult_vel

                # despawn por llegar arriba
                if cotton_locations[c][1]<=50:
                    cotton_locations.pop(c)
                    numero_cotton-=1
                    

                if len(cotton_locations)>0:
                    if poder_activado>0:
                        if dist_eucl([player1_location[0]+80,player1_location[1]+100],cotton_locations[c])<300:
                            cotton_locations.pop(c)
                            numero_cotton-=1
                            asesinados+=1
                        else:
                            c+=1
                    else:
                        if abs(player1_location[0]+100-cotton_locations[c][0]-40)<=100 and abs(cotton_locations[c][1]-player1_location[1]-100)<=110:
                            cotton_locations.pop(c)
                            numero_cotton-=1
                            asesinados+=1
                            poder_contador+=2
                        else:
                            c+=1
                else:
                    c+=1
        if len(corns_locations)!=0:
            c=0
            while c<len(corns_locations):

                # juego se reinicia por chocar con ruby
                if abs(corns_locations[c][0]-player2_location[0]-100)<=70 and abs(corns_locations[c][1]-player2_location[1]-100)<110 :
                    pg.mixer.music.load('audio/gameover.mp3')
                    pause(75,mult_vel,asesinados,player2_location)
                
                screen.blit(candycorn_image,corns_locations[c])
                corns_locations[c][1]-=4*mult_vel
                
                # despawn por llegar arriba
                if corns_locations[c][1]<=50:
                    corns_locations.pop(c)
                    numero_corns-=1

                # poder elimina enemigo
                

                # dia elimina enemigo
                if len(corns_locations)>0:
                    if poder_activado>0:
                        if dist_eucl([player1_location[0]+80,player1_location[1]+100],corns_locations[c])<300:
                            corns_locations.pop(c)
                            numero_corns-=1
                            asesinados+=1
                        else:
                            c+=1
                    else:
                        if abs(player1_location[0]+100-corns_locations[c][0]-40)<=100 and abs(corns_locations[c][1]-player1_location[1]-100)<=110:
                            corns_locations.pop(c)
                            numero_corns-=1
                            asesinados+=1
                            poder_contador+=1
                        else:
                            c+=1
                else:
                    c+=1
                
        if player1_location[1]>player2_location[1]:
            if asesinados%100<=5:
                screen.blit(ruby_ganbaruby_image,player2_location)
                screen.blit(ganbaruby_image,[player2_location[0]+180,player2_location[1]-25])
                screen.blit(Dia_armada_image,player1_location)
            else:
                screen.blit(ruby_game_image,player2_location)
                screen.blit(Dia_armada_image,player1_location)
        else:
            if asesinados%100<=5:
                screen.blit(Dia_armada_image,player1_location)
                screen.blit(ruby_ganbaruby_image,player2_location)
                screen.blit(ganbaruby_image,[player2_location[0]+180,player2_location[1]-25])
            else:
                screen.blit(Dia_armada_image,player1_location)
                screen.blit(ruby_game_image,player2_location)
        if direccion==1:
            player2_location[0]+=4
        else:
            player2_location[0]-=4
        if player2_location[0]>=(size[0]-(size[0]/5)) or player2_location[0]<=size[0]/5:
            direccion=direccion*-1

        if shifting1==True:
            speed1=3
        else:
            speed1=1
        if moving1_right==True:
            player1_location[0]+=4*speed1
        
        if moving1_left==True:
            player1_location[0]-=4*speed1

        if moving1_up==True:
            player1_location[1]-=4*speed1
        
        if moving1_down==True:
            player1_location[1]+=4*speed1
        
        if moving2_right==True:
            player2_location[0]+=4*speed2
        
        if moving2_left==True:
            player2_location[0]-=4*speed2

        if moving2_up==True:
            player2_location[1]-=4*speed2
        
        if moving2_down==True:
            player2_location[1]+=4*speed2

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_d:
                    moving1_right = True
                if event.key == K_a:
                    moving1_left = True
                if event.key == K_w:
                    moving1_up = True
                if event.key == K_s:
                    moving1_down = True
                if event.key == K_LSHIFT:
                    shifting1= True
                if event.key == K_SPACE:
                    shifting1= True
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == KEYUP:
                if event.key == K_d:
                    moving1_right= False
                if event.key == K_a:
                    moving1_left = False 
                if event.key == K_w:
                    moving1_up = False
                if event.key == K_s:
                    moving1_down = False
                if event.key == K_LSHIFT:
                    shifting1= False
                if event.key == K_SPACE:
                    shifting1= False

        #contador de puntos
        txt_surf = font.render("puntos="+str(asesinados), True, font_color)
        draw_rect_alpha(screen, (219, 61, 96, 127), (5*size[0]/7-10,size[1]/6, 230, 80))
        screen.blit(txt_surf, (rect.right+10, rect.top))
        
        #contador poder idol
        texto_poder = font.render("Idol Power="+str(poder_contador)+'/60', True, font_color)
        draw_rect_alpha(screen, (219, 61, 96, 127), (1*size[0]/7-10,size[1]/6, 400, 80))
        screen.blit(texto_poder, (rect_poder.right+10, rect_poder.top))
        

        #actualizar pantalla
        pg.display.flip()
        clock.tick(60)
def game_over(mult_vel,asesinados):
    input_box1 = InputBox(300,size[1]/2,200,50)
    input_boxes = [input_box1]
    nombrearchivo="highscores"+str(mult_vel)+".txt"
    Puntajes=open("files/"+nombrearchivo,"r")
    Puntajeslista=[]
    for line in Puntajes:
        for word in line.split():
            if word.isdigit():
                Puntajeslista.append([line,int(word)])
    Puntajes.close()
    Puntajeslista.sort(key=lambda x:x[1])
    Puntajeslista.reverse()

    print(Puntajeslista)
    while True:
        Puntajes=open("files/"+nombrearchivo,"r")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            for box in input_boxes: 
                box.handle_event(event,asesinados,nombrearchivo)

        for box in input_boxes:
            box.update()

        screen.fill((202, 255, 191))
        
        for box in input_boxes:
            box.draw(screen)
        c=300

        texto_Highscore= font.render("Highscores :",True, font_color)
        screen.blit(texto_Highscore,(1300,200))

        for tupla in Puntajeslista:
            texto_puntaje = font.render(tupla[0][:-1], True, font_color)
            screen.blit(texto_puntaje, (1300, c))
            c+=50

        screen.blit(rubymuerta,[size[0]/2,size[1]/2])
        texto_gameover = font.render("puntaje="+str(asesinados), True, font_color)
        draw_rect_alpha(screen, (219, 61, 96, 127), (1*size[0]/7-10,size[1]/6, 400, 80))
        screen.blit(texto_gameover, (rect_poder.right+10, rect_poder.top))
        texto_gameover1 = font.render("Ruby ha sido asesinada, es tu culpa", True, font_color)
        texto_gameover2 = font.render("Introduce tu nombre :D", True, font_color)
        screen.blit(texto_gameover1, (rect_prologo.right-300, rect_prologo.top-200))  
        screen.blit(texto_gameover2, (rect_prologo.right-300, rect_prologo.top-50)) 
        pg.display.flip()
        clock.tick(30)
main_menu()