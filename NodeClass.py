# import os
# 目前手牌大小
def get_card_value():
    
    
    return

class Node:
    def __init__(self) -> None:
        self.node_util = 0.0
        pass
class DecisionNode(Node):
    def __init__(self) -> None:
        super.__init__()
        self.check_p = 0.166
        self.check = None
        
        self.call_p = 0.166
        self.call = None
        
        self.fold_p = 0.166
        
        self.rs_1_3_p = 0.166
        self.rs_3_5_p = 0.166
        self.rs_5_p = 0.166
        
        self.rs_1_3 = None
        self.rs_3_5 = None
        self.rs_5 = None
        
        self.end = False
        pass
    

# class RsNode(Node):
#     def __init__(self) -> None:
#         super.__init__()
        
#         self.one_three_p = 0.333
#         self.one_three = None
        
#         self.three_five_p = 0.333
#         self.three_five = None
        
#         self.over_five_p = 0.333
#         self.over_five = None
#         pass
    
# class BetNode(Node):
#     def __init__(self) -> None:
#         super.__init__()
        
#         self.call_p = 0.5*0.75
#         self.call = None
        
#         self.rs_p = 0.5
#         self.rs = None
    


class EvalNode:
    def __init__(self,card_value:int) -> None:
        self.hand = card_value
        self.big = DecisionNode()
        # self.big.call = DecisionNode()
        # self.mid = DecisionNode()
        self.small = DecisionNode()
        this = self.big
        for i in range(5):
            this.call = EvalNode()
            this = this.call 
        for i in range(5):
            this.check = EvalNode()
            this = this.check
        pass
    
    
class RootNode:
    def __init__(self) -> None:
        for i in range(169):
            exec('self.n{} = EvalNode({}) '.format(i,i))
        
        
    
# root = RootNode()

    