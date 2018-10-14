from datetime import datetime

import numpy as np

from API import *
from Util import get_distance


class BotState:
    game_server: ServerComms
    game_objects = {}
    me = None
    bot_name = ""
    snitch_holder_id = None

    def __init__(self, game_server, bot_name):
        self.game_server = game_server
        self.bot_name = bot_name

    def handle(self, message_type, message_payload):
        if message_type == ServerMessageTypes.OBJECTUPDATE:
            self.update_time(message_payload)
            self.update_mobility(message_payload)
            self.game_objects[message_payload['Name']] = message_payload
        elif message_type == ServerMessageTypes.DESTROYED:
            self.game_server.sendMessage(ServerMessageTypes.TOGGLEFORWARD)
        elif message_type == ServerMessageTypes.SNITCHPICKUP:
            self.snitch_holder_id = message_payload['Id']
        #print(message_payload)

        self.me = self.get_me()

    def get_me(self):
        if self.bot_name not in self.game_objects:
            return None
        return self.game_objects[self.bot_name]

    @staticmethod
    def update_time(message_payload):
        message_payload['time'] = datetime.now()

    def update_mobility(self, message_payload):
        name = message_payload['Name']
        if name not in self.game_objects:
            message_payload['mobility'] = 0  # TODO: Why tho
            return

        old_state = self.game_objects[name]
        dist = get_distance(message_payload['X'], message_payload['Y'], old_state['X'],
                            old_state['Y'])
        if 'mobility' not in message_payload:
            message_payload['mobility'] = dist
        else:
            message_payload['mobility'] = np.mean(message_payload['mobility'], dist)
