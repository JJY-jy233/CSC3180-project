class State:
    def __init__(self):
        self.legal_actions = []
        self.player_actions = []
        self.public_cards = []
        
        self.max_bet = 0
        self.round_pot = 0
        pass
    
    def clear(self):
        self.legal_actions = []
        self.player_actions = []
        self.public_cards = []
        
        self.max_bet = 0
        self.round_pot = 0
        pass