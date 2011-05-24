#-------------------------------------------------------------------------------
# Name:        JImage
# Purpose:
#
# Author:      Jeremy Anderson
#
# Created:     25/02/2011
# Copyright:   (c) Jeremy Anderson 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame
from pygame.locals import *
import sys

def loadimage( name, colorkey = None ):
    try:
        image = pygame.image.load( name )
    except pygame.error, message:
        print 'Cannot load image: ', name
        raise SystemExit, message

    image = image.convert()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at( (0, 0 ) )
        image.set_colorkey( colorkey, RLEACCEL )

    return image, image.get_rect()

class JImageException(Exception):
    def __init__( self, description ):
        Exception.__init__( self )
        self.description = description

    def __str__( self ):
        return self.description

class JImage(object):
    def __init__( self, name = 'none' ):
        self.create( name )
    def create( self, name = 'none' ):
        try:
            self.image, self.rect = loadimage( name )
        except SystemExit, message:
            raise JImageException(str(message))


class JImageManager(object):
    def __init__(self):
        self.textureMap = {}
    def create(self, name='none'):
        if name in self.textureMap:
            return self.textureMap[name]
        else:
            self.textureMap[name] = JImage(name)
            return self.textureMap[name]



def load_images(src, ftype = 'png'):
    """ Creates a dict mapping Sprite classnames to image objects """
    images = {}

    files = glob.glob( src+'*.'+ftype )

    for filename in files:
        key = filename.split('.')[0].split( '\\' )[1]

        filename = filename.replace( '\\', '/' )
        print filename
        value = JImage( filename )

        images[key] = value

    return images

if __name__ == '__main__':
    manager = JImageManager()
    try:
        image = manager.create('none')
    except JImageException, message:
        print message
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

