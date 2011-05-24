import pygame
from pygame.locals import *
from Queue import *
import random
import sys
import time
from JImage import JImageManager
from MapBuilder import MineSweeperMap

class Game(object):
    def __init__(self, width = 10, height = 10, numberOfBombs = 10):
        self.width = max(width, 9)
        self.height = max(height, 9)
        self.numberOfBombs = min(numberOfBombs, int(0.85 * self.width * self.height))
        self.screenSize = (self.width * 32, self.height * 32)
        self.running = True
        self.imageManager = JImageManager()
        self.sprites = {}
        self.minemap = MineSweeperMap(self.width, self.height, self.numberOfBombs)
        self.grid = [['-' for x in xrange(self.width)] for y in xrange(self.height)]
        self.firstClick = True
        self.GameOver = False
        self.Win = False

        if not pygame.font:
            print 'Fonts disabled'

        if not pygame.mixer:
            print 'Sounds disabled'

        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize, DOUBLEBUF | HWSURFACE) # | FULLSCREEN )
        pygame.display.set_caption('MineSweeper')
        #pygame.mouse.set_visible(0)
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.endBackground = pygame.Surface((300, 100))
        self.endBackground.fill((0, 0, 0))
        self.endBackground.set_alpha(180)

        self.oldbackground = self.background.convert()

        self.__buildsprites()
        self.mouseButtonPrevious = (0, 0, 0)
        self.mouseButtonCurrent = (0, 0, 0)
        self.mouseButtonTriggered = (0, 0, 0)

        if pygame.font:
            fontsize = 24
            self.font = pygame.font.Font( None, fontsize )
            swin = 'You have won the game.'
            slose = 'You have lost the game.'
            stext2 = 'Press \'R\' to restart and play again.'
            stext3 = 'Or press \'Escape\' to quit.'
            self.WinText = self.font.render( swin, 1, ( 255, 255, 200 ) )
            self.LoseText = self.font.render( slose, 1, ( 255, 255, 200 ) )
            self.Text2 = self.font.render( stext2, 1, ( 255, 255, 200 ) )
            self.Text3 = self.font.render( stext3, 1, ( 255, 255, 200 ) )
            height = self.background.get_height()/2 - ((3 + fontsize)*3)/2
            temp = (self.background.get_width() - max(len(swin),len(slose)) * fontsize) / 2
            self.Text1Pos = ((self.background.get_width() - max(len(swin),len(slose)) * 8) / 2, height)
            self.Text2Pos = ((self.background.get_width() - (len(stext2)-2) * 8) / 2, height + fontsize + 3)
            self.Text3Pos = ((self.background.get_width() - (len(stext3)-2) * 8) / 2, height + (fontsize + 3)*2)
