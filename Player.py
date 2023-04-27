import random
import numpy as np
import NodeClass
from State import State
# import Matrix_class

import math
# from Player import Player
from util import *

class Matrix:
    def __init__(self,player = None):
        self.matrix = [[1]*(13) for _ in range(13)]
        self.precentage_sum = 13*13
        self.owner:Player = player

        self.upper_precentage_sum = 12+12*11/2
        self.lower_precentage_sum = 13+13*12/2

        self.curve_index = 60
        self.nd_power = 5
        self.one_pair_position_index = 0.25
        self.two_pair_position_index = 1.0
        self.three_of_kind_position_index = 1.5
        self.straight_position_index = 2.0
        self.full_house_position_index = 2.5
        self.four_of_the_kind_position_index = 2.75

        self.winning_posibility_matrix = [[30.8, 19.8, 18.2, 17.0, 16.1, 14.1, 13.4, 12.9, 12.5, 12.9, 12.8, 12.6, 12.4],
                                          [16.2, 25.8, 17.6, 16.5, 15.7, 13.7, 12.4,
                                              11.9, 11.5, 11.2, 11.1, 11.0, 10.9],
                                          [14.5, 14.1, 21.9, 16.1, 15.3, 13.4, 12.0,
                                              10.9, 10.5, 10.2, 10.1, 10.1, 10.0],
                                          [13.1, 12.8, 12.5, 18.9, 15.3, 13.4, 12.1,
                                              10.9, 9.84, 6.58, 9.47, 9.41, 9.32],
                                          [12.0, 11.8, 11.6, 11.8, 16.6, 13.6, 12.3,
                                              11.1, 9.98, 9.01, 8.90, 8.83, 8.77],
                                          [9.93, 9.69, 9.55, 9.71, 10.1, 15.2, 12.3,
                                              11.4, 10.3, 9.32, 8.44, 8.36, 8.28],
                                          [9.16, 8.22, 8.07, 8.26, 8.67, 8.74, 14.1,
                                              11.7, 10.8, 9.85, 8.90, 8.06, 7.94],
                                          [8.56, 7.65, 6.79, 6.91, 7.32, 7.76, 8.14,
                                              13.2, 11.2, 10.4, 9.52, 5.58, 7.74],
                                          [8.11, 7.25, 6.38, 5.76, 6.11, 6.59, 7.22,
                                              7.70, 12.6, 10.9, 10.1, 9.27, 8.32],
                                          [8.60, 6.91, 6.10, 5.49, 5.05, 5.47, 6.15,
                                              6.85, 7.37, 12.0, 10.6, 9.97, 9.06],
                                          [8.43, 9.78, 5.98, 5.35, 4.88, 4.55, 5.09,
                                              5.86, 6.62, 7.20, 11.8, 9.61, 8.92],
                                          [8.27, 6.69, 5.87, 5.29, 4.82, 4.42, 4.42,
                                              4.84, 5.65, 6.42, 6.05, 11.8, 8.59],
                                          [7.96, 6.60, 5.81, 5.23, 4.76, 4.37, 4.11, 3.98, 4.63, 5.47, 5.31, 4.97, 11.8]]

        pass

    def valueable_func(self, wager, current_deposit, initial_deposit):  # 衡量这笔下注对玩家有多重要
        return wager*(initial_deposit/current_deposit + 1)*0.5

    def return_possibility(self, row, col):
        if col > row:
            return self.matrix[row][col]/self.upper_precentage_sum
        else:
            return self.matrix[row][col]/self.lower_precentage_sum


    def curve_process(self, wager):  # 转化为一个Lim等于2的func
        curve_index = self.curve_index
        return 2-(curve_index/(wager + curve_index/2))

    # 将正态分布函数在0-2中移动以显示哪个值上的可能性较高
    def normal_distribution_process(self, wager, position_index):
        return 1+self.nd_power**((1+self.curve_process(wager))*math.exp(-0.5*(position_index-2*(self.curve_process(wager)-0.5))**2))

    def get_appear_time(self, public_card):  # 返回每个数字出现的个数
        appear_time_list = [0]*13
        for card in public_card:
            appear_time_list[card[1]] += 1
        return appear_time_list

    def one_pair_complement(self, wager, public_card: list):
        matrix = self.matrix
        one_pair_position_index = self.one_pair_position_index
        for card in public_card:
            for r in range(13):
                for c in range(13):
                    if c == card[1]:
                        cache1 = matrix[r][card[1]] * self.normal_distribution_process(
                            wager, one_pair_position_index)
                        cache2 = matrix[r][card[1]]
                        if card[1] > r:
                            self.upper_precentage_sum += (cache1-cache2)
                        else:
                            self.lower_precentage_sum += (cache1-cache2)
                        self.precentage_sum += (cache1-cache2)
                        matrix[r][card[1]] = cache1
                    elif r == card[1]:
                        cache1 = matrix[card[1]][c] * self.normal_distribution_process(
                            wager, one_pair_position_index)
                        cache2 = matrix[card[1]][c]
                        if c > card[1]:
                            self.upper_precentage_sum += (cache1-cache2)
                        else:
                            self.lower_precentage_sum += (cache1-cache2)
                        self.precentage_sum += (cache1-cache2)
                        matrix[card[1]][c] = cache1

    def two_pair_complement(self, wager, public_card: list):
        matrix = self.matrix
        two_pair_position_index = self.two_pair_position_index
        time_list = self.get_appear_time(public_card)
        i = 0
        while i < 13:
            if time_list[i] == 2:
                for rc in range(13):
                    cache1 = matrix[rc][rc] * self.normal_distribution_process(
                        wager, two_pair_position_index)
                    cache2 = matrix[rc][rc]
                    self.lower_precentage_sum += (cache1-cache2)
                    self.precentage_sum += (cache1-cache2)
                    matrix[rc][rc] = cache1

            elif time_list[i] == 1:
                j = i+1
                while j < 13:
                    if time_list[j] == 1:
                        cache1 = matrix[i][j] * self.normal_distribution_process(
                            wager, two_pair_position_index)
                        cache2 = matrix[i][j]
                        self.upper_precentage_sum += (cache1-cache2)
                        self.precentage_sum += (cache1-cache2)
                        matrix[i][j] = cache1

                        cache1 = matrix[j][i] * self.normal_distribution_process(
                            wager, two_pair_position_index)
                        cache2 = matrix[j][i]
                        self.upper_precentage_sum += (cache1-cache2)
                        self.precentage_sum += (cache1-cache2)
                        matrix[j][i] = cache1
            i += 1

    def three_of_kind_complement(self, wager, public_card: list):
        matrix = self.matrix
        three_of_kind_position_index = self.three_of_kind_position_index
        time_list = self.get_appear_time(public_card)
        i = 0
        while i < 13:
            if time_list[i] == 2:
                for rc in range(13):
                    if rc != i:
                        cache1r = matrix[rc][i] * self.normal_distribution_process(
                            wager, three_of_kind_position_index)
                        cache2r = matrix[rc][i]
                        if i > rc:
                            self.upper_precentage_sum += (cache1r-cache2r)
                        else:
                            self.lower_precentage_sum += (cache1r-cache2r)
                        self.precentage_sum += (cache1r-cache2r)
                        matrix[rc][i] = cache1r

                        cache1c = matrix[i][rc] * self.normal_distribution_process(
                            wager, three_of_kind_position_index)
                        cache2c = matrix[i][rc]

                        if rc > i:
                            self.upper_precentage_sum += (cache1c-cache2c)
                        else:
                            self.lower_precentage_sum += (cache1c-cache2c)
                        self.precentage_sum += (cache1c-cache2c)
                        matrix[i][rc] = cache1c
                    else:
                        cache1 = matrix[i][i] * self.normal_distribution_process(
                            wager, three_of_kind_position_index)
                        cache2 = matrix[i][i]
                        self.lower_precentage_sum += (cache1-cache2)
                        self.precentage_sum += (cache1-cache2)
                        matrix[i][i] = cache1

            elif time_list[i] == 1:
                cache1 = matrix[i][i] * self.normal_distribution_process(
                    wager, three_of_kind_position_index)
                cache2 = matrix[i][i]
                self.lower_precentage_sum += (cache1-cache2)
                self.precentage_sum += (cache1-cache2)
                matrix[i][i] = cache1
            i += 1

    def straight_complement(self, wager, public_card: list):
        matrix = self.matrix
        straight_position_index = self.straight_position_index
        time_list = self.get_appear_time(public_card)
        time_list = [time_list[12]] + time_list
        i = 0
        while i < 10:
            interval_time_list = time_list[i:i+5]
            count = 0

            required_card = []
            x = 0
            while x < 5:
                if interval_time_list[x] == 0:
                    ix = i+x
                    if ix == 13:
                        ix = 0
                    required_card.append(ix)
                else:
                    count += 1
                x += 1

            if count == 3:
                cache1r = matrix[required_card[0]][required_card[1]] * \
                    self.normal_distribution_process(
                        wager, straight_position_index)
                cache2r = matrix[required_card[0]][required_card[1]]
                if required_card[1] > required_card[0]:
                    self.upper_precentage_sum += (cache1r-cache2r)
                else:
                    self.lower_precentage_sum += (cache1r-cache2r)
                self.precentage_sum += (cache1r-cache2r)
                matrix[required_card[0]][required_card[1]] = cache1r

                cache1c = matrix[required_card[1]][required_card[0]] * \
                    self.normal_distribution_process(
                        wager, straight_position_index)
                cache2c = matrix[required_card[1]][required_card[0]]
                if required_card[0] > required_card[1]:
                    self.upper_precentage_sum += (cache1c-cache2c)
                else:
                    self.lower_precentage_sum += (cache1c-cache2c)
                self.precentage_sum += (cache1c-cache2c)
                matrix[required_card[1]][required_card[0]] = cache1c

            elif count == 4:
                for rc in range(13):
                    if rc != required_card[0]:
                        cache1r = matrix[rc][required_card[0]] * \
                            self.normal_distribution_process(
                                wager, straight_position_index)
                        cache2r = matrix[rc][required_card[0]]
                        if required_card[0] > rc:
                            self.upper_precentage_sum += (cache1r-cache2r)
                        else:
                            self.lower_precentage_sum += (cache1r-cache2r)
                        self.precentage_sum += (cache1r-cache2r)
                        matrix[rc][required_card[0]] = cache1r

                        cache1c = matrix[required_card[0]][rc] * \
                            self.normal_distribution_process(
                                wager, straight_position_index)
                        cache2c = matrix[required_card[0]][rc]
                        if rc > required_card[0]:
                            self.upper_precentage_sum += (cache1c-cache2c)
                        else:
                            self.lower_precentage_sum += (cache1c-cache2c)
                        self.precentage_sum += (cache1c-cache2c)
                        matrix[required_card[0]][rc] = cache1c
                    else:
                        cache1 = matrix[required_card[0]][required_card[0]] * \
                            self.normal_distribution_process(
                                wager, straight_position_index)
                        cache2 = matrix[required_card[0]][required_card[0]]
                        self.lower_precentage_sum += (cache1-cache2)
                        self.precentage_sum += (cache1-cache2)
                        matrix[required_card[0]][required_card[0]] = cache1
            i += 1

    def full_house_complement(self, wager, public_card: list):
        matrix = self.matrix
        full_house_position_index = self.full_house_position_index
        time_list = self.get_appear_time(public_card)
        for j in range(13):
            if time_list[j] == 3:
                for i in range(13):
                    if time_list[i] == 1:
                        for rc in range(13):
                            cache1r = matrix[rc][i] * self.normal_distribution_process(
                                wager, full_house_position_index)
                            cache2r = matrix[rc][i]
                            if i > rc:
                                self.upper_precentage_sum += (cache1r-cache2r)
                            else:
                                self.lower_precentage_sum += (cache1r-cache2r)
                            self.precentage_sum += (cache1r-cache2r)
                            matrix[rc][i] = cache1r

                            cache1c = matrix[i][rc] * self.normal_distribution_process(
                                wager, full_house_position_index)
                            cache2c = matrix[i][rc]
                            if rc > i:
                                self.upper_precentage_sum += (cache1c-cache2c)
                            else:
                                self.lower_precentage_sum += (cache1c-cache2c)
                            self.precentage_sum += (cache1c-cache2c)
                            matrix[i][rc] = cache1c

                    cache1 = matrix[i][i] * self.normal_distribution_process(
                        wager, full_house_position_index)
                    cache2 = matrix[i][i]
                    self.lower_precentage_sum += (cache1-cache2)
                    self.precentage_sum += (cache1-cache2)
                    matrix[i][i] = cache1
            elif time_list[j] == 2:
                for k in range(j+1, 13):
                    if time_list[k] == 2:
                        for rc in range(13):
                            cache1r = matrix[rc][k] * self.normal_distribution_process(
                                wager, full_house_position_index)
                            cache2r = matrix[rc][k]
                            if k > rc:
                                self.upper_precentage_sum += (cache1r-cache2r)
                            else:
                                self.lower_precentage_sum += (cache1r-cache2r)
                            self.precentage_sum += (cache1r-cache2r)
                            matrix[rc][k] = cache1r

                            cache1c = matrix[k][rc] * self.normal_distribution_process(
                                wager, full_house_position_index)
                            cache2c = matrix[k][rc]
                            if rc > k:
                                self.upper_precentage_sum += (cache1c-cache2c)
                            else:
                                self.lower_precentage_sum += (cache1c-cache2c)
                            self.precentage_sum += (cache1c-cache2c)
                            matrix[k][rc] = cache1c

                            cache1r = matrix[rc][j] * self.normal_distribution_process(
                                wager, full_house_position_index)
                            cache2r = matrix[rc][j]
                            if j > rc:
                                self.upper_precentage_sum += (cache1r-cache2r)
                            else:
                                self.lower_precentage_sum += (cache1r-cache2r)
                            self.precentage_sum += (cache1r-cache2r)
                            matrix[rc][j] = cache1r

                            cache1c = matrix[j][rc] * self.normal_distribution_process(
                                wager, full_house_position_index)
                            cache2c = matrix[j][rc]
                            if rc > j:
                                self.upper_precentage_sum += (cache1c-cache2c)
                            else:
                                self.lower_precentage_sum += (cache1c-cache2c)
                            self.precentage_sum += (cache1c-cache2c)
                            matrix[j][rc] = cache1c

                    elif time_list[k] == 1:
                        for i in range(13):
                            if time_list[i] == 1:
                                cache1 = matrix[i][i] * self.normal_distribution_process(
                                    wager, full_house_position_index)
                                cache2 = matrix[i][i]
                                self.lower_precentage_sum += (cache1-cache2)
                                self.precentage_sum += (cache1-cache2)
                                matrix[i][i] = cache1

    def four_of_the_kind_complement(self, wager, public_card: list):
        matrix = self.matrix
        four_of_the_kind_position_index = self.four_of_the_kind_position_index
        time_list = self.get_appear_time(public_card)
        for i in range(13):
            if time_list[i] == 3:
                for rc in range(13):
                    if rc != i:
                        cache1r = matrix[rc][i] * self.normal_distribution_process(
                            wager, four_of_the_kind_position_index)
                        cache2r = matrix[rc][i]
                        if i > rc:
                            self.upper_precentage_sum += (cache1r-cache2r)
                        else:
                            self.lower_precentage_sum += (cache1r-cache2r)
                        self.precentage_sum += (cache1r-cache2r)
                        matrix[rc][i] = cache1r

                        cache1c = matrix[i][rc] * self.normal_distribution_process(
                            wager, four_of_the_kind_position_index)
                        cache2c = matrix[i][rc]
                        if rc > i:
                            self.upper_precentage_sum += (cache1c-cache2c)
                        else:
                            self.lower_precentage_sum += (cache1c-cache2c)
                        self.precentage_sum += (cache1c-cache2c)
                        matrix[i][rc] = cache1c
                    else:
                        cache1 = matrix[i][i] * self.normal_distribution_process(
                            wager, four_of_the_kind_position_index)
                        cache2 = matrix[i][i]
                        self.lower_precentage_sum += (cache1-cache2)
                        self.precentage_sum += (cache1-cache2)
                        matrix[i][i] = cache1

            elif time_list[i] == 2:
                cache1 = matrix[i][i] * self.normal_distribution_process(
                    wager, four_of_the_kind_position_index)
                cache2 = matrix[i][i]
                self.lower_precentage_sum += (cache1-cache2)
                self.precentage_sum += (cache1-cache2)
                matrix[i][i] = cache1

    def first_bet_update(self, wager, current_deposit, initial_deposit):  # 没有公牌时用的update
        matrix = self.matrix
        possibility_threshold = 8 + 4 *self.valueable_func(wager, current_deposit,initial_deposit)/initial_deposit
        for row in range(13):
            for col in range(13):
                cache = (possibility_threshold - 9) * (
                    self.winning_posibility_matrix[12-row][12-col]-possibility_threshold)
                if cache >= 0:
                    self.precentage_sum += (cache-1)
                    matrix[12-row][12-col] = cache
                else:
                    self.precentage_sum -= (1+1/cache)
                    matrix[12-row][12-col] = -1/cache

    def second_bet_update(self, wager, current_deposit, initial_deposit, raw_public_card):  # 有公牌时用的update
        value = self.valueable_func(wager, current_deposit, initial_deposit)
        public_card = []
        for raw_card in raw_public_card:
            public_card.append([get_card_suit_id(raw_card), 12-get_card_num_id(raw_card)])

        self.one_pair_complement(value, public_card)
        self.three_of_kind_complement(value, public_card)
        self.straight_complement(value, public_card)
        self.full_house_complement(value, public_card)
        self.four_of_the_kind_complement(value, public_card)

    def m_show_hand(self, public_cards, self_player, compare_player):
        rest_players = [self_player, compare_player]
        biggest_type = -1
        for player in rest_players:
            seven_cards = public_cards + player.hand
            scores = get_max_score(seven_cards)
            player.score = scores
            if scores[0] > biggest_type:
                biggest_type = scores[0]

        # 最大牌型的玩家们
        winners: list[Player] = []
        for player in rest_players:
            if player.score[0] == biggest_type:
                winners.append(player)

        # 如果只有一个玩家具有最大牌型，独赢
        if len(winners) == 1:
            if winners[0] is self_player:
                return 1
            else:
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
                    if winners[0] is self_player:
                        return 1
                    else:
                        return 0

                # 遍历到最后一名玩家后 break
                if winners[j] == winners[-1]:
                    break
                j += 1

        # 还没有分出胜负，平分彩池
        return 0.5

    def return_winning_possibility(self, public_cards, self_player):
        possible_combination = [[0, 1, 2, 3], [1, 2, 3], [2, 3], [3]]
        conditional_winning_possibility = [
            [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]]
        suit_count = [0, 0, 0, 0]
        win_count = 0
        sum_count = 0

        if len(public_cards) == 0:
            i = max(get_card_num_id(self_player.hand[0]),get_card_num_id(self_player.hand[1]))
            j = min(get_card_num_id(self_player.hand[0]),get_card_num_id(self_player.hand[1]))

            if get_card_suit_id(self_player.hand[0]) == get_card_suit_id(self_player.hand[1]):                   
                i = min(get_card_num_id(self_player.hand[0]),get_card_num_id(self_player.hand[1]))
                j = max(get_card_num_id(self_player.hand[0]),get_card_num_id(self_player.hand[1]))

            for row in range(13):
                for col in range(13):
                    if self.winning_posibility_matrix[i][j] > self.winning_posibility_matrix[row][col]:
                        win_count += self.matrix[i][j]/self.precentage_sum
                    elif self.winning_posibility_matrix[i][j] == self.winning_posibility_matrix[row][col]:
                        win_count += 0.5*self.matrix[i][j]/self.precentage_sum
            return win_count

        for card in public_cards:
            suit_count[get_card_suit_id(card)] += 1

        three_same_suit = -1
        four_same_suit = -1

        for c in range(len(suit_count)):
            if suit_count[c] == 4:
                four_same_suit = c
            elif suit_count[c] == 3:
                three_same_suit = c

        for i in range(4):
            for j in range(len(possible_combination[i])):
                if i == j:
                    for row in range(13):
                        for col in range(row+1, 13):
                            temp_player = Player(name=' ', position=1)
                            temp_player.hand = [i + 4*(12-row), j + 4*(12-col)]
                            if i + 4*(12-row) in self_player.hand or j + 4*(12-col) in self_player.hand:
                                continue
                            conditional_winning_possibility[i][j] += self.m_show_hand(
                                public_cards, self_player, temp_player) * self.return_possibility(row, col)
                else:
                    for row in range(13):
                        for col in range(row):
                            temp_player = Player(name=' ', position=1)
                            temp_player.hand = [i + 4*(12-row), j + 4*(12-col)]
                            if i + 4*(12-row)  in self_player.hand or j + 4*(12-col) in self_player.hand:
                                continue
                            conditional_winning_possibility[i][j] += self.m_show_hand(
                                public_cards, self_player, temp_player) * self.return_possibility(row, col)

        for i in range(4):
            for j in range(len(possible_combination[i])):
                multiplier = 1
                if three_same_suit == i and three_same_suit == j:
                    multiplier = 3
                elif four_same_suit == i or four_same_suit == j:
                    multiplier = 2
                win_count += multiplier * conditional_winning_possibility[i][j]
                sum_count += multiplier
        return win_count/sum_count
    
    def refresh_matrix(self):
        self.matrix = [[1]*(13) for _ in range(13)]
        self.precentage_sum = 13*13

