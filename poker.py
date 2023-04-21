import random
from itertools import combinations
import NodeClass

def display_card(card_id:int) -> str:
    
    num = get_card_num_id(card_id)
    if num == 12: display = 'A'
    elif num == 8: display = 'T'
    elif num == 9: display = 'J'
    elif num == 10: display = 'Q'
    elif num == 11: display = 'K'
    else: display = str(num+2)
    
    suit = get_card_suit_id(card_id)
    if suit == 0: display += '♠'
    elif suit == 1: display += '♥'
    elif suit == 2: display += '♦'
    else: display += '♣'
    return display

def display_hand(hand:list) -> None:
    hand_display = []
    for i in hand:
        hand_display.append(display_card(i))
    print(hand_display)
    
# 8 同花顺：比最大的牌即可。牌型分就是最大牌的数字大小
# 7 四条：牌型分需要先比四条的数字，再比单牌的数字。所以牌型分是个二维的结构：（四条的数字, 单牌的数字）
# 6 葫芦：牌型分是个二维的结构：（三条的数字, 一对的数字）
# 5 同花：牌型分是个五维的结构，从大到小排列的5个牌的数字
# 4 顺子：牌型分就是最大牌的数字大小
# 3 三条：牌型分是个三维的结构：（三条的数字, 较大单牌的数字, 较小单牌的数字）
# 2 两对：牌型分是个三维的结构：（较大对子的数字, 较小对子的数字, 单牌的数字）
# 1 一对：牌型分是个三维的结构：（对子的数字, 最大单牌的数字, 第二大单牌的数字, 第三大单牌的数字）
# 0 高牌：牌型分是个五维的结构，从大到小排列的5个牌的数字

def is_flush(five_cards):
    s = get_card_suit_id(five_cards[0])
    for c in five_cards[1:]:
        if s != get_card_suit_id(c):
            return False
    return True

# 顺子：牌型分就是最大牌的数字大小
def is_straight(five_cards) -> tuple:
    nums = sorted([get_card_num_id(c) for c in five_cards])
    if nums == [0, 1, 2, 3, 12]:
        return True, [3]
    n4 = nums[4]
    for i, n in enumerate(nums[:4]):
        if n4 - n != 4 - i:
            return False, [0]
    return True, [n4]
    

def get_type(five_cards):
    straight, straight_value = is_straight(five_cards)
    flush = is_flush(five_cards)
    if flush and straight:
        return 8, straight_value
    if flush:
        return 5, None  # sorted([get_card_num_id(c) for c in five_cards], reverse=True)
    if straight:
        return 4, straight_value
    nums = [0] * 13
    for card in five_cards:
        nums[get_card_num_id(card)] += 1
    max_freq = max(nums)
    if max_freq == 1:
        return 0, None  # sorted([get_card_num_id(c) for c in five_cards], reverse=True)
    if max_freq == 4:
        return 7, None  # [nums.index(4), nums.index(1)]
    if max_freq == 3:
        if min(nums) == 2:
            return 6, None  # [nums.index(3), nums.index(2)]
        return 3, None
    # max_freq == 2
    if nums.count(2) == 1:
        return 1, None
    return 2, None

def get_value(t, v, five_cards):
    if v is not None:
        return v
    if t in (0, 5):
        return sorted((get_card_num_id(c) for c in five_cards), reverse=True)
    nums = [0] * 13
    for card in five_cards:
        nums[get_card_num_id(card)] += 1
    return sorted(list(set(get_card_num_id(c) for c in five_cards)), reverse=True, key=lambda x: (nums[x] << 5) + x)
    
def get_max_score(seven_cards:list) -> tuple:
    max_type = -1
    res = []
    for cards in combinations(seven_cards, 5):
        t, v = get_type(cards)
        if t > max_type:
            max_type = t
            res = [(t, v, cards)]
        elif t == max_type:
            res.append((t, v, cards))
    max_value = get_value(*res[0])
    for r in res[1:]:
        value = get_value(*r)
        if value > max_value:
            max_value = value
    return max_type, max_value

