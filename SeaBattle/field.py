import math


class Point:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __str__(self):
        return f"({self.y}, {self.x})"

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)

    def __sub__(self, other):
        return Point(self.y - other.y, self.x - other.x)

    def round(self):
        return Point(round(self.y), round(self.x))

    def multiplyWithNumber(self, a):
        return Point(self.y * a, self.x * a)

    def length(self):
        return math.sqrt(self.y * self.y + self.x * self.x)


class Water:
    INTACT = "~"
    EMPTY = "0"

    def __init__(self, state):
        self.state = state

    def getSymbol(self, index):
        return Water.INTACT if self.state else Water.EMPTY

    def hit(self):
        self.state = False

    def getState(self):
        return self.state


class Ship:
    HIT = 0
    KILLED = 1

    def __init__(self, length):
        self.length = length
        self.state = [True for i in range(length)]

    def checkIfAlive(self):
        for cell in self.state:
            if cell:
                return True

        return False

    def isIntact(self, index):
        return self.state[index]

    def hit(self, index):
        if self.state[index]:
            self.state[index] = False
        if self.checkIfAlive():
            return Ship.HIT
        else:
            return Ship.KILLED

    def getSymbol(self, index):
        return "#" if self.state[index] else "*"

    def getLength(self):
        return self.length


class Field:
    class Cell:
        def __init__(self, point, content, index):
            self.point = point
            self.content = content
            self.index = index

        def __str__(self):
            return self.content.getSymbol(self.index)

        def toString(self, secure=False):
            if type(self.content) == Ship:
                if secure and self.content.isIntact(self.index):
                    return Water.INTACT
                else:
                    return self.content.getSymbol(self.index)
            else:
                return self.content.getSymbol(self.index)


    class WrongCoordinateException(Exception):
        def __init__(self, message):
            self.message = message

    def __init__(self, verticalSize, horizontalSize):
        self.__verticalSize = verticalSize
        self.__horizontalSize = horizontalSize
        self.field = [[Field.Cell(Point(i, j), Water(True), 0) for i in range(0, verticalSize)] for j in
                      range(0, horizontalSize)]

    def getHeight(self):
        return self.__verticalSize

    def getWidth(self):
        return self.__horizontalSize

    def getLetterByCoordinate(coordinate):
        return chr(ord('a')+coordinate)

    @staticmethod
    def parseCoordinates(coordinates):
        letter = coordinates[0]
        if not 'a' <= letter <= 'z':
            raise Field.WrongCoordinateException(f"First coordinate is not a letter: {coordinates}")
        number = coordinates[1:]
        if not number.isnumeric():
            raise Field.WrongCoordinateException(f"Second coordinate is not a number: {coordinates}")

        return Point(ord(letter) - ord('a'), int(number))

    def checkCoordinatesInField(self, point):
        return 0 <= point.y < self.__verticalSize and 0 <= point.x < self.__horizontalSize

    def getValue(self, point):
        return self.field[point.y][point.x]

    def setValue(self, point, value):
        self.field[point.y][point.x] = value

    def placeShip(self, ship, startCoordinates, endCoordinates, verbose=True):
        startPoint = startCoordinates
        endPoint = endCoordinates
        if type(startCoordinates) != Point:
            startPoint = Field.parseCoordinates(startCoordinates)
            endPoint = Field.parseCoordinates(endCoordinates)

        if not self.checkCoordinatesInField(startPoint):
            if verbose:
                print(f"Cannot place ship, point {startPoint} is out of the field")
            return False

        if not self.checkCoordinatesInField(endPoint):
            if verbose:
                print(f"Cannot place ship, point {endPoint} is out of the field")
            return False

        if startPoint.x != endPoint.x and startPoint.y != endPoint.y:
            if verbose:
                print(f"Cannot place ship, points {startPoint} and {endPoint} are not on a same line")
            return False

        if int((endPoint - startPoint).length()) + 1 != ship.getLength():
            if verbose:
                print("Cannot place ship, length not matches points")
            return False

        v = Point(0, 0)
        if (endPoint - startPoint).length() > 0:
            v = (endPoint - startPoint).multiplyWithNumber(1 / (endPoint - startPoint).length()).round()

        i = 0
        while v.multiplyWithNumber(i).length() <= ship.length-1 and not (
                v.length() == 0 and i > 0):
            point = startPoint + v.multiplyWithNumber(i)
            if type(self.getValue(point).content) != Water:
                if verbose:
                    print(f"Cannot place ship, point {point} is busy by another ship")
                return False
            i = i + 1

        i = 0

        while v.multiplyWithNumber(i).length() <= ship.length-1 and not (
                v.length() == 0 and i > 0):
            point = startPoint + v.multiplyWithNumber(i)

            self.setValue(point, Field.Cell(point, ship, i))
            i = i + 1

        return True

    def fire(self, coordinates):
        point = Field.parseCoordinates(coordinates)

        cell = self.getValue(point)

        if type(cell.content) == Water:
            cell.content.hit()
            return "Water"
        elif type(cell.content) == Ship:
            if cell.content.hit(cell.index) == Ship.HIT:
                return "Wounded"
            else:
                return "Killed"

    def isTouched(self, point):
        cell = self.getValue(point)

        if type(cell.content) == Water:
            return not Water(cell.content).state

        if type(cell.content) == Water:
            return not Ship(cell.content).isIntact(cell.index)

        return False

    def __str__(self):
        result = ""
        for line in self.field:
            for point in line:
                result = result + f" {point}"
            result = result + "\n"
        return result

    def toString(self, secure=False):
        result = "  "

        for x in range(self.getWidth()):
            result = result + " " + str(x)
        result = result + "\n"

        y = 0
        for line in self.field:
            result = result + str(Field.getLetterByCoordinate(y)) + " "
            y = y + 1

            for cell in line:
                result = result + f" {cell.toString(secure)}"
            result = result + "\n"
        return result
