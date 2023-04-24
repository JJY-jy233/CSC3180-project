# import os
# 目前手牌大小
# def get_card_value():


#     return

class ResultNode:
    def __init__(self):
        self.value = 0
        pass

    def change_util(self, util):
        self.value = util
        pass


class DecisionNode():
    def __init__(self):

        self.check_p = 0.166
        self.check = None
        self.call_p = 0.166
        self.call = None
        self.fold_p = 0.166
        self.rs_1_3_p = 0.166
        self.rs_1_3 = None
        self.rs_3_5_p = 0.166
        self.rs_3_5 = None
        self.rs_5_p = 0.166
        self.rs_5 = None

        self.util = None
        self.over = False
        # by calling decisions[i] to decide which action to take
        # eg:decisions[0] means "check"
        self.decisions = [self.check, self.call,
                          self.rs_1_3, self.rs_3_5, self.rs_5]
        self.decisions_p = [self.check_p, self.call_p,
                            self.rs_1_3_p, self.rs_3_5_p, self.rs_5_p]
        pass

    def extend_node(self, node):
        for i in range(len(self.decisions)):
            self.decisions[i] = node
        pass

    # def extend_resultnode(self, node):
    #     for i in range(len(self.decisions)):
    #         self.decisions[i] = node
    #     pass
    # def extend_final_node(self, node, resultNode):
    #     self.check = node
    #     self.check.util = resultNode
    #     self.call = node
    #     self.check.util = resultNode
    #     self.rs_1_3 = node
    #     self.check.util = resultNode
    #     self.rs_3_5 = node
    #     self.check.util = resultNode
    #     self.rs_5 = node
    #     self.check.util = resultNode

    def change_possibility(self, possibility):
        pass


# class EvalNode:
#     def __init__(self, card_value):
#         self.hand = card_value
#         self.big = None
#         self.small = None

#     def extend_node(self, node):
#         self.big = node
#         self.small = node


class RootNode:
    def __init__(self):
        self.nodes = []
        for i in range(169):
            node = DecisionNode()
            self.nodes.append(node)  # create the dicisions at the begining

        for i in range(169):
            new_node = DecisionNode()
            # create the dicisions after the first round
            self.nodes[i].extend_node(new_node)

        for i in range(169):
            new_node = DecisionNode()
            for t in range(len(self.nodes[i].decisions)):
                # create the dicisions after the second round
                self.nodes[i].decisions[t].extend_node(new_node)

        for i in range(169):
            new_node = DecisionNode()
            for t in range(len(self.nodes[i].decisions)):
                for j in range(len(self.nodes[i].decisions[t].decisions)):
                    self.nodes[i].decisions[t].decisions[j].extend_node(
                        new_node)  # create the dicisions after the third round

        for i in range(169):
            new_node = DecisionNode()
            for t in range(len(self.nodes[i].decisions)):
                for j in range(len(self.nodes[i].decisions[t].decisions)):
                    for n in range(len(self.nodes[i].decisions[t].decisions[j].decisions)):
                        self.nodes[i].decisions[t].decisions[j].decisions[n].extend_node(
                            new_node)  # create the dicisons after the fourth round

        for i in range(169):
            new_node = ResultNode()
            for t in range(len(self.nodes[i].decisions)):
                for j in range(len(self.nodes[i].decisions[t].decisions)):
                    for n in range(len(self.nodes[i].decisions[t].decisions[j].decisions)):
                        for m in range(len(self.nodes[i].decisions[t].decisions[j].decisions)):
                            self.nodes[i].decisions[t].decisions[j].decisions[n].decisions[m].util = new_node


# class Tree:
#     def __init__(self):
#         root = RootNode
#         pass
root = RootNode()

print(
    root.nodes[168].decisions[0].decisions[0].decisions[0].decisions[0].util.value)
