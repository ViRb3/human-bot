#!/usr/bin/python
from threading import Timer

from API import *
from BotActions import BotActions
from BotState import *
import datetime
import time

# Parse command line args
from Shooter import get_target

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
parser.add_argument('-H', '--hostname', default='192.168.44.109', help='Hostname to connect to')
parser.add_argument('-p', '--port', default=8052, type=int, help='Port to connect to')
parser.add_argument('-n', '--name', default='Human', help='Name of bot')
args = parser.parse_args()

# Set up console logging
if args.debug:
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

# Connect to game server
GameServer = ServerComms(args.hostname, args.port)

# Spawn our tank
logging.info("Creating tank with name '{}'".format(args.name))
GameServer.sendMessage(ServerMessageTypes.CREATETANK, {'Name': args.name})

state = BotState(GameServer, args.name)
state.game_server.sendMessage(ServerMessageTypes.TOGGLEFORWARD)
actions = BotActions(state)
#state.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": 10})

while True:
    (messageType, messagePayload) = GameServer.readMessage()
    state.handle(messageType, messagePayload)

    if state.me is None:
        continue

    actions.update()

    isAmmo = False
    if state.me['Ammo'] < 1:
        isAmmo = actions.go_ammo()

    if not isAmmo:
        actions.wander()

    target = get_target(state)
    if target is None:
        actions.shooter.stop()
    elif state.me['Ammo'] > 0:
        actions.shooter.shoot(target['X'], target['Y'])


