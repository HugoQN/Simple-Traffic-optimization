# layout.py

import os
from game import Info, Intersection, Crossroad, Road

class Layout(object):
    """
    A Layout parse the map into Graph.
    """

    def __init__(self, layoutText):
        self.width = len(layoutText[0])
        self.height = len(layoutText)
        self.mapInfo = Info(self.width, self.height)
        self.intersections = []
        self.crossroads = []
        self.roads = []
        self.parseLayoutText(layoutText)
        self.layoutText = layoutText

    def parseLayoutText(self, layoutText):
        """
        Parse all intersections and crossroads first, and then parse the roads in the map.
        """

        self.__parseMap(layoutText)
        self.__parseMap2(layoutText)

    def __parseMap(self, layoutText):
        # Add information into mapInfo,intersecions,crossroads.
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[y][x]
                if self.mapInfo.get(x, y) is not None: continue
                if layoutChar == '%':
                    self.mapInfo.setField(x, y)
                elif layoutChar == 'I':
                    # The same intersection/crossroad is labed the same number.
                    number = len(self.intersections)
                    positions = self.__parseIntersection(layoutText, x, y, number)
                    self.intersections.append(Intersection(number, positions))
                elif layoutChar == 'C':
                    number = len(self.crossroads)
                    positions = self.__parseCrossroad(layoutText, x, y, number)
                    self.crossroads.append(Crossroad(number, positions))

    def __parseIntersection(self, layoutText, x, y, number):
        # To find the same block of intersecion (recurssively).
        self.mapInfo.setIntersection(x, y, number)
        positions = [(x, y)]
        for (nextX, nextY) in self.__getPosNearBy(x, y):
            if layoutText[nextY][nextX] != 'I': continue
            if self.mapInfo.get(nextX, nextY) is not None: continue
            positions.extend(self.__parseIntersection(layoutText, nextX, nextY, number))
        return positions

    def __parseCrossroad(self, layoutText, x, y, number):
        self.mapInfo.setCrossroad(x, y, number)
        positions = [(x, y)]
        for (nextX, nextY) in self.__getPosNearBy(x, y):
            if layoutText[nextY][nextX] != 'C': continue
            if self.mapInfo.get(nextX, nextY) is not None: continue
            positions.extend(self.__parseCrossroad(layoutText, nextX, nextY, number))
        return positions

    def __parseMap2(self, layoutText):
        for node in self.intersections + self.crossroads:
            # (x,y) of class intersecion/crossroad.
            # set up SNWE (Road) in map.
            for pos in node.getPostions():
                for (nextX, nextY) in self.__getPosNearBy(pos[0], pos[1]):
                    if self.mapInfo.get(nextX, nextY) is not None: continue
                    (testX, testY) = self.__getNextPos(nextX, nextY, layoutText[nextY][nextX])
                    if not (testX == pos[0] and testY == pos[1]):
                        number = len(self.roads)
                        (positions, ways) = self.__parseRoad(layoutText, nextX, nextY, number)
                        start = self.mapInfo.get(pos[0], pos[1])
                        end = positions.pop()
                        self.roads.append(Road(number, positions, ways, start, end))
                        self.__setInOutRoad(number, start, end)

    def __parseRoad(self, layoutText, x, y, number):
        self.mapInfo.setRoad(x, y, number)
        positions = [(x, y)]
        ways = [layoutText[y][x]]
        (nextX, nextY) = self.__getNextPos(x, y, layoutText[y][x])
        posInfo = self.mapInfo.get(nextX, nextY)
        if posInfo is None:
            (p, w) = self.__parseRoad(layoutText, nextX, nextY, number)
            positions.extend(p)
            ways.extend(w)
        else:
            positions.append(posInfo)
        return (positions, ways)

    def __setInOutRoad(self, number, start, end):
        if start[0] == Info.INTERSECTION:
            self.intersections[start[1]].addOutRoad(number)
        elif start[0] == Info.CROSSROAD:
            self.crossroads[start[1]].addOutRoad(number)
        if end[0] == Info.INTERSECTION:
            self.intersections[end[1]].addInRoad(number)
        elif end[0] == Info.CROSSROAD:
            self.crossroads[end[1]].addInRoad(number)

    def __getPosNearBy(self, x, y):
        positions = []
        move = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for m in move:
            nextX = x + m[0]
            nextY = y + m[1]
            if 0 <= nextX < self.width and 0 <= nextY < self.height:
                positions.append((nextX, nextY))
        return positions

    def __getNextPos(self, x, y, direction):
        if direction == 'N':
            return (x, y - 1)
        elif direction == 'S':
            return (x, y + 1)
        elif direction == 'E':
            return (x + 1, y)
        elif direction == 'W':
            return (x - 1, y)

    def getTrafficLights(self):
        return [(i.number, i.getInRoads()) for i in self.intersections]

# Call by Game?
def getLayout(name, back=2):
    if name.endswith('.lay'):
        layout = tryToLoad('layouts/' + name)
        if layout is None: layout = tryToLoad(name)
    else:
        layout = tryToLoad('layouts/' + name + '.lay')
        if layout is None: layout = tryToLoad(name + '.lay')
    if layout is None and back >= 0:
        curdir = os.path.abspath('.')
        os.chdir('..')
        layout = getLayout(name, back - 1)
        os.chdir(curdir)
    return layout

def tryToLoad(fullname):
    if not os.path.exists(fullname): return None
    f = open(fullname)
    try: return Layout([line.strip() for line in f])
    finally: f.close()

if __name__ == '__main__':
    l = getLayout('double_cross')
    # print('crossroads')
    # for c in l.crossroads:
    #     print(c.getPostions())
    # print('intersections')
    # for it in l.intersections:
    #     print(it.getPostions())
    #     print(it.getOutRoads())
    # print('roads')
    # for r in l.roads:
    #     print(r.getPostions())
        # print(r.getStart())
        # print(r.getEnd())
    print(l.getTrafficLights())
