import NodeClass
from Player import Player
import poker

# def MCCFR(node, i:Player, h, p):
#     if isinstance(node,NodeClass.ResultNode):  # 如果游戏已经结束
#         return node.value # 拿utility
#     elif h.player() == i:   # 如果这是当前玩家的回合
#         decisions_p = node.decisions_p # 获取当前策略
#         node_utility = 0
#         decisions = node.decisions
#         for a in range(len(decisions_p)):
#             if a == 0:
#                 # fold
#                 pass
#             i.action(a)
#             new_p = decisions_p[a] * p
#             node = decisions[a]
#             next_h = game.do_action(h, a)
#             node_utility += MCCFR(node, i, next_h, new_p)
#             regret = node_utility - MCCFR(node, i, h, p)
#             update_regret_sum(node, i, h, a, regret)
#         return node_utility
#     else:                   # 如果这不是当前玩家的回合
#         strategy = get_average_strategy(node, i, h)   # 获取平均策略
#         a = choose_action(strategy)          # 根据平均策略选择动作
#         return MCCFR(node, i, game.do_action(h, a), p)
    
    
# def update_regret_sum(node,i,h,a,regret):
#     pass


def simulate_game(game:poker.Game,player:Player,ini_money:list):
    players_original_money = [0] * game.players_num
    for i in range(game.players_num):
        players_original_money[i] = ini_money[i]
        
    player_money_after_first_round = [0] * game.players_num
    player_money_after_second_round = [0] * game.players_num
    player_money_after_third_round = [0] * game.players_num
    
    player_after_first_round = []
    player_after_second_round = []
    player_after_third_round = []
    
    # game.deal_public_cards(3,2)
    # game.deal_public_cards(1,3)
    # game.deal_public_cards(1,4)
    
    # decisions_p = node.decisions_p # 获取当前策略
    # node_utility = 0
    # decisions = node.decisions
    
    current_money = player.money
    node = player.tree.nodes[player.hand_num].decisions
    p1 = 0
    for i in range(7):
        
        node = player.tree.nodes[player.hand_num].decisions
        # 重置彩池
        game.pot = p1
        # 重置剩余玩家
        game.rest_players = game.players.copy()
        # 重置玩家的钱
        for i in range(game.players_num):
            game.players[i].money = players_original_money[i]
        
        
        # 弃牌的话 这个node的utility等于损失的钱
        if i == 0: # fold
            node[i].value = -(current_money - player.money)
            continue
        
        # 第一轮里想让这个玩家做i这个动作   
        if not (game.action_first_round(player,i)): # 如果不成功
            flag = False
            for t in range(3): # 尝试三次
                flag = game.action_first_round(player,i) 
                if flag: # 如果成功了，继续往下
                    break
            if not flag:
                continue
        if len(game.rest_players) == 1 and len(game.allin) == 0: # player 赢了，这个node的utility等于彩池
            node[i].value = game.pot - (current_money - player.money)
            continue
        
        #  第一轮就结束了，证明有人allin了
        if len(game.rest_players) == 0 and len(game.allin) != 0:
            if game.show_hand(player) == 1: # player 赢了
                node[i].value = game.pot - (current_money - player.money)
            else: # 输了
                node[i].value = -(current_money - player.money)
            continue
                
        
        # 储存这一轮结束后的彩池和每个玩家的剩余的钱
        player_after_first_round = game.rest_players.copy()
        p2 = game.pot
        for num in range(game.players_num):
            player_money_after_first_round[num] = game.players[num].money
            pass
        
        # 进入下一个node
        # node = node[i].decisions
        
        # round 2
        for j in range(7):
            
            node = player.tree.nodes[player.hand_num].decisions[i].decisions
            # 重置彩池，等于第一轮结束时的彩池
            game.pot = p2
            # 重置玩家
            game.rest_players = player_after_first_round.copy()
            
            # 重置玩家的钱
            for num in range(game.players_num):
                game.players[num].money = player_money_after_first_round[num]
                
                
            if j == 0: # fold
                node[j].value = -(current_money - player.money)
                continue
            
            # 第二轮里想让这个玩家做j这个动作   
            if not (game.action(2,player,j)): # 如果不成功
                flag = False
                for t in range(3): # 尝试三次
                    flag = game.action(2,player,j) 
                    if flag: # 如果成功了，继续往下
                        break
                if not flag:
                    continue
            
            # 如果
            if len(game.rest_players) == 1 and len(game.allin) == 0: # player 赢了，这个node的utility等于彩池
                node[j].value = game.pot - (current_money - player.money)
                continue
        
            #  第一轮就结束了，证明有人allin了
            if len(game.rest_players) == 0 and len(game.allin) != 0:
                if game.show_hand(player) == 1: # player 赢了
                    node[j].value = game.pot - (current_money - player.money)
                else: # 输了
                    node[j].value = -(current_money - player.money)
                continue
            
            
            # 储存这一轮结束后的彩池和每个玩家的剩余的钱
            player_after_second_round = game.rest_players.copy()
            p3 = game.pot
            for num in range(game.players_num):
                player_money_after_second_round[num] = game.players[num].money
                pass
                
                
            # node = node[j].decisions
            
            # round 3
            for k in range(7):
                
                node = player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions
                # 重置彩池，等于第一轮结束时的彩池
                game.pot = p3
                # 重置玩家
                game.rest_players = player_after_second_round.copy()
                # 重置玩家的钱
                for num in range(game.players_num):
                    game.players[num].money = player_money_after_second_round[num]
                
                if k == 0: # fold
                    node[k].value = -(current_money - player.money)
                    continue
                # 第二轮里想让这个玩家做i这个动作   
                if not (game.action(3,player,k)): # 如果不成功
                    flag = False
                    for t in range(3): # 尝试三次
                        flag = game.action(2,player,k) 
                        if flag: # 如果成功了，继续往下
                            break
                    if not flag:
                        continue
                    
                # 因为我们不让这个player 弃牌，所以留下来的玩家一定是player
                if len(game.rest_players) == 1 and len(game.allin) == 0: # player 赢了，这个node的utility等于彩池
                    node[k].value = game.pot - (current_money - player.money)
                    continue
                
                #  第二轮就结束了，证明有人allin了
                if len(game.rest_players) == 0 and len(game.allin) != 0:
                    if game.show_hand(player) == 1: # player 赢了
                        node[k].value = game.pot - (current_money - player.money)
                    else: # 输了
                        node[k].value = -(current_money - player.money)
                    continue    
                    
                # print(k)
                # print(type(node[k]))
                # node = node[k].decisions
                player_after_third_round = game.rest_players.copy()
                
                p4 = game.pot
                for num in range(game.players_num):
                    player_money_after_third_round[num] = game.players[num].money
            
                
                # round 4
                for l in range(len(node)):
                    
                    # if(i == 4 and j == 3 and k == 2):
                    #     print(player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k])
                    # print(player.hand_num,i,j,k)
                    node = player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].decisions
                    
                    game.pot = p4
                    game.rest_players = player_after_third_round.copy()
                     # 重置玩家的钱
                    for num in range(game.players_num):
                        game.players[num].money = player_money_after_third_round[num]
                        
                    
                    if i == 0: # fold
                        node[l].value = current_money - player.money
                        continue
                    # 第二轮里想让这个玩家做i这个动作   
                    if not (game.action(4,player,l)): # 如果不成功
                        flag = False
                        for t in range(3): # 尝试三次
                            flag = game.action(4,player,l) 
                            if flag: # 如果成功了，继续往下
                                break
                        if not flag:
                            continue
                        
                    # 正常到这第四轮结束就应该比大小了
                    if len(game.rest_players) == 1 and len(game.allin) == 0:
                        node[l] = game.pot - (current_money - player.money)
                    if len(game.rest_players) > 1:
                        if game.show_hand(player) == 1: # player 赢了
                            node[l].value = game.pot - (current_money - player.money)
                        else: # 输了
                            node[l].value = -(current_money - player.money)
                
