from random import random

from bot import Bot
from field import Field
from field import Ship
from player import ShipPlacer

STATE_IDLE = 0
STATE_EXIT = -1
STATE_PLAYER_TURN = 1
STATE_BOT_TURN = 2
STATE_SETUP_PLAYER_SHIP = 3

WELCOME_MESSAGE = "Welcome to NavalBattle!"
IDLE_INSTRUCTION_MESSAGE = "To exit, type \"exit\", to start game, type \"game <height> <length>\""
START_GAME_MESSAGE = "Let the Battle begin!"
PLAYER_TURN_WELCOME_MESSAGE = "You turn, please select point to shoot, example: 'a1'"
BOT_TURN_MESSAGE = "Bot is making it's move: %s"
BOT_WON_MESSAGE = "Bot got you first. Live with this!"


botField = None
playerField = None
bot = None

playerShips = None
botShips = None


def initShips():
    ships = [
        Ship(4),
        Ship(3),
        Ship(3)#,
        # Ship(2),
        # Ship(2),
        # Ship(2),
        # Ship(1),
        # Ship(1)
    ]

    return ships


def checkIfHaveShipsAlive(ships):
    for ship in ships:
        if ship.checkIfAlive():
            return True
    return False


def initGame(height, width):
    global botField, playerField, botShips, playerShips, bot
    botField = Field(height, width)
    playerField = Field(height, width)

    playerShips = initShips()
    botShips = initShips()

    bot = Bot(botField, playerField, botShips)
    bot.initShips()


def handleGameCommand(userInput):
    parameters = userInput.split(" ")

    if len(parameters) == 3 and parameters[1].isnumeric() and parameters[2].isnumeric():
        initGame(int(parameters[1]), int(parameters[2]))
        ShipPlacer.startPlacement(playerShips, playerField)
        return STATE_SETUP_PLAYER_SHIP
    else:
        print(IDLE_INSTRUCTION_MESSAGE)
        return STATE_IDLE


def showPlayerTurnMessage():
    print(PLAYER_TURN_WELCOME_MESSAGE)


def doBotTurn():
    target = bot.getShootingSolution()
    print(BOT_TURN_MESSAGE % target)
    result = playerField.fire(target)
    bot.handleResult(result, target)
    print(result)
    printGameState()
    if checkIfHaveShipsAlive(playerShips):
        print(PLAYER_TURN_WELCOME_MESSAGE)
        return STATE_PLAYER_TURN
    else:
        print(BOT_WON_MESSAGE)
        return STATE_IDLE


def startGame():
    print(START_GAME_MESSAGE)
    printGameState()
    if random() < 0.5:
        showPlayerTurnMessage()
        return STATE_PLAYER_TURN
    else:
        return doBotTurn()


def printGameState():
    SEPARATOR = "     "
    playerFieldLines = playerField.toString(False).split("\n")
    botFieldLines = botField.toString(True).split("\n")
    lineLen = len(playerFieldLines[0])
    result = "Enemy field".center(lineLen) + SEPARATOR + "Your field".center(lineLen) + "\n"
    for i in range(len(playerFieldLines)):
        result = result + botFieldLines[i] + SEPARATOR + playerFieldLines[i] + "\n"
    print(result)




print(WELCOME_MESSAGE)
print(IDLE_INSTRUCTION_MESSAGE)
state = STATE_IDLE

while state != STATE_EXIT:
    userInput = input()

    if userInput == "exit":
        state = STATE_EXIT

    if state == STATE_IDLE:
        if userInput[:4] == "game":
            state = handleGameCommand(userInput)
        else:
            print(IDLE_INSTRUCTION_MESSAGE)

    elif state == STATE_SETUP_PLAYER_SHIP:
        if not ShipPlacer.handleAndCheckIfHasNext(userInput):
            state = startGame()

    elif state == STATE_PLAYER_TURN:
        print(botField.fire(userInput))
        if checkIfHaveShipsAlive(botShips):
            state = doBotTurn()
        else:
            print("You have won!")
            state = STATE_IDLE
