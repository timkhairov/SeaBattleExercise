from random import random


class ShipPlacer: #singletone for ship placement
    SETUP_PLAYER_SHIP_MESSAGE = "Please, set the ship with length %d. To set it up type start and end points. Example: 'a1 a3'"

    __instance = None

    def __init__(self, ships, field):
        self.index = 0
        self.ships = ships
        self.field = field

    @staticmethod
    def startPlacement(ships, field):
        ShipPlacer.__instance = ShipPlacer(ships, field)
        ShipPlacer.__instance.showWelcomeMessage()

    def showWelcomeMessage(self):
        print(self.field.toString(False))
        print(ShipPlacer.SETUP_PLAYER_SHIP_MESSAGE % (self.ships[self.index].getLength()))

    def handleInputAndCheckIfHasNext(self, userInput):
        if self.index < len(self.ships):
            coordinates = userInput.split(" ")
            if len(coordinates) != 2:
                print("Wrong input")
                self.showWelcomeMessage()
                return True
            elif self.field.placeShip(self.ships[self.index], coordinates[0], coordinates[1]):
                self.index = self.index + 1
                if self.index < len(self.ships):
                    self.showWelcomeMessage()
                    return True
                else:
                    return False
            else:
                self.showWelcomeMessage()
                return True
        else:
            return False

    @staticmethod
    def handleAndCheckIfHasNext(userInput):
        return ShipPlacer.__instance.handleInputAndCheckIfHasNext(userInput)



