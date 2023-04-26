import random
# import numpy as np
import NodeClass
from Player import Player
import time
from State import State
import MCCFR
from util import *

    

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
            self.players[i].position = i
            for j in range(4):
                self.players[i].states[j] = self.states[j]
        pass
    
    def is_terminal(self):
        if len(self.rest_players) == 1:
            return True
        if self.round == 5:
            return True
        return False
    

    def show_hand(self,player:Player = None) -> int:
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
            
            # 如果指定了玩家
            if player != None:
                # 如果这个玩家赢了
                if winners[0] == player:
                    return 1
                else:
                    return 0
            self.end_game(winners[0])
            return 0

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
                    # 如果指定了玩家
                    if player != None:
                        # 如果这个玩家赢了
                        if winners[0] == player:
                            return 1
                        else:
                            return 0
                    self.end_game(winners[0])
                    return 0
                
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
        
        # 清空手牌, 换位置
        
        for i in range(self.players_num):
            self.players[i].position = i
            self.players[i].hand = []
            
            
        
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
                # if (len(self.rest_players[j].hand)) > 2:
                #     print(self.rest_players[j].hand)
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
    
    def action(self,round,player:Player = None,simulate:int = -1) -> bool:
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
            
            # simulate
            if p == player:
                if simulate == 1: # check
                    if p.current_bet != max_bet: # 如果不能check了
                        return False
                elif simulate == 2: # call
                    if p.current_bet == max_bet: # 如果不能call，（别人还没有下注）
                        return False
                elif simulate == 3: # bet
                    if max_bet > 0: # 别人已经bet了，只能call或者raise
                        return False
                player_bet = p.action(max_bet,round,simulate)
                
            
            # 玩家的下注量 可能是负数（fold：-2，check：-1）
            else:
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
        return True    
            # update i matirx
        
            
            
    def action_first_round(self,player:Player = None,simulate:int = -1) -> None:
        for i in self.rest_players:
            i.current_bet = 0
        i = 2
        # smallblinder = self.rest_players[0]
        last_p = self.rest_players[1]
        # 
        self.rest_players[0].small_blind(self.smallblind)
        # self.states[0].legal_actions.append(['fold','call','raise'])
        # self.states[0].player_actions.append(['bet'])
        
        
        # 
        self.rest_players[1].big_blind(self.bigblind)
        # self.states[0].legal_actions.append(['raise'])
        
        check_last_p = self.rest_players[1]
        # last_talk_p = self.rest_players[1]
        self.pot = self.bigblind + self.smallblind
        self.states[0].round_pot += self.pot
        
        
        max_bet = self.bigblind
        self.states[0].max_bet = max_bet
        
        while len(self.rest_players) !=0:
            
            p = self.rest_players[i]
            
            # simulate
            if p == player:
                if simulate == 1: # check
                    if p.current_bet != max_bet: # 如果不能check了
                        return False
                elif simulate == 2: # call
                    if p.current_bet == max_bet and max_bet == 0: # 如果不能call，（别人还没有下注）
                        return False 
                elif simulate == 3: # bet
                    if max_bet > 0: # 别人已经bet了，只能call或者raise
                        return False
                player_bet = p.action(max_bet,1,simulate)
                
            
            # 玩家的下注量 可能是负数（fold：-2，check：-1）
            else:
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
        return True

            
            
    def end_game(self,player:Player) -> None:
        player.money += self.pot
        # print(player.name,'wins, now have:',player.money)
        for i in self.players:
            i.learn()
            
    
    def one_play(self):
        # 洗牌，清空彩池
        self.new_game()
        
        initial_money=[0] * self.players_num
        for i in range(self.players_num):
            initial_money[i] = self.players[i].money
        
        # 给每个玩家发手牌
        self.deal_card()

        
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
        self.deal_public_cards(1,3)
        
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
        self.deal_public_cards(1,4)
        
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
    # s = time.time()
    # # i = 0
    # for k in range(100):
    #     for l in game.players:
    #         l.money = 400
    #     for i in range(10):
    #         print("game: ",k*10+i)
    #         game.one_play()
    #         # time.sleep(3)
    #         i+=1
    #         sum = 0
    #         for j in game.players:
    #             sum += j.money
                
    #         if sum != 2000:
    #             print(sum)
    #             break

                
    # e = time.time()
    # print(e-s)
    game.deal_card()
    game.deal_public_cards(3,2)
    game.deal_public_cards(1,3)
    game.deal_public_cards(1,4)
    # Jack.hand_num = eval_hand(Jack.hand)
    print(Jack.hand_num)
    print(Jack.tree.nodes[Jack.hand_num].decisions[2].decisions[2].decisions[2].decisions[2].value)
    print(Jack.tree.nodes[Jack.hand_num].decisions[2].decisions[2].decisions[2].decisions[3].value)
    
# player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].decisions
    
    MCCFR.simulate_game(game,Jack,[400,400,400,400,400])
    print(Jack.tree.nodes[Jack.hand_num].decisions[2].decisions[2].decisions[2].decisions[2].value)
    print(Jack.tree.nodes[Jack.hand_num].decisions[2].decisions[2].decisions[2].decisions[3].value)
    

    
        
        

    

    
    

                


