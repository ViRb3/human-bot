import math

from BotState import *
from API import *


def radian_to_degree(angle):
    return angle * (180.0 / math.pi)


def get_heading(x1, y1, x2, y2):
    heading = math.atan2(y2 - y1, x2 - x1)
    heading = radian_to_degree(heading)
    heading = math.fmod((heading - 360), 360)
    return abs(heading)


class Turner:
    def __init__(self, state):
        self.state = state

    turret = False
    state: BotState = None
    x2 = 0
    y2 = 0
    finished = False
    callback = None
    msg = ServerMessageTypes.TURNTOHEADING

    def turn(self, x2, y2, callback=None):
        self.finished = False
        self.x2 = x2
        self.y2 = y2
        self.callback = callback

    def update(self):
        if self.finished:
            self.state.game_server.sendMessage(ServerMessageTypes.TOGGLETURRETLEFT)
            return
        if self.looking_at(self.x2, self.y2):
            self.finished = True
            if self.callback is not None:
                self.callback()
        else:
            self.turn_to_heading(self.x2, self.y2)

    def stop(self):
        self.finished = True

    def restart(self):
        self.finished = False

    def looking_at(self, x2, y2):
        heading = self.get_heading(self.state.me)
        target_heading = get_heading(self.state.me['X'], self.state.me['Y'], x2, y2)
        dif = abs(heading - target_heading)
        if dif > 5:
            return False
        return True

    @staticmethod
    def get_heading(self_object):
        return self_object['Heading']

    def turn_to_heading(self, x2, y2):
        heading = get_heading(self.state.me['X'], self.state.me['Y'], x2, y2)
        self.state.game_server.sendMessage(self.msg, {"Amount": heading})
