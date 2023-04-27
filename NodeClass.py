
import pickle


class ResultNode:
    def __init__(self):
        self.value = 0
        self.is_end = True
        pass

    def change_util(self, util):
        self.value = util
        pass


class DecisionNode():
    def __init__(self):
        self.is_end = False
        self.check_p = 0.2
        self.check = None
        self.call_p = 0.2
        self.call = None
        self.fold_p = 0.2

        self.bet = None
        self.bet_p = 0.2

        self.rs_1_3_p = 0.1
        self.rs_1_3 = None
        self.rs_3_5_p = 0.06
        self.rs_3_5 = None
        self.rs_5_p = 0.04
        self.rs_5 = None

        self.fold = None
        self.util = None

        self.value = 0
        self.over = False
        # by calling decisions[i] to decide which action to take
        # eg:decisions[0] means "check"
        self.decisions = [self.fold, self.check, self.call, self.bet,
                          self.rs_1_3, self.rs_3_5, self.rs_5]
        self.decisions_p = [self.fold_p, self.check_p, self.call_p,  self.bet_p,
                            self.rs_1_3_p, self.rs_3_5_p, self.rs_5_p]
        pass

    def extend_node(self):
        for i in range(1, len(self.decisions)):
            node = DecisionNode()
            self.decisions[i] = node
        util = ResultNode()
        self.decisions[0] = util
        pass

    def compute_value(self):
        self.value = self.decisions[0].value * self.decisions_p[0] + self.decisions[1].value * self.decisions_p[1] + self.decisions[2].value * self.decisions_p[2] + self.decisions[3].value * \
            self.decisions_p[3] + self.decisions[4].value * self.decisions_p[4] + \
            self.decisions[5].value * self.decisions_p[5] + \
            self.decisions[6].value * self.decisions_p[6]

    def change_p(self):
        average_value = 0
        sum_value = 0
        for i in range(len(self.decisions)):
            sum_value += self.decisions[i].value
        average_value = sum_value / len(self.decisions)
        diff_list = []
        for i in range(len(self.decisions_p)):
            diff = 0.0001*(self.decisions[i].value-average_value)
            diff_list.append(diff)

        if abs(min(diff_list)) <= min(self.decisions_p):
            for i in range(len(self.decisions_p)):
                self.decisions_p[i] += diff_list[i]
        elif abs(min(diff_list)) == 0:
            return
        else:
            factor = min(self.decisions_p) / abs(min(diff_list))
            diff_list = [factor * i for i in diff_list]
            for j in range(len(self.decisions_p)):
                self.decisions_p[j] += diff_list[j]

    def pass_value(self):
        for i in range(len(self.decisions)):
            self.decisions[i].value = self.value
            if self.decisions[i].is_end == False:
                self.decisions[i].pass_value()

    def update(self):
        if self.decisions[1].is_end == True:
            self.change_p()
            self.compute_value()
        else:
            for i in range(1, len(self.decisions)):
                self.decisions[i].update()
            self.change_p()
            self.compute_value()

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
            # create the dicisions after the first round
            self.nodes[i].extend_node()

        for i in range(169):
            for t in range(1, len(self.nodes[i].decisions)):
                # create the dicisions after the second round
                self.nodes[i].decisions[t].extend_node()

        for i in range(169):
            for t in range(1, len(self.nodes[i].decisions)):
                for j in range(1, len(self.nodes[i].decisions[t].decisions)):
                    self.nodes[i].decisions[t].decisions[j].extend_node(
                    )  # create the dicisions after the third round

        for i in range(169):
            for t in range(1, len(self.nodes[i].decisions)):
                for j in range(1, len(self.nodes[i].decisions[t].decisions)):
                    for n in range(1, len(self.nodes[i].decisions[t].decisions[j].decisions)):
                        self.nodes[i].decisions[t].decisions[j].decisions[n].extend_node(
                        )  # create the dicisons after the fourth round

        for i in range(169):
            for t in range(1, len(self.nodes[i].decisions)):
                for j in range(1, len(self.nodes[i].decisions[t].decisions)):
                    for n in range(1, len(self.nodes[i].decisions[t].decisions[j].decisions)):
                        for m in range(1, len(self.nodes[i].decisions[t].decisions[j].decisions)):
                            new_node = ResultNode()
                            self.nodes[i].decisions[t].decisions[j].decisions[n].decisions[m] = new_node

        for i in range(169):
            for t in range(1, len(self.nodes[i].decisions)):
                for j in range(1, len(self.nodes[i].decisions[t].decisions)):
                    for n in range(1, len(self.nodes[i].decisions[t].decisions[j].decisions)):
                        self.nodes[i].decisions[t].decisions[j].decisions[n].compute_value(
                        )

        for i in range(169):
            for t in range(1, len(self.nodes[i].decisions)):
                for j in range(1, len(self.nodes[i].decisions[t].decisions)):
                    self.nodes[i].decisions[t].decisions[j].compute_value()

        for i in range(169):
            for t in range(1, len(self.nodes[i].decisions)):
                self.nodes[i].decisions[t].compute_value()

        for i in range(169):
            self.nodes[i].compute_value()

    def update(self):
        for i in range(169):
            for t in range(1, len(self.nodes[i].decisions)):
                for j in range(1, len(self.nodes[i].decisions[t].decisions)):
                    for n in range(1, len(self.nodes[i].decisions[t].decisions[j].decisions)):
                        self.nodes[i].decisions[t].decisions[j].decisions[n].change_p()
                        self.nodes[i].decisions[t].decisions[j].decisions[n].compute_value(
                        )

        for i in range(169):
            for t in range(1, len(self.nodes[i].decisions)):
                for j in range(1, len(self.nodes[i].decisions[t].decisions)):
                    self.nodes[i].decisions[t].decisions[j].change_p()
                    self.nodes[i].decisions[t].decisions[j].compute_value()

        for i in range(169):
            for t in range(1, len(self.nodes[i].decisions)):
                self.nodes[i].decisions[t].change_p()
                self.nodes[i].decisions[t].compute_value()

        for i in range(169):
            self.nodes[i].change_p()
            self.nodes[i].compute_value()

    def store_p(self, filename:str):
        with open(filename, "wb") as f:
            for i in range(169):
                pickle.dump(self.nodes[i].decisions_p, f)
            for i in range(169):
                for t in range(1, len(self.nodes[i].decisions)):
                    pickle.dump(self.nodes[i].decisions[t].decisions_p, f)
            for i in range(169):
                for t in range(1, len(self.nodes[i].decisions)):
                    for j in range(1,len(self.nodes[i].decisions[t].decisions)):
                        pickle.dump(
                            self.nodes[i].decisions[t].decisions[j].decisions_p, f)
            for i in range(169):
                for t in range(1, len(self.nodes[i].decisions)):
                    for j in range(1, len(self.nodes[i].decisions[t].decisions)):
                        for n in range(1, len(self.nodes[i].decisions[t].decisions[j].decisions)):
                            pickle.dump(
                                self.nodes[i].decisions[t].decisions[j].decisions[n].decisions_p, f)
                            
            f.close()

    def read_p(self,filename:str):
        with open(filename, "rb") as f:
            for i in range(169):
                self.nodes[i].decisions_p = pickle.load(f)
            for i in range(169):
                for t in range(1, len(self.nodes[i].decisions)):
                    self.nodes[i].decisions[t].decisions_p = pickle.load(f)
            for i in range(169):
                for t in range(1, len(self.nodes[i].decisions)):
                    for j in range(1, len(self.nodes[i].decisions[t].decisions)):
                        self.nodes[i].decisions[t].decisions[j].decisions_p = pickle.load(
                            f)
            for i in range(169):
                for t in range(1, len(self.nodes[i].decisions)):
                    for j in range(1, len(self.nodes[i].decisions[t].decisions)):
                        for n in range(1, len(self.nodes[i].decisions[t].decisions[j].decisions)):
                            self.nodes[i].decisions[t].decisions[j].decisions[n].decisions_p = pickle.load(
                                f)
            f.close()
