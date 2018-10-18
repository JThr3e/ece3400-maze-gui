import pandas as pd
import webbrowser, os
import pygame
import time
import sys
import threading
import copy
# Prevent cell truncating when creating the HTML table
pd.set_option('display.max_colwidth', 1)

class View():
  def __init__(self, rows, cols, open_browser=False, refresh_rate=1, default_sprite='./sprites/unexplored.jpg'):
    self.squareSize = 50
    pygame.init()
    self._refresh_rate = refresh_rate
    size = (cols*self.squareSize,rows*self.squareSize)
    self.screen = pygame.display.set_mode(size)
    self._sprite_layout = [[{}]*rows]*cols

    handler = EventHandler()
    handler.start()


#sprite_layout is the matrix containing the model info
  def render(self, model):
    self.screen.fill((0,0,0)) 
    for i in range(0, len(model)):
        for j in range(0, len(model[0])):
            
            if model[j][i]['explored'] == False:
                pygame.draw.rect(self.screen,(0,0,0),(i*self.squareSize+1,j*self.squareSize+1,self.squareSize-2,self.squareSize-2))
            elif model[j][i]['explored'] == True:
                pygame.draw.rect(self.screen,(255,0,0),(i*self.squareSize+1,j*self.squareSize+1,self.squareSize-2,self.squareSize-2))
                if model[j][i]['north'] == True:
                  pygame.draw.rect(self.screen,(255,255,255),(i*self.squareSize+1,j*self.squareSize+1,self.squareSize-2,(self.squareSize/8)-2))
                if model[j][i]['east'] == True:
                  pygame.draw.rect(self.screen,(255,255,255),((i+1)*self.squareSize-(self.squareSize/8)+1,j*self.squareSize+1,((self.squareSize/8)-2),self.squareSize-2))
                if model[j][i]['west'] == True:
                  pygame.draw.rect(self.screen,(255,255,255),(i*self.squareSize+1,j*self.squareSize+1,((self.squareSize/8)-2),self.squareSize-2))
                if model[j][i]['south'] == True:
                  pygame.draw.rect(self.screen,(255,255,255),(i*self.squareSize+1,(j+1)*self.squareSize-(self.squareSize/8)+1,self.squareSize-2,(self.squareSize/8)-2))
            else:
                print("wronk")
            if model[j][i]['iamhere'] == True:
                pygame.draw.circle(self.screen,(0,255,0),(i*self.squareSize+1+(self.squareSize/2),j*self.squareSize+1+(self.squareSize/2)), (self.squareSize/4)-2)
    pygame.event.pump()
    pygame.display.flip()


class EventHandler(threading.Thread):

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()