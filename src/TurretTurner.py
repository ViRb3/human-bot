from BotState import *
from API import *
from Turner import *


class TurretTurner(Turner):
    msg = ServerMessageTypes.TURNTURRETTOHEADING

    @staticmethod
    def get_heading(self_object):
        return self_object['TurretHeading']
