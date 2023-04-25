import random
import numpy as np
from itertools import combinations
import NodeClass
from Player import Player
import time
from State import State
def eval_hand(hand:list) -> int: #11 , 9 -> 1,3
    # l = [['AA','AKs','AQs','AJs','ATs','A9s','A8s','A7s','A6s','A5s','A4s','A3s','A2s'],
    #      ['AKo','KK','KQs','KJs','KTs','K9s','K8s','K7s','K6s','K5s','K4s','K3s','K2s'],
    #      ['AQo','KQo','QQ','QJs','QTs','Q9s','Q8s','Q7s','Q6s','Q5s','Q4s','Q3s','Q2s'],
    #      ['AJo','KJo','QJo','JJ','JTs','J9s','J8s','J7s','J6s','J5s','J4s','J3s','J2s'],
    #      ['ATo','KTo','QTo','JTo','TT','T9s','T8s','T7s','T6s','T5s','T4s','T3s','T2s'],
    #      ['A9o','K9o','Q9o','J9o','T9o','99','98s','97s','96s','95s','94s','93s','92s'],
    #      ['A8o','K8o','Q8o','J8o','T8o','98o','88','87s','86s','85s','84s','83s','82s'],
    #      ['A7o','K7o','Q7o','J7o','T7o','97o','87o','77','76s','75s','74s','73s','72s'],
    #      ['A6o','K6o','Q6o','J6o','T6o','96o','86o','76o','66','65s','64s','63s','62s'],
    #      ['A5o','K5o','Q5o','J5o','T5o','95o','85o','75o','65o','55','54s','53s','52s'],
    #      ['A4o','K4o','Q4o','J4o','T4o','94o','84o','74o','64o','54o','44','43s','42s'],
    #      ['A3o','K3o','Q3o','J3o','T3o','93o','83o','73o','63o','53o','43o','33','32s'],
    #      ['A2o','K2o','Q2o','J2o','T2o','92o','82o','72o','62o','52o','42o','32o','22'],]
    hand.sort()
    a = get_card_suit_id(hand[0])
    b = get_card_suit_id(hand[1]) 
    big = get_card_num_id(hand[0]) # 0-12
    small = get_card_num_id(hand[1])

    i = 12 - big
    j = 12 - small         
    if a == b: # suit
        return j * 13 + i
    else: 
        return i * 13 + j
    

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



    

