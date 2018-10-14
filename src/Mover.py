from Turner import *


class Mover:
    def __init__(self, state, turner):
        self.state = state
        self.turner = turner

    state: BotState = None
    turner: Turner = None
    x2 = 0
    y2 = 0
    finished = True
    callback = None

    def move(self, x2, y2, callback):
        #print("MOVE", x2, y2)
        self.finished = False
        self.x2 = x2
        self.y2 = y2
        self.callback = callback

    def update(self):
        if self.finished:
            return
        dst = get_distance(self.state.me['X'], self.state.me['Y'], self.x2, self.y2)
        if dst < 5:
            self.turner.stop()
            self.finished = True
            self.callback()
            return
        if self.turner.finished:
            self.turner.turn(self.x2, self.y2)
            return

    def stop(self):
        self.finished = True

    def restart(self):
        self.finished = False
