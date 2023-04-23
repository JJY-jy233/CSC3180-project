import math

class Matrix:
    def __init__(self):
        self.matrix = [[1]*(13) for _ in range(13)]
        self.precentage_sum = 13*13
        self.curve_index = 5
        self.nd_power = 2
        self.one_pair_position_index = 0
        self.two_pair_position_index = 0.25
        self.three_of_kind_position_index = 0.75
        self.straight_position_index =1.25
        self.full_house_position_index =1.5
        self.four_of_the_kind_position_index = 1.75       

        self.winning_posibility_matrix = [[30.8 ,19.8 ,18.2, 17.0 ,16.1 ,14.1 ,13.4 ,12.9 ,12.5 ,12.9 ,12.8 ,12.6 ,12.4],
                                    [16.2 ,25.8 ,17.6 ,16.5 ,15.7 ,13.7 ,12.4 ,11.9 ,11.5 ,11.2 ,11.1 ,11.0 ,10.9],
                                    [14.5 ,14.1 ,21.9 ,16.1 ,15.3 ,13.4 ,12.0 ,10.9 ,10.5 ,10.2 ,10.1 ,10.1 ,10.0],
                                    [13.1 ,12.8 ,12.5 ,18.9 ,15.3 ,13.4 ,12.1 ,10.9 ,9.84 ,6.58 ,9.47 ,9.41 ,9.32],
                                    [12.0 ,11.8 ,11.6 ,11.8 ,16.6 ,13.6 ,12.3 ,11.1 ,9.98 ,9.01 ,8.90 ,8.83 ,8.77],
                                    [9.93 ,9.69 ,9.55 ,9.71 ,10.1 ,15.2 ,12.3 ,11.4 ,10.3 ,9.32 ,8.44 ,8.36 ,8.28],
                                    [9.16 ,8.22 ,8.07 ,8.26 ,8.67 ,8.74 ,14.1 ,11.7 ,10.8 ,9.85 ,8.90 ,8.06 ,7.94],
                                    [8.56 ,7.65 ,6.79 ,6.91 ,7.32 ,7.76 ,8.14 ,13.2 ,11.2 ,10.4 ,9.52 ,5.58 ,7.74],
                                    [8.11 ,7.25 ,6.38 ,5.76 ,6.11 ,6.59 ,7.22 ,7.70 ,12.6 ,10.9 ,10.1 ,9.27 ,8.32],
                                    [8.60 ,6.91 ,6.10 ,5.49 ,5.05 ,5.47 ,6.15 ,6.85 ,7.37 ,12.0 ,10.6 ,9.97 ,9.06],
                                    [8.43 ,9.78 ,5.98 ,5.35 ,4.88 ,4.55 ,5.09 ,5.86 ,6.62 ,7.20 ,11.8 ,9.61 ,8.92],
                                    [8.27 ,6.69 ,5.87 ,5.29 ,4.82 ,4.42 ,4.42 ,4.84 ,5.65 ,6.42 ,6.05 ,11.8 ,8.59],
                                    [7.96 ,6.60 ,5.81 ,5.23 ,4.76 ,4.37 ,4.11 ,3.98 ,4.63 ,5.47 ,5.31 ,4.97 ,11.8]]
        
        pass

    def valueable_func(self,wager, current_deposit, initial_deposit): #衡量这笔下注对玩家有多重要
        return wager*(initial_deposit/current_deposit + 1)*0.5

    def return_possibility(self,row,col):
        matrix = self.matrix
        precentage_sum = self.precentage_sum
        return matrix[row][col]/precentage_sum

    def curve_process(self,wager): #转化为一个Lim等于2的func
        curve_index = self.curve_index
        return 2-(curve_index/(wager +curve_index/2))

    def normal_distribution_process(self,wager,position_index):#将正态分布函数在0-2中移动以显示哪个值上的可能性较高
        return 1+self.nd_power*((1+self.curve_process(wager))*math.exp(-1*(position_index-2*(self.curve_process(wager)-0.5))**2))

    def get_appear_time(self,public_card):#返回每个数字出现的个数
        appear_time_list = [0]*13
        for card in public_card:
            appear_time_list [card[1]] += 1
        return appear_time_list

    def one_pair_complement(self,wager,public_card:list):
        matrix = self.matrix
        precentage_sum = self.precentage_sum
        one_pair_position_index = self.one_pair_position_index
        for card in public_card:
            for r in range(13):
                for c in range(13):
                    if c == card[1]:
                        print(self.normal_distribution_process(wager,one_pair_position_index))
                        cache1 = matrix[r][card[1]] * self.normal_distribution_process(wager,one_pair_position_index)
                        cache2 = matrix[r][card[1]]
                        precentage_sum += (cache1-cache2)
                        matrix[r][card[1]] = cache1
                    elif r == card[1]:
                        cache1 = matrix[card[1]][c] * self.normal_distribution_process(wager,one_pair_position_index)
                        cache2 = matrix[card[1]][c]
                        precentage_sum += (cache1-cache2)
                        matrix[card[1]][c] = cache1
                
    def two_pair_complement(self,wager,public_card:list):
        matrix = self.matrix
        precentage_sum = self.precentage_sum
        two_pair_position_index= self.two_pair_position_index
        time_list = self.get_appear_time(public_card)
        i = 0
        while i < 13:
            if time_list[i] == 2:
                for rc in range(13):
                    cache1 = matrix[rc][rc] * self.normal_distribution_process(wager,two_pair_position_index)
                    cache2 = matrix[rc][rc]
                    precentage_sum += (cache1-cache2)
                    matrix[rc][rc] = cache1
                
            elif time_list[i] == 1:
                j = i+1
                while j < 13:
                    if time_list[j] == 1:
                        cache1 = matrix[i][j] * self.normal_distribution_process(wager,two_pair_position_index)
                        cache2 = matrix[i][j]
                        precentage_sum += (cache1-cache2)
                        matrix[i][j] = cache1
                        
                        cache1 = matrix[j][i] * self.normal_distribution_process(wager,two_pair_position_index)
                        cache2 = matrix[j][i]
                        precentage_sum += (cache1-cache2)
                        matrix[j][i] = cache1
            i += 1


    def three_of_kind_complement(self,wager,public_card:list):
        matrix = self.matrix
        precentage_sum = self.precentage_sum
        three_of_kind_position_index = self.three_of_kind_position_index
        time_list = self.get_appear_time(public_card)
        i = 0
        while i < 13:
            if time_list[i] == 2:
                for rc in range(13):
                    if rc != i:
                        cache1r = matrix[rc][i] * self.normal_distribution_process(wager,three_of_kind_position_index)
                        cache2r = matrix[rc][i]
                        precentage_sum += (cache1r-cache2r)
                        matrix[rc][i] = cache1r

                        cache1c = matrix[i][rc] * self.normal_distribution_process(wager,three_of_kind_position_index)
                        cache2c = matrix[i][rc]
                        precentage_sum += (cache1c-cache2c)
                        matrix[i][rc] = cache1c
                    else :
                        cache1 = matrix[i][i] * self.normal_distribution_process(wager,three_of_kind_position_index)
                        cache2 = matrix[i][i]
                        precentage_sum += (cache1-cache2)
                        matrix[i][i] = cache1

            elif time_list[i] == 1:
                cache1 = matrix[i][i] * self.normal_distribution_process(wager,three_of_kind_position_index)
                cache2 = matrix[i][i]
                precentage_sum += (cache1-cache2)
                matrix[i][i] = cache1
            i += 1

    def straight_complement(self,wager,public_card:list):
        matrix = self.matrix
        precentage_sum = self.precentage_sum
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
                cache1r = matrix[required_card[0]][required_card[1]] * self.normal_distribution_process(wager,straight_position_index)
                cache2r = matrix[required_card[0]][required_card[1]]
                precentage_sum += (cache1r-cache2r)
                matrix[required_card[0]][required_card[1]] = cache1r

                cache1c = matrix[required_card[1]][required_card[0]] * self.normal_distribution_process(wager,straight_position_index)
                cache2c = matrix[required_card[1]][required_card[0]] 
                precentage_sum += (cache1c-cache2c)
                matrix[required_card[1]][required_card[0]]  = cache1c    
            
            
            elif count == 4:
                for rc in range(13):
                    if rc != required_card[0]:
                        cache1r = matrix[rc][required_card[0]] * self.normal_distribution_process(wager,straight_position_index)
                        cache2r = matrix[rc][required_card[0]]
                        precentage_sum += (cache1r-cache2r)
                        matrix[rc][required_card[0]] = cache1r

                        cache1c = matrix[required_card[0]][rc] * self.normal_distribution_process(wager,straight_position_index)
                        cache2c = matrix[required_card[0]][rc]
                        precentage_sum += (cache1c-cache2c)
                        matrix[required_card[0]][rc] = cache1c
                    else :
                        cache1 = matrix[required_card[0]][required_card[0]] * self.normal_distribution_process(wager,straight_position_index)
                        cache2 = matrix[required_card[0]][required_card[0]]
                        precentage_sum += (cache1-cache2)
                        matrix[required_card[0]][required_card[0]] = cache1
            i += 1


    def full_house_complement(self,wager,public_card:list):
        matrix = self.matrix
        precentage_sum = self.precentage_sum
        full_house_position_index = self.full_house_position_index
        time_list = self.get_appear_time(public_card)
        for j in range(13):
            if time_list[j] == 3:
                for i in range(13):
                    if time_list[i] == 1:
                        for rc in range(13):
                            cache1r = matrix[rc][i] * self.normal_distribution_process(wager,full_house_position_index)
                            cache2r = matrix[rc][i]
                            precentage_sum += (cache1r-cache2r)
                            matrix[rc][i] = cache1r

                            cache1c = matrix[i][rc] * self.normal_distribution_process(wager,full_house_position_index)
                            cache2c = matrix[i][rc]
                            precentage_sum += (cache1c-cache2c)
                            matrix[i][rc] = cache1c
                    

                    cache1 = matrix[i][i] * self.normal_distribution_process(wager,full_house_position_index)
                    cache2 = matrix[i][i]
                    precentage_sum += (cache1-cache2)
                    matrix[i][i] = cache1
            elif time_list[j] == 2:
                for k in range(j+1,13):
                    if time_list[k] == 2:
                        for rc in range(13):
                            cache1r = matrix[rc][k] * self.normal_distribution_process(wager,full_house_position_index)
                            cache2r = matrix[rc][k]
                            precentage_sum += (cache1r-cache2r)
                            matrix[rc][k] = cache1r

                            cache1c = matrix[k][rc] * self.normal_distribution_process(wager,full_house_position_index)
                            cache2c = matrix[k][rc]
                            precentage_sum += (cache1c-cache2c)
                            matrix[k][rc] = cache1c

                            
                            cache1r = matrix[rc][j] * self.normal_distribution_process(wager,full_house_position_index)
                            cache2r = matrix[rc][j]
                            precentage_sum += (cache1r-cache2r)
                            matrix[rc][j] = cache1r

                            cache1c = matrix[j][rc] * self.normal_distribution_process(wager,full_house_position_index)
                            cache2c = matrix[j][rc]
                            precentage_sum += (cache1c-cache2c)
                            matrix[j][rc] = cache1c

                    elif time_list[k] == 1:
                        for i in range(13):
                            if time_list[i] == 1:                        
                                cache1 = matrix[i][i] * self.normal_distribution_process(wager,full_house_position_index)
                                cache2 = matrix[i][i]
                                precentage_sum += (cache1-cache2)
                                matrix[i][i] = cache1

                    
    def four_of_the_kind_complement(self,wager,curve_index,four_of_the_kind_position_index,public_card:list):  
        matrix = self.matrix
        precentage_sum = self.precentage_sum
        four_of_the_kind_position_index = self.four_of_the_kind_position_index
        time_list = self.get_appear_time(public_card)
        for i in range(13):
            if time_list[i] == 3:
                for rc in range(13):
                    if rc != i:
                        cache1r = matrix[rc][i] * self.normal_distribution_process(wager,four_of_the_kind_position_index)
                        cache2r = matrix[rc][i]
                        precentage_sum += (cache1r-cache2r)
                        matrix[rc][i] = cache1r

                        cache1c = matrix[i][rc] * self.normal_distribution_process(wager,four_of_the_kind_position_index)
                        cache2c = matrix[i][rc]
                        precentage_sum += (cache1c-cache2c)
                        matrix[i][rc] = cache1c
                    else :
                        cache1 = matrix[i][i] * self.normal_distribution_process(wager,four_of_the_kind_position_index)
                        cache2 = matrix[i][i]
                        precentage_sum += (cache1-cache2)
                        matrix[i][i] = cache1
            
            elif time_list[i] == 2:
                cache1 = matrix[i][i] * self.normal_distribution_process(wager,four_of_the_kind_position_index)
                cache2 = matrix[i][i]
                precentage_sum += (cache1-cache2)
                matrix[i][i] = cache1

    def first_bet_update(self,wager, current_deposit, initial_deposit): #没有公牌时用的update
        matrix = self.matrix
        precentage_sum = self.precentage_sum
        possibility_threshold = 10 + 10*self.valueable_func(wager, current_deposit, initial_deposit)/initial_deposit
        for row in range(13):
            for col in range(13):
                cache = (possibility_threshold- 9) * (self.winning_posibility_matrix[12-row][12-col]-possibility_threshold)
                if cache >= 0:
                    precentage_sum +=(cache-1)
                    matrix[12-row][12-col] = cache
                else:
                    precentage_sum -= (1+1/cache)
                    matrix[12-row][12-col] =-1/cache

    def second_bet_update(self,wager,current_deposit, initial_deposit, curve_index,public_card):#有公牌时用的update
        value = self.valueable_func(wager, current_deposit, initial_deposit)/initial_deposit
        self.one_pair_complement(value,curve_index,self.one_pair_position_index,public_card)    
        self.two_pair_complement(value,curve_index,self.two_pair_position_index,public_card)    
        self.three_of_kind_complement(value,curve_index,self.three_of_kind_position_index,public_card)
        self.straight_complement(value,curve_index,self.straight_position_index,public_card)
        self.full_house_complement(value,curve_index,self.full_house_position_index,public_card)
        self.four_of_the_kind_complement(value,curve_index,self.four_of_the_kind_position_index,public_card)
    