class Game:

    def __init__(self,players_list:list[Player] = [],bigblind:int = 2,smallblind:int = 1) -> None:  
        
        # [0~51] 0:2♠ 1:2♥ .... 50: A♦ 51:A♣
        self.cards = [i for i in range(52)]
        random.shuffle(self.cards)
        self.public_cards = []
        self.players = players_list
        self.rest_players = self.players.copy()
        self.players_num = len(players_list)
        self.card_position = 0
        self.pot = 0
        self.round = 0
        self.bigblind = bigblind
        self.smallblind = smallblind
        self.allin = []
        self.states:list[State] = []
        for i in range(4):
            self.states.append(State())
        for i in range(self.players_num):
            for j in range(4):
                self.players[i].states[j] = self.states[j]
        pass
    
    def is_terminal(self):
        if len(self.rest_players) == 1:
            return True
        if self.round == 5:
            return True
        return False
    

    def show_hand(self) -> None:
        # allin的人
        
        for i in range(len(self.allin)):
            self.rest_players.append(self.allin.pop(0))
        
        self.rest_players = list(set(self.rest_players))
        biggest_type = -1
        for player in self.rest_players:
            seven_cards = self.public_cards + player.hand
            scores = get_max_score(seven_cards)
            player.score = scores
            if scores[0] > biggest_type:
                biggest_type = scores[0]
        
        # 最大牌型的玩家们
        winners:list[Player] = []
        for player in self.rest_players:
            if player.score[0] == biggest_type:
                winners.append(player)
        
        # 如果只有一个玩家具有最大牌型，独赢
        if len(winners) == 1:
            # print(winners[0].name)
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
                    # print(winners[0].name)
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
        # winners = list(set(winners))
        part_pot = self.pot / len(winners)
        print(self.pot,"part",part_pot,"WINNER LEN",len(winners))
        self.pot = 0
        for winner in winners:
            winner.money += part_pot
            print(winner.name,winner.score)
            
            
      
                    
    
    def new_game(self) -> None:
        # 换位置
        # if self.round != 0:
        self.players.append(self.players.pop(0))
            
        # 洗牌
        random.shuffle(self.cards)
        
        # 清空手牌
        for i in self.players:
            i.hand = []
            
            
        
        self.rest_players = self.players.copy()
        self.card_position = 0
        self.pot = 0
        self.public_cards = []
        # change position 
        # self.round = 0
        
    
    # 玩家进场 
    def add_player(self,new:Player) -> None:
        self.players.insert(new.position,new)
        self.players_num += 1
        
    # 玩家离场，num：index of player
    def delete_player(self,num:int) -> Player:
        if num > self.players_num:
            raise 'This play does not exist' 
        self.players_num -= 1
        return self.players.pop(num)
        
    # 发手牌
    def deal_card(self) -> None: 
        for i in range(2):
            for j in range(self.players_num):
                self.rest_players[j].hand.append(self.cards[self.card_position])
                if (len(self.rest_players[j].hand)) > 2:
                    print(self.rest_players[j].hand)
                self.card_position += 1 
        for k in range(self.players_num):
            self.rest_players[k].hand_num = eval_hand(self.rest_players[k].hand)
        return
 
    # num：发几张公牌
    def deal_public_cards(self,num:int,round:int) -> None:
        if num == 3:
            # 切一张牌
            self.card_position += 1
            for i in range(3):
                self.public_cards.append(self.cards[self.card_position])
                self.states[1].public_cards.append(self.cards[self.card_position])
                self.card_position += 1
            
        elif num == 1:
            self.card_position += 1
            self.public_cards.append(self.cards[self.card_position])
            if round == 3:
                self.states[2].public_cards = self.public_cards.copy()
            elif round == 4:
                self.states[3].public_cards = self.public_cards.copy()
            self.card_position += 1
        return
    
    def action(self,round) -> None:
        for i in self.rest_players:
            i.current_bet = 0
        i = 0
        # smallblinder = self.rest_players[0]
        last_p = self.rest_players[-1]
        check_last_p = self.rest_players[-1]
        # current_bet = 0
        max_bet = 0
        while len(self.rest_players) !=0:
            
            p = self.rest_players[i]

            
            
            # 玩家的下注量 可能是负数（fold：-2，check：-1）
            player_bet = p.action(max_bet,round)
            self.pot += max(0,player_bet)
            
            # # 当前一轮最大下注筹码
            # current_bet = max(player_bet,current_bet)
            # 当前一轮最大下注筹码
            if player_bet > max_bet:
                max_bet = player_bet
                # 都allinle
                if len(self.rest_players) == 0:
                    break
                last_p = self.rest_players[(i+len(self.rest_players)-1)%len(self.rest_players)]
            
            # 弃牌，
            if player_bet == -2:
                self.rest_players.remove(p)
                # print(p.name,"fold")
                i-=1
            
            # allin
            elif player_bet == -3:
                self.rest_players.remove(p)
                self.allin.append(p)
                i-=1
            
            if(len(self.rest_players) == 1 and len(self.allin) == 0):
                break
            
            
            
            # 到最后一个人说完话时，这一轮结束
            if p == last_p:
                break
            
            
            # check后，此玩家跳过，放到最后一个人说话
            if player_bet == -1:
                # self.rest_players.append(self.rest_players.pop(0))

                # 所有人check结束本回合
                if check_last_p == p:
                    break

                last_p = p
                # i-=1
            i+=1   
            if i > (len(self.rest_players) - 1):
                i = 0
            
            # update i matirx
        
            
            
    def action_first_round(self) -> None:
        for i in self.rest_players:
            i.current_bet = 0
        i = 2
        # smallblinder = self.rest_players[0]
        last_p = self.rest_players[1]
        # 
        self.rest_players[0].small_blind(self.smallblind)
        self.states[0].legal_actions.append(['fold','call','raise'])
        self.states[0].player_actions.append(['bet'])
        
        
        # 
        self.rest_players[1].big_blind(self.bigblind)
        self.states[0].legal_actions.append(['raise'])
        
        check_last_p = self.rest_players[1]
        # last_talk_p = self.rest_players[1]
        self.pot = self.bigblind + self.smallblind
        self.states[0].round_pot += self.pot
        
        
        max_bet = self.bigblind
        self.states[0].max_bet = max_bet
        
        while len(self.rest_players) !=0:
            
            p = self.rest_players[i]
            
            # 玩家的下注量 可能是负数（fold：-2，check：-1）
            player_bet = p.action(max_bet,1)
            self.pot += max(0,player_bet)
            self.states[0].round_pot += max(0,player_bet)
            
            
             # 当前一轮最大下注筹码
            if p.current_bet > max_bet:
                max_bet = p.current_bet
                self.states[0].max_bet = p.current_bet
                
                if len(self.rest_players) == 0:
                    break
                last_p = self.rest_players[(i+len(self.rest_players)-1)%len(self.rest_players)]
               
            
            # allin
            if player_bet == -3:
                self.rest_players.remove(p)
                self.allin.append(p)
                self.pot += p.money
                player_bet = p.current_bet
                p.money = 0
                i-=1
            # 弃牌，
            elif player_bet == -2:
                self.rest_players.remove(p)
                # print(p.name,"fold")
                i-=1
                
            if(len(self.rest_players) == 1 and len(self.allin) == 0):
                break
                
                
            # 到最后一个人说完话时，这一轮结束
            if p == last_p:
                break
            
            
            # check后，此玩家跳过，放到最后一个人说话
            if player_bet == -1:
                # self.rest_players.append(self.rest_players.pop(0))
                if check_last_p == p:
                    break
                last_p = p
                # i-=1
            i+=1   
            if i > (len(self.rest_players) - 1):
                i = 0
            
            # update i matirx
        
        # 恢复说话顺序
        # if check_count != len(self.rest_players):
        #     for i in range(check_count):
        #         self.rest_players.insert(0,self.rest_players.pop())
            
            
    def end_game(self,player:Player) -> None:
        player.money += self.pot
        # print(player.name,'wins, now have:',player.money)
        for i in self.players:
            i.learn()
            
    
    def one_play(self):
        # 洗牌，清空彩池
        self.new_game()
        if self.pot != 0:
            print('1',self.pot)
        
        # 给每个玩家发手牌
        self.deal_card()
        if self.pot != 0:
            print('2',self.pot)
        
        # 第一轮下注
        self.action_first_round()
    
        
        # 如果只剩一个玩家了，独赢
        if len(self.rest_players) == 1:
            # if
            self.end_game(self.rest_players[0])
            return
        elif len(self.rest_players) == 0 and len(self.allin) != 0:
            self.deal_public_cards(3)
            self.deal_public_cards(1)
            self.deal_public_cards(1)
            
            self.show_hand()
            return
        
        # 发三张公牌
        self.deal_public_cards(3,0)
        
        # 第二轮下注
        self.action(2)
        
        if len(self.rest_players) == 1:
            self.end_game(self.rest_players[0])
            return
        elif len(self.rest_players) == 0 and len(self.allin) != 0:
            self.deal_public_cards(1)
            self.deal_public_cards(1)
            self.show_hand()
            return
        
        # 发转牌
        self.deal_public_cards(1,1)
        
        # 第三轮下注
        self.action(3)
        
        if len(self.rest_players) == 1:
            self.end_game(self.rest_players[0])
            return
        elif len(self.rest_players) == 0 and len(self.allin) != 0:
            self.deal_public_cards(1)
            self.show_hand()
            return
        
        # 发河牌
        self.deal_public_cards(1,2)
        
        # 第四轮下注
        self.action(4)
        
        if len(self.rest_players) == 1:
            self.end_game(self.rest_players[0])
            return
        elif len(self.rest_players) == 0 and len(self.allin) != 0:
            self.show_hand()
            return
        
        # show hand
        self.show_hand()
        return
        

        

        
              
            

        
            
            
