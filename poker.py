import random

def generate_cards() -> list:
    cards = []
    for i in range(4):
        for j in range(1,14):
            if j == 1: j = 'A'
            elif j == 10: j = 'T'
            elif j == 11: j = 'J'
            elif j == 12: j = 'Q'
            elif j == 13: j = 'K'
            if i == 0: s = j.__str__() + '♠'
            elif i == 1: s = j.__str__() + '♥'
            elif i == 2: s = j.__str__() + '♦'
            else: s = j.__str__() + '♣'
            cards.append(s) 
    return cards  
        


class Player:
    def __init__(self,name:str,position:int,money:int = 200,label = None) -> None:
        self.name = name
        self.money = money
        self.label = label
        self.position = position
        self.tree = None
        self.hand = []
        self.score = 0
        pass
    
    def change_position(self) -> None:
        # To change the position after one game
        pass
        
    def learning(self) -> None:
        # Update decision tree
        pass
    
    def bet(self,money:int) -> int:
        # 
        return 0

class Game:

    def __init__(self,players_list:list[Player] = []) -> None:  
        self.cards = generate_cards()
        random.shuffle(self.cards)
        self.public_cards = []
        self.players = players_list
        self.players_num = len(players_list)
        self.card_position = 0
        self.pot = 0
        self.round = 0
        pass
    
    def new_game(self) -> None:
        random.shuffle(self.cards)
        self.card_position = 0
        self.pot = 0
        # change position 
        if self.round != 0:
            self.players.append(self.players.pop(0))
        self.round = 0
        
    def add_player(self,new:Player) -> None:
        self.players.insert(new.position,new)
        self.players_num += 1
        
    def delete_player(self,num:int) -> Player:
        if num > self.players_num:
            raise 'This play does not exist' 
        self.players_num -= 1
        return self.players.pop(num)
        
    
    def deal_card(self) -> None: 
        for i in range(2):
            for j in range(self.players_num):
                self.players[j].hand.append(self.cards[self.card_position])
                self.card_position += 1 
        return
 
    def deal_public_cards(self,num:int) -> None:
        if num == 3:
            self.card_position += 1
            for i in range(3):
                self.public_cards.append(self.cards[self.card_position])
                self.card_position += 1
        elif num == 1:
            self.card_position += 1
            self.public_cards.append(self.cards[self.card_position])
            self.card_position += 1
        return
    
    def action(self) -> None:
        for i in self.players:
            self.pot += i.bet()
            

    
        

if __name__ == "__main__":
    Jack = Player('Jack',1,300)
    Bob = Player('Bob',2,350)
    Amy = Player('Amy',3)
    Cat = Player('Cat',4)
    Dog = Player('Dog',5)
    players_list = [Jack,Bob,Amy]
    game = Game(players_list)
    game.delete_player(0)
    game.add_player(Jack)
    game.add_player(Cat)
    game.add_player(Dog)
    game.deal_card()
    for i in game.players:
        print(i.hand)
    game.deal_public_cards(3)
    print(game.public_cards)
    game.deal_public_cards(1)
    print(game.public_cards)
    game.deal_public_cards(1)
    print(game.public_cards)
    
    

                


