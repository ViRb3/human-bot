import math

from BotState import BotState
from Mover import *
from Shooter import Shooter
from Turner import *
from TurretTurner import *
from Util import get_distance, is_uptodate


class BotActions:
    mover: Mover
    turner: Turner
    turretTurner: TurretTurner
    shooter: Shooter
    state: BotState

    edge1 = (70, 75)
    edge2 = (55, 90)
    edgePoints = [(62, 0), (0, 103), (-62, 0), (0, -103)]
    nextPoint = -1

    def __init__(self, state: BotState):
        self.state = state
        self.turner = Turner(state)
        self.turretTurner = TurretTurner(state)
        self.mover = Mover(state, self.turner)
        self.shooter = Shooter(state, self.turretTurner)

    def update(self):
        self.mover.update()
        self.turner.update()
        self.turretTurner.update()
        self.shooter.update()

    def wander(self):
        if not self.mover.finished:
            return False
        if self.nextPoint == -1:
            self.nextPoint = self.edgePoints.index(
                min(self.edgePoints, key=lambda k: get_distance(self.state.me['X'], self.state.me['Y'], k[0], k[1])))
        self.mover.move(self.edgePoints[self.nextPoint][0], self.edgePoints[self.nextPoint][1], self.next_loop)
        return True

    def next_loop(self):
        self.nextPoint = self.nextPoint + 1 if self.nextPoint < len(self.edgePoints) - 1 else 0
        self.wander()

    def go_ammo(self):
        asd = list(filter(lambda x: x['Type'] == 'AmmoPickup' and is_uptodate(x['time']),
                          self.state.game_objects.values()))
        #print(len(asd))
        #for x in asd:
            #print(x['X'], x['Y'])
        ammo_objs = list(map(lambda x: (x, get_distance(self.state.me['X'], self.state.me['Y'], x['X'], x['Y'])), asd))
        if len(ammo_objs) < 1:
            return False

        target = min(ammo_objs, key=lambda x: x[1])[0]
        self.mover.move(target['X'], target['Y'], self.empty)
        self.turretTurner.turn(target['X'], target['Y'])
        return True

    def empty(self):
        pass