def get_card_suit_id(card_id):
    return card_id & 3

def get_card_num_id(card_id):
    return (card_id >> 2)
    
def oo(n1,n2):
    n1 += 1
    n2 += 2

if __name__ == "__main__":
    
    root = NodeClass.RootNode()
    Jack = Player('1',1,400,root)
    Bob = Player('2',2,400,root)
    Amy = Player('3',3,400,root)
    Cat = Player('4',4,400,root)
    Dog = Player('5',5,400,root)
    players_list = [Jack,Bob,Amy,Cat,Dog]
    game = Game(players_list)
    # game.delete_player(0)
    # game.add_player(Jack)
    # game.add_player(Cat)
    # game.add_player(Dog)
    # game.deal_card()
    # for i in game.players:
    #     i.action()
    # for i in game.players:
    #     print(i.name)
    #     display_hand(i.hand)
        
    # game.deal_public_cards(3)
    # display_hand(game.public_cards)
    # game.deal_public_cards(1)
    # display_hand(game.public_cards)
    
    # game.deal_public_cards(1)
    # display_hand(game.public_cards)
    
    # game.show_hand()
    # for i in game.players:
    #     print(i.score)
    s = time.time()
    # i = 0
    for k in range(100):
        for l in game.players:
            l.money = 400
        for i in range(10):
            print("game: ",k*10+i)
            game.one_play()
            # time.sleep(3)
            i+=1
            sum = 0
            for j in game.players:
                sum += j.money
                
            if sum != 2000:
                print(sum)
                break

                
    e = time.time()
    print(e-s)
    # np.random.seed(0)
    # p = np.array([0.1 / 0.4,0.3 / 0.4])
    # for i in range(20):
    #     print(np.random.choice([1,2] , p = p.ravel()))
    # hand = [5,45]
    # print(eval_hand(hand))
    # display_hand(hand)
    # int("-------------------------------------------------------------------------------------------------------")
        
        

    

    
    

                


