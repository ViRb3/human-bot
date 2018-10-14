from datetime import *
from time import *

from TurretTurner import *
from BotState import *
from API import *
from Util import is_uptodate


def get_target(state: BotState):
    results = list(map(lambda x: get_score(state, x),
                       filter(
                           lambda x: x['Type'] == 'Tank' and x['Name'] != state.bot_name and is_uptodate(x['time']),
                           state.game_objects.values())))
    if len(results) < 1:
        return None
    return state.game_objects[min(results, key=lambda x: x[0])[1]]


def get_score(state: BotState, tank):
    score = tank['mobility'] * 50 + \
            get_distance(state.me['X'], state.me['Y'], tank['X'], tank['Y']) + \
            tank['Health'] * 100
    if state.snitch_holder_id == tank['Id']:
        score = 0  # GO KILL EM BOY
    # print(tank['Name'], score)
    return score, tank['Name']


class Shooter:
    def __init__(self, state, turner):
        self.state = state
        self.turretTurner = turner

    state: BotState = None
    turretTurner: TurretTurner = None
    x2 = 0
    y2 = 0
    finished = True

    def shoot(self, x2, y2):
        self.x2 = x2
        self.y2 = y2
        self.finished = False

    def update(self):
        if self.finished:
            return
        # if self.turner.finished:
        self.turretTurner.turn(self.x2, self.y2,
                               self.kill)

    def kill(self):
        # self.state.GameServer.sendMessage(ServerMessageTypes.STOPMOVE)
        self.state.game_server.sendMessage(ServerMessageTypes.FIRE)
        # self.state.GameServer.sendMessage(ServerMessageTypes.TOGGLEFORWARD)

    def stop(self):
        self.finished = True