##            background = oldbackground.convert()
##            background.blit( text1, textpos1 )
##            background.blit( text2, textpos2 )

    def __buildminemap(self, startingPos):
        self.minemap.buildmap(startingPos)

    def __buildsprite(self,name,imagename):
        tempsprite = pygame.sprite.Sprite()
        tempimage = self.imageManager.create(imagename)
        tempsprite.image, tempsprite.rect = tempimage.image, tempimage.rect
        self.sprites[name] = tempsprite

    def __buildsprites(self):
        self.__buildsprite('-', 'blank.png')
        self.__buildsprite(' ', 'empty.png')
        self.__buildsprite('*', 'bomb.png')
        self.__buildsprite('<', 'flag.png')
        self.__buildsprite('1', '1.png')
        self.__buildsprite('2', '2.png')
        self.__buildsprite('3', '3.png')
        self.__buildsprite('4', '4.png')
        self.__buildsprite('5', '5.png')
        self.__buildsprite('6', '6.png')
        self.__buildsprite('7', '7.png')
        self.__buildsprite('8', '8.png')

    def __restart(self):
        self.grid = [['-' for x in xrange(self.width)] for y in xrange(self.height)]
        self.firstClick = True
        self.minemap.clearmap()
        self.GameOver = False
        self.Win = False

    def update(self, dt = 0.0):
        self.logic(dt)

        self.background = self.oldbackground.convert()

        self.screen.blit(self.background, ( 0, 0 ))

        for y in xrange(self.height):
            for x in xrange(self.width):
                sprite = self.sprites[self.grid[y][x]]
                sprite.rect.left = x * 32
                sprite.rect.top = y * 32
                self.screen.blit(sprite.image,sprite.rect)

        if self.GameOver and pygame.font:
            height = self.background.get_height()/2 - 100/2 - 5
            width = self.background.get_width()/2 - 300/2

            self.screen.blit(self.endBackground, (width,height))

            if self.Win:
                self.screen.blit(self.WinText, self.Text1Pos)
            elif not self.Win:
                self.screen.blit(self.LoseText, self.Text1Pos)
            self.screen.blit(self.Text2, self.Text2Pos)
            self.screen.blit(self.Text3, self.Text3Pos)


        pygame.display.flip()

    def __cleararea(self,pos):
        areas = ((0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1))
        tempmap = self.minemap.getmap()
        visited = [[False for x in xrange(self.width)] for y in xrange(self.height)]
        q = Queue()

        q.put(pos)
        while not q.empty():
            n = q.get()
            if tempmap[n[1]][n[0]] != '*' and self.grid[n[1]][n[0]] != '<':
                self.grid[n[1]][n[0]] = str(tempmap[n[1]][n[0]])
                visited[n[1]][n[0]] = True
            areas = ((0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1))
            for x in areas:
                nn = (n[0]+x[0], n[1]+x[1])
                if 0 <= nn[0] < self.width and 0 <= nn[1] < self.height:
                    if tempmap[nn[1]][nn[0]] == ' ' and not visited[nn[1]][nn[0]]:
                        q.put(nn)
                        visited[nn[1]][nn[0]] = True
                    elif tempmap[nn[1]][nn[0]] != '*' and self.grid[nn[1]][nn[0]] != '<':
                        self.grid[nn[1]][nn[0]] = str(tempmap[nn[1]][nn[0]])
                        visited[nn[1]][nn[0]] = True

    def __showbombs(self):
        for y in xrange(self.height):
            for x in xrange(self.width):
                if self.minemap.getmap()[y][x] == '*':
                    self.grid[y][x] = '*'

    def __checkwin(self):
        for y in xrange(self.height):
            for x in xrange(self.width):
                if self.grid[y][x] == '-' or self.grid[y][x] == '<':
                    if self.minemap.getmap()[y][x] != '*':
                        return False
        return True

    def logic(self, dt = 0.0):
        for event in pygame.event.get():
            if event.type is QUIT:
                self.running = False

        keys = pygame.key.get_pressed()

        if keys[K_ESCAPE]:
            self.running = False
        if keys[K_r]:
            self.__restart()

        if self.__checkwin():
            self.GameOver = True
            self.Win = True

        focused = pygame.mouse.get_focused()
        if focused and not self.GameOver:
            mousepos = pygame.mouse.get_pos()
            self.mouseButtonPrevious = self.mouseButtonCurrent
            self.mouseButtonCurrent = pygame.mouse.get_pressed()
            self.mouseButtonTriggered = [self.mouseButtonPrevious[x] and not self.mouseButtonCurrent[x] for x in xrange(len(self.mouseButtonCurrent))]
            idx = mousepos[0]/32
            idy = mousepos[1]/32

            if self.mouseButtonTriggered[0] and self.grid[idy][idx] != '<':
                if self.firstClick:
                    self.__buildminemap((idx,idy))
                    self.firstClick = False

                tempid = str(self.minemap.getmap()[idy][idx])
                if tempid == ' ':
                    self.__cleararea((idx,idy))
                elif tempid.isalnum():
                    self.grid[idy][idx] = tempid
                elif tempid == '*':
                    self.__showbombs()
                    self.GameOver = True
                    self.Win = False

            if self.mouseButtonTriggered[2]:
                if self.grid[idy][idx] == '-':
                    self.grid[idy][idx] = '<'
                elif self.grid[idy][idx] == '<':
                    self.grid[idy][idx] = '-'

    def exit(self):
        pygame.display.quit()
        pygame.quit()
