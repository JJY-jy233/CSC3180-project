import random
import numpy as np
import NodeClass
from State import State


class Player:
    def __init__(self,name:str,position:int,money:int = 10000,tree:NodeClass.RootNode = None,label = None) -> None:
        self.name = name
        self.money = money
        self.label = label
        self.position = position
        self.tree = tree
        self.hand = []
        self.score = None
        self.current_bet = 0
        self.p = None
        self.first_choice = None
        self.second_choice = None
        self.third_choice = None
        self.fourth_choice = None
        self.hand_num = None
        self.first_state:State = None
        self.second_state:State = None
        
        self.third_state:State = None
        self.fourth_state:State = None
        # self.is_fold = False
        # # self.is_bet = False
        # self.is_check = False
        # self.allow_check = True
        # self.state:state = None
        pass
    
    def change_position(self) -> None:
        # To change the position after one game
        pass
        
    def learn(self) -> None:
        # Update decision tree
        self.tree.nodes[self.hand_num]
        
        
        pass
    
    def small_blind(self,sb):
        self.current_bet = sb
        self.money -= sb
        
    def big_blind(self,bb):
        self.current_bet = bb
        self.money -= bb
    
    # 没人下注时 第一个下注的人
    def bet(self,max_bet:int) -> int:
        # rand
        bet_money = random.randint(1,50)
        if self.money > bet_money:
            self.money -= bet_money
            self.current_bet += bet_money
            # self.is_bet = True
            return bet_money
        else:
            allin = self.money
            self.current_bet += allin
            # self.money = 0
            return -3 # allin
    
    # def call(self,money:int) -> int:
    #     return money
    
    def Raise(self,max_bet:int,factors:int) -> int:
        
        if factors == 1:
            coefficient = random.choice([2,3])
        elif factors == 3:
            coefficient = random.choice([4,5])
        elif factors == 5:
            coefficient = random.choice([6,7])
        dif = coefficient * max_bet - self.current_bet
        if self.money > dif:
            self.money -= dif
            self.current_bet += dif
            return dif
        else:
            allin = self.money
            self.current_bet += allin
            # self.money = 0
            return -3
    
    def check(self) -> int:

        return -1
    
    def call(self,money:int) -> int:
        # 补差码
        dif = money - self.current_bet
        if self.money > dif:
            self.money -= dif
            self.current_bet += dif
            return dif
        else:
            allin = self.money
            self.current_bet += allin
            # self.money = 0
            return -3
    

    def fold(self) -> float:
        self.hand = []

        return -2
    
    def new_game(self)->None:
        pass
        # self.tree 
    
    def action(self,max_bet,round) -> float:
        
        # action_label = -1
        # search tree
        # step
        if round == 1:
           
            self.p_l = self.tree.nodes[self.hand_num].decisions_p
        elif round == 2:
            self.p_l = self.tree.nodes[self.hand_num].decisions[self.first_choice].decisions_p
        elif round == 3:
            self.p_l = self.tree.nodes[self.hand_num].decisions[self.first_choice].decisions[self.second_choice].decisions_p
            
        elif round == 4:
            self.p_l = self.tree.nodes[self.hand_num].decisions[self.first_choice].decisions[self.second_choice].decisions[self.third_choice].decisions_p
            
        # print(self.p_l)
        
        # self.hand

        # action_label = self.tree
        # random.choice(["check","call",'asd'])
        
        
        np.random.seed(0)
        # 没人下注的话，可以check和bet（一般不直接fold）S
        if((max_bet - self.current_bet)==0):
            sum = self.p_l[1] * (0.75) + winrate *0.25 + self.p_l[3]
            p = np.array([self.p_l[1] / sum, self.p_l[3] / sum])
            action_label = np.random.choice([1,3] , p = p.ravel())
            
        # 有人下注就不能check，只能fold，call，raise
        else:
            sum = self.p_l[0] + self.p_l[2] + self.p_l[4] + self.p_l[5] + self.p_l[6]
            p = np.array([self.p_l[0] / sum, self.p_l[2] / sum, self.p_l[4] / sum, self.p_l[5] / sum,self.p_l[6] / sum])
            action_label = np.random.choice([0,2,4,5,6] , p = p.ravel())
            # action_label = random.choice([0,3,4,5,6])
        # action_label = 4
        if round == 1:
           
            self.first_choice = action_label
        elif round == 2:
            self.second_choice = action_label

        elif round == 3:
            self.third_choice = action_label
            
        elif round == 4:
            self.fourth_choice = action_label
            
            

            
        if action_label == 0:
            money = self.fold()
        elif action_label == 1:
            money = self.check()
        elif action_label == 2:
            money = self.bet(2)
        elif action_label == 3:  # call
            money = self.call(max_bet)
        elif action_label == 4:
            money = self.Raise(max_bet,1)
        elif action_label == 5:
            money = self.Raise(max_bet,3)
        elif action_label == 6:
            money = self.Raise(max_bet,5)
        return money
        
    
    def get_max_score(self) -> None:
        
        return
