# -*- coding: utf-8 -*-

import config

class WhiteLister:

    def __init__(self):
        self.whitelist = {config.tid : config.ctoken, config.atid : '543c1eb9c9d04cf9b318cff5968c4ec63bf3015b'}
        
        self.acclist = {config.ctoken : '324', config.actoken : '594'}
        #todo: заполнять из autocomplete

        self.states = {}


    def get_account_id (self, chat_id):
        return self.acclist.get(chat_id)

    def get_account_token (self, chat_id):
        return self.whitelist.get(chat_id)

    def update_whitelist(self, chat_id, token):
        new = {chat_id: token}
        self.whitelist.update(new)

    def update_states(self, chat_id, state):
        new = {chat_id: state}
        self.states.update(new)

    def clear_states(self, chat_id):
        self.states.pop(chat_id)

    def get_states(self, chat_id):
        return self.states.get(chat_id)

