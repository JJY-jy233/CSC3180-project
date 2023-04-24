import pickle


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

    def store_p(self):
        with open('decision_data.pkl', 'wb') as f:
            for i in range(169):
                pickle.dump(self.nodes[i].decisions_p, f)
            for i in range(169):
                for t in range(len(self.nodes[i].decisions)):
                    pickle.dump(self.nodes[i].decisions[t].decisions_p, f)
            for i in range(169):
                for t in range(len(self.nodes[i].decisions)):
                    for j in range(len(self.nodes[i].decisions[t].decisions)):
                        pickle.dump(
                            self.nodes[i].decisions[t].decisions[j].decisions_p, f)
            for i in range(169):
                for t in range(len(self.nodes[i].decisions)):
                    for j in range(len(self.nodes[i].decisions[t].decisions)):
                        for n in range(len(self.nodes[i].decisions[t].decisions[j].decisions)):
                            pickle.dump(
                                self.nodes[i].decisions[t].decisions[j].decisions[n].decisions_p, f)

    def read_p(self):
        with open('decision_data.pkl', 'rb') as f:
            for i in range(169):
                self.nodes[i].decision_p = pickle.load(f)
            for i in range(169):
                for t in range(len(self.nodes[i].decisions)):
                    self.nodes[i].decisions[t].decisions_p = pickle.load(f)
            for i in range(169):
                for t in range(len(self.nodes[i].decisions)):
                    for j in range(len(self.nodes[i].decisions[t].decisions)):
                        self.nodes[i].decisions[t].decisions[j].decisions_p = pickle.load(f)
            for i in range(169):
                for t in range(len(self.nodes[i].decisions)):
                    for j in range(len(self.nodes[i].decisions[t].decisions)):
                        for n in range(len(self.nodes[i].decisions[t].decisions[j].decisions)):
                            self.nodes[i].decisions[t].decisions[j].decisions[n].decisions_p = pickle.load(f)


# root = RootNode()
# root.nodes[168].decisions[0].decisions[0].decisions[0].decisions_p[0]= 100
# root.store_p()
# root.read_p()
# print(root.nodes[168].decisions[0].decisions[0].decisions[0].decisions_p)
# root.nodes[0].decisions_p[1] = 1
# root.nodes[1].decisions_p[1] = 2

# print(
#     root.nodes[168].decisions[0].decisions[0].decisions[0].decisions[0].util.value)

# with open('decision_data.pkl', 'wb') as f:
#         pickle.dump(root.nodes[0].decisions_p, f)
#         pickle.dump(root.nodes[1].decisions_p, f)

# with open('decision_data.pkl', 'rb') as f:
#     data1 = pickle.load(f)
#     data2 = pickle.load(f)

# root.nodes[2]=data1

# print(data1,data2,root.nodes[2])