class Player:
    def __init__(self,name:str,position:int,money:int = 200,label = None) -> None:
        self.name = name
        self.money = money
        self.label = label
        self.position = position
        self.tree = None
        self.hand = []
        self.score = None
        pass
    
    def change_position(self) -> None:
        # To change the position after one game
        pass
        
    def learn(self) -> None:
        # Update decision tree
        pass
    
    def bet(self,money:int) -> int:
        # 
        return 0
    
    def Raise(self,money:int) -> int:
        
        return 0
    
    def check(self) -> None:
        return
    

    def fold(self) -> None:
        self.hand.clear()
        return
    
    def action(self) -> None:
        
        action_label = -1
        # search tree
        
        if action_label == 0:
            self.fold()
        elif action_label == 1:
            self.check()
        elif action_label == 2:
            self.bet(2)
        else:
            self.Raise(1)
        
        
    
    def get_max_score(self) -> None:
        
        return


class Game:

    def __init__(self,players_list:list[Player] = []) -> None:  
        
        # [0~51] 0:2♠ 1:2♥ .... 50: A♦ 51:A♣
        self.cards = [i for i in range(52)]
        random.shuffle(self.cards)
        self.public_cards = []
        self.players = players_list
        self.rest_players = players_list
        self.players_num = len(players_list)
        self.card_position = 0
        self.pot = 0
        self.round = 0
        pass
    
    def is_terminal(self):
        if len(self.rest_players) == 1:
            return True
        if self.round == 5:
            return True
        return False
    
# not finished
    def show_hand(self) -> None:
        biggest_type = -1
        for player in self.rest_players:
            seven_cards = self.public_cards + player.hand
            scores = get_max_score(seven_cards)
            player.score = scores
            if scores[0] > biggest_type:
                biggest_type = scores[0]
        
        # 最大牌型的玩家们
        winners = []
        for player in self.rest_players:
            if player.score[0] == biggest_type:
                winners.append(player)
        
        # 如果只有一个玩家具有最大牌型，独赢
        if len(winners) == 1:
            print(winners[0].name)
            self.end_game(winners[0])
            return

        # 如果有多个玩家具有最大牌型，比较
        r = len(winners[0].score[1])
        for i in range(r):
            high = -1   
            j = 0     
            while True:
                if high < winners[j].score[1][i]:
                    if high != -1:
                        
                        # 如果有一个牌比目前最大的牌大，清除winner里的人
                        winners = winners[j:]
                        j = 0
                    high = winners[j].score[1][i]
                    
                # 如果后面的牌没有目前最大的牌大，排除出winners
                elif high > winners[j].score[1][i]: 
                    winners.remove(winners[j])
                    j -= 1
                    
                # 如果只剩最后一个winner    
                if len(winners) == 1:
                    print(winners[0].name)
                    self.end_game(winners[0])
                    return
                
                # 遍历到最后一名玩家后 break
                if winners[j] == winners[-1]:
                    break                
                j+=1
        
        # 还没有分出胜负，平分彩池
        self.chop(winners)
        print("chop")
                
                    
            
    def chop(self,winners:list[Player]) -> None:
        part_pot = self.pot / len(winners)
        for winner in winners:
            winner.money += part_pot
            print(winner.name)
            
            
                
                
            
                    
    
    def new_game(self) -> None:
        random.shuffle(self.cards)
        self.rest_players = self.players.copy()
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
            # update i matirx
            
            
    def end_game(self,player:Player) -> None:
        player.money += self.pot
        for i in self.players:
            i.learn()
              
            

        
            
            
def get_card_suit_id(card_id):
    return card_id & 3

def get_card_num_id(card_id):
    return (card_id >> 2)
    
def oo(n1,n2):
    n1 += 1
    n2 += 2

if __name__ == "__main__":
    
    root = NodeClass.RootNode()
    Jack = Player('2',1,300)
    Bob = Player('1',2,350)
    Amy = Player('3',3)
    Cat = Player('4',4)
    Dog = Player('5',5)
    players_list = [Jack,Bob,Amy]
    game = Game(players_list)
    game.delete_player(0)
    game.add_player(Jack)
    game.add_player(Cat)
    game.add_player(Dog)
    game.deal_card()
    for i in game.players:
        print(i.name)
        display_hand(i.hand)
        
    game.deal_public_cards(3)
    display_hand(game.public_cards)
    game.deal_public_cards(1)
    display_hand(game.public_cards)
    
    game.deal_public_cards(1)
    display_hand(game.public_cards)
    
    game.show_hand()
    for i in game.players:
        print(i.score)
        
    # int("-------------------------------------------------------------------------------------------------------")
        
        

    

    
    

                


