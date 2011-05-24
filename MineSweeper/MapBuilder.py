import random

class MineSweeperMap(object):
    def __init__(self, width=10, height=10, numberOfBombs=30):
        self.width = width
        self.height = height
        self.numberOfBombs = numberOfBombs
        #self.buildmap(startingPos)
        self.map = [[' ' for x in xrange(self.width)] for y in xrange(self.height)]

    def buildmap(self, startingPos):
        #self.map = [[' ' for x in xrange(self.width)] for y in xrange(self.height)]
        self.placebombs(startingPos)
        self.placenumbers()

    def placebombs(self, startingPos):
        i = self.numberOfBombs
        while i > 0:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            if self.map[y][x] == ' ' and not (y == startingPos[1] and x == startingPos[0]):
                self.map[y][x] = '*'
                i -= 1

    def placenumbers(self):
        dxy = ((0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1))
        for y in xrange(self.height):
            for x in xrange(self.width):
                if self.map[y][x] == '*':
                    for d in dxy:
                        n = (x+d[0], y+d[1])
                        if 0 <= n[0] < self.width and 0 <= n[1] < self.height:
                            if self.map[n[1]][n[0]] == ' ':
                                self.map[n[1]][n[0]] = 0
                            if self.map[n[1]][n[0]] != '*':
                                self.map[n[1]][n[0]] += 1

    def clearmap(self):
        self.map = [[' ' for x in xrange(self.width)] for y in xrange(self.height)]

    def printmap(self):
        for y in self.map:
            s = ' '
            for x in y:
                s += '{0} '.format(x)
            print s

    def getmap(self):
        return self.map



def main():
    mine = MineSweeperMap()#(startingPos = (5,5))#(3,3,8,(1,1))
    mine.buildmap((5,5))
    mine.printmap()
    mine.clearmap()
    mine.buildmap((5,5))
    mine.printmap()




if __name__ == '__main__':
    main()