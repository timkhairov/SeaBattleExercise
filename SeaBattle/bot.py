from random import random

from field import Point, Field


class Bot:
    class Target:
        def checkPoint(self, point):
            if not self.playerField.checkCoordinatesInField(point):
                return False

            if self.playerField.isTouched(point):
                return False

            return True

        def getPossibleDirections(self, point):
            directions = []

            for k in [-1, 1]:
                candidateDirection = Point(k, 0)
                if self.checkPoint(point + candidateDirection):
                    directions.append(candidateDirection)

                candidateDirection = Point(0, k)
                if self.checkPoint(point + candidateDirection):
                    directions.append(candidateDirection)

            return directions

        def __init__(self, point, playerField):
            self.points = [point]
            self.playerField = playerField
            self.possibleDirections = self.getPossibleDirections(point)
            self.currentDirection = self.possibleDirections.pop()
            self.isReversed = False

        def getPossiblePoint(self):
            if not self.isReversed:
                return self.currentDirection + self.points[-1]
            else:
                return self.currentDirection.multiplyWithNumber(-1) + self.points[0]

        def handleResult(self, result, targets):
            if result == "Killed":
                targets.pop()
                return False

            if result == "Wounded":
                if not self.isReversed:
                    self.points.append(self.getPossiblePoint())
                else:
                    self.points.insert(0, self.getPossiblePoint())

                if self.playerField.checkCoordinatesInField(self.getPossiblePoint()):
                    return True
                else:
                    targets.pop()
                    for point in self.points:
                        targets.append(Bot.Target(point, self.playerField))
                    return False

            if result == "Water":
                if len(self.points) == 1:
                    self.currentDirection = self.possibleDirections.pop()
                    if self.currentDirection is None:
                        targets.pop()
                        return False
                    else:
                        return True
                else:
                    if self.isReversed:
                        targets.pop()
                        for point in self.points:
                            targets.append(Bot.Target(point, self.playerField))
                        return False
                    else:
                        self.isReversed = True
                        if self.checkPoint(self.getPossiblePoint()):
                            return True
                        else:
                            targets.pop()
                            for point in self.points:
                                targets.append(Bot.Target(point, self.playerField))
                            return False


    def __init__(self, botField, playerField, ships):
        self.botField = botField
        self.playerField = playerField
        self.ships = ships
        self.targets = []

    def getPossibleEnds(self, start, ship):
        if ship.getLength() == 1:
            return [Point(start.y, start.x)]
        else:
            points = []
            for k in [-1, 1]:
                point = Point(start.y + k * (ship.getLength() - 1), start.x)
                if self.botField.checkCoordinatesInField(point):
                    points.append(point)

                point = Point(start.y, start.x + k * (ship.getLength() - 1))
                if self.botField.checkCoordinatesInField(point):
                    points.append(point)

            return points

    def initShips(self):
        for ship in self.ships:
            keepTrying = True
            while keepTrying:
                y = int(random() * self.botField.getHeight())
                x = int(random() * self.botField.getWidth())
                start = Point(y, x)
                possibleEnds = self.getPossibleEnds(start, ship)

                while len(possibleEnds) > 0:
                    possibleEnd = possibleEnds.pop(int(random() * len(possibleEnds)))
                    if self.botField.placeShip(ship, start, possibleEnd, False):
                        keepTrying = False
                        break

    def getShootingSolution(self):
        field = self.playerField

        y = int(random() * field.getHeight())
        x = int(random() * field.getWidth())

        if len(self.targets) > 0:
            targetPoint = self.targets[0].getPossiblePoint()
            x = targetPoint.x
            y = targetPoint.y
        else:
            while field.isTouched(Point(y, x)):
                y = int(random() * field.getHeight())
                x = int(random() * field.getWidth())

        return Field.getLetterByCoordinate(y) + str(x)

    def handleResult(self, result, pointString):
        if len(self.targets) > 0:
            self.targets[0].handleResult(result, self.targets)
        elif (result == "Wounded"):
            point = Field.parseCoordinates(pointString)
            self.targets.append(Bot.Target(point, self.playerField))