class Player:
    def __init__(self, name: str, position: int, money: int = 10000, tree: NodeClass.RootNode = None, label=None) -> None:
        self.name = name
        self.money = money
        self.init_money = money
        self.label = label
        self.position = position
        self.tree = tree
        self.hand = []
        self.score = None
        self.current_bet = 0
        self.p = None
        self.position: int = None
        self.first_choice = None
        self.second_choice = None
        self.third_choice = None
        self.fourth_choice = None
        self.hand_num = None
        self.states: list[State] = [None, None, None, None]
        self.matrice: list[Matrix] = []
        self.last_wager = 0
        self.character = 0

        # self.second_state:State = None

        # self.third_state:State = None
        # self.fourth_state:State = None
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

    def small_blind(self, sb):
        self.current_bet = sb
        self.money -= sb

    def big_blind(self, bb):
        self.current_bet = bb
        self.money -= bb

    # 没人下注时 第一个下注的人
    def bet(self, max_bet: int) -> int:
        # rand
        bet_money = random.randint(1, 50)
        if self.money > bet_money:
            self.money -= bet_money
            self.current_bet += bet_money
            # self.is_bet = True
            return bet_money
        else:
            allin = self.money
            self.current_bet += allin
            # self.money = 0
            return -3  # allin

    # def call(self,money:int) -> int:
    #     return money

    def Raise(self, max_bet: int, factors: int) -> int:

        if factors == 1:
            coefficient = random.choice([2, 3])
        elif factors == 3:
            coefficient = random.choice([4, 5])
        elif factors == 5:
            coefficient = random.choice([6, 7])
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

    def call(self, money: int) -> int:
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

    def new_game(self) -> None:
        pass
        # self.tree

    def action(self, max_bet, round, simulate=-1) -> float:

        if simulate != -1:
            if simulate == 0:
                return self.fold()
            elif simulate == 1:
                return self.check()
            elif simulate == 2:
                return self.call(max_bet)
            elif simulate == 3:
                return self.bet(max_bet)
            elif simulate == 4:
                return self.Raise(max_bet, 1)
            elif simulate == 5:
                return self.Raise(max_bet, 3)
            elif simulate == 6:
                return self.Raise(max_bet, 5)
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
            self.p_l = self.tree.nodes[self.hand_num].decisions[self.first_choice].decisions[
                self.second_choice].decisions[self.third_choice].decisions_p

        # print(self.p_l)

        # self.hand

        # action_label = self.tree
        # random.choice(["check","call",'asd'])

        # if round == 1:
        #     win_pos = 0.5
        # else:
        #     self.matrix.second_bet_update(
        #         self.last_wager, self.money, self.init_money, self.states[round-1].public_cards)
        #     win_pos = self.matrix.return_winning_possibility(
        #         self.states[round-1].public_cards, self)
        # win_pos = 0.5
        # np.random.seed(0)
        # # 没人下注的话，可以check和bet（一般不直接fold）S
        # if ((max_bet - self.current_bet) == 0):
        #     sum = self.p_l[1] + self.p_l[3]
        #     p1 = self.p_l[1] / sum / 2 + (1-win_pos) / 2
        #     p2 = self.p_l[3] / sum / 2 + win_pos / 2
        #     p = np.array([p1, p2])
        #     action_label = np.random.choice([1, 3], p=p.ravel()
        if round == 1:
            sum_pos = 0
            player_number = 0
            for i in self.matrice:
                i_fold = False
                if i.owner != self and i_fold == False:
                    sum_pos += i.return_winning_possibility([], self)
                    player_number += 1
            win_pos = sum_pos / player_number
        else:
            sum_pos = 0
            player_number = 0
            for i in self.matrice:
                i_fold = False
                if i.owner in self.states[round - 1].rest_players:
                    i_fold = False
                else:
                    i_fold = True
                if i.owner != self and i_fold == False:
                    sum_pos += i.return_winning_possibility(self.states[round - 1].public_cards, self)
                    player_number += 1
            if player_number == 0:
                win_pos = 0.5
            else:    
                win_pos = sum_pos / player_number

            
        np.random.seed(0)
        win_pos = 0.5
        # # 没人下注的话，可以check和bet（一般不直接fold）S
        if ((max_bet - self.current_bet) == 0):
            sum = self.p_l[1] + self.p_l[3]
            p1 = self.p_l[1] / sum / 2 + (1-win_pos) / 2
            p2 = self.p_l[3] / sum / 2 + win_pos / 2
            p = np.array([p1, p2])
            action_label = np.random.choice([1, 3], p=p.ravel())

        # 有人下注就不能check，只能fold，call，raise
        else:
            sum = self.p_l[0] + self.p_l[2] + \
                self.p_l[4] + self.p_l[5] + self.p_l[6]
            if win_pos < 0.4:
                p1 = self.p_l[0] / sum / 2 + (1-win_pos)/2
                p2 = self.p_l[2] / sum / 2 + win_pos/8
                p3 = self.p_l[4] / sum / 2 + win_pos/8
                p4 = self.p_l[5] / sum / 2 + win_pos/8
                p5 = self.p_l[6] / sum / 2 + win_pos/8
            elif win_pos >= 0.4 and win_pos < 0.55:
                p1 = self.p_l[0] / sum / 2 + (1-win_pos)/8
                p2 = self.p_l[2] / sum / 2 + win_pos/2
                p3 = self.p_l[4] / sum / 2 + (1-win_pos)/8
                p4 = self.p_l[5] / sum / 2 + (1-win_pos)/8
                p5 = self.p_l[6] / sum / 2 + (1-win_pos)/8
            elif win_pos >= 0.55 and win_pos < 0.7:
                p1 = self.p_l[0] / sum / 2 + (1-win_pos)/8
                p2 = self.p_l[2] / sum / 2 + (1-win_pos)/8
                p3 = self.p_l[4] / sum / 2 + win_pos/2
                p4 = self.p_l[5] / sum / 2 + (1-win_pos)/8
                p5 = self.p_l[6] / sum / 2 + (1-win_pos)/8
            elif win_pos >= 0.7 and win_pos < 0.85:
                p1 = self.p_l[0] / sum / 2 + (1-win_pos)/8
                p2 = self.p_l[2] / sum / 2 + (1-win_pos)/8
                p3 = self.p_l[4] / sum / 2 + (1-win_pos)/8
                p4 = self.p_l[5] / sum / 2 + win_pos/2
                p5 = self.p_l[6] / sum / 2 + (1-win_pos)/8
            elif win_pos >= 0.85 and win_pos <= 1:
                p1 = self.p_l[0] / sum / 2 + (1-win_pos)/8
                p2 = self.p_l[2] / sum / 2 + (1-win_pos)/8
                p3 = self.p_l[4] / sum / 2 + (1-win_pos)/8
                p4 = self.p_l[5] / sum / 2 + (1-win_pos)/8
                p5 = self.p_l[6] / sum / 2 + win_pos/2
            p = np.array([p1, p2, p3, p4, p5])
            action_label = np.random.choice([0, 2, 4, 5, 6], p=p.ravel())
            action_label = random.choice([0,3,4,5,6])

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
            money = self.call(max_bet)
        elif action_label == 3:  # call
            money = self.bet(2)
        elif action_label == 4:
            money = self.Raise(max_bet, 1)
        elif action_label == 5:
            money = self.Raise(max_bet, 3)
        elif action_label == 6:
            money = self.Raise(max_bet, 5)
        if money > 0:
            self.last_wager = self.current_bet
        return money

    def get_max_score(self) -> None:

        return

# p_l = [0.2,0.2,0.2,0.2,0.1,0.06,0.04]
# sum = p_l[0] + p_l[2] + p_l[4] + p_l[5] + p_l[6]
# p = np.array([p_l[0] / sum, p_l[2] / sum, p_l[4] / sum, p_l[5] / sum,p_l[6] / sum])
# z_count = 0
# c_count = 0
# r_count = 0


# for i in range(100):
#     action_label = np.random.choice([0,2,4,5,6] , p = p.ravel())
#     if action_label == 0:
#         z_count += 1
#     elif action_label == 2:
#         c_count += 1
#     else:
#         r_count += 1

# print(z_count,c_count,r_count)
