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
    for ps in range(game.players_num):
        players_original_money[ps] = ini_money[ps]
        
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
    # print("hand",player.hand_num)
    # node = player.tree.nodes[player.hand_num].decisions
    p1 = 0
    for i in range(7):
        
        # node = player.tree.nodes[player.hand_num].decisions
        # 重置彩池
        game.pot = p1
        # 重置剩余玩家
        game.rest_players = game.players.copy()
        # 重置玩家的钱
        for i1 in range(game.players_num):
            game.players[i1].money = players_original_money[i1]
        
        # print("i",i)
        # 弃牌的话 这个node的utility等于损失的钱
        if i == 0: # fold
            game.action_first_round(player,i)
            player.tree.nodes[player.hand_num].decisions[i].value = -(current_money - player.money)
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
        if len(game.rest_players) == 1:
            if len(game.allin) == 0: # player 赢了，这个node的utility等于彩池
                player.tree.nodes[player.hand_num].decisions[i].value = game.pot - (current_money - player.money)
                player.tree.nodes[player.hand_num].decisions[i].pass_value()
                continue
            else:
                winners_num = game.show_hand(player)
                if winners_num > 0:
                    player.tree.nodes[player.hand_num].decisions[i].value = game.pot / winners_num - (current_money - player.money)
                    player.tree.nodes[player.hand_num].decisions[i].pass_value()
                else:
                    player.tree.nodes[player.hand_num].decisions[i].value = -(current_money - player.money)
                    player.tree.nodes[player.hand_num].decisions[i].pass_value()
        
        #  第一轮就结束了，证明有人allin了
        if len(game.rest_players) == 0 and len(game.allin) != 0:
            winners_num = game.show_hand(player)
            if winners_num > 0: # player 赢了
                player.tree.nodes[player.hand_num].decisions[i].value = game.pot - (current_money - player.money)
                player.tree.nodes[player.hand_num].decisions[i].pass_value()
            else: # 输了
                player.tree.nodes[player.hand_num].decisions[i].value = -(current_money - player.money)
                player.tree.nodes[player.hand_num].decisions[i].pass_value()
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
            
            # node = player.tree.nodes[player.hand_num].decisions[i].decisions
            # 重置彩池，等于第一轮结束时的彩池
            game.pot = p2
            # 重置玩家
            game.rest_players = player_after_first_round.copy()
            
            # 重置玩家的钱
            for j1 in range(game.players_num):
                game.players[j1].money = player_money_after_first_round[j1]
                
            # print("j",j)
            if j == 0: # fold
                player.tree.nodes[player.hand_num].decisions[i].decisions[j].value = -(current_money - player.money)
                continue
            
            # 第二轮里想让这个玩家做j这个动作   
            if not (game.action(2,player,j)): # 如果不成功
                flag = False
                for t1 in range(3): # 尝试三次
                    flag = game.action(2,player,j) 
                    if flag: # 如果成功了，继续往下
                        break
                if not flag:
                    continue
            
            # 如果
            if len(game.rest_players) == 1:
                if len(game.allin) == 0: # player 赢了，这个node的utility等于彩池
                    player.tree.nodes[player.hand_num].decisions[i].decisions[j].value = game.pot - (current_money - player.money)
                    player.tree.nodes[player.hand_num].decisions[i].decisions[j].pass_value()
                    continue
                else:
                    winners_num = game.show_hand(player)
                    if winners_num > 0: # player 赢了
                        player.tree.nodes[player.hand_num].decisions[i].decisions[j].value = game.pot / winners_num - (current_money - player.money)
                        player.tree.nodes[player.hand_num].decisions[i].decisions[j].pass_value()
                        
                    else: # 输了
                        player.tree.nodes[player.hand_num].decisions[i].decisions[j].value = -(current_money - player.money)
                        player.tree.nodes[player.hand_num].decisions[i].decisions[j].pass_value()
                    continue
        
            #  第一轮就结束了，证明有人allin了
            if len(game.rest_players) == 0 and len(game.allin) != 0:
                winners_num = game.show_hand(player)
                if winners_num > 0: # player 赢了
                    player.tree.nodes[player.hand_num].decisions[i].decisions[j].value = game.pot / winners_num - (current_money - player.money)
                    player.tree.nodes[player.hand_num].decisions[i].decisions[j].pass_value()
                else: # 输了
                    player.tree.nodes[player.hand_num].decisions[i].decisions[j].value = -(current_money - player.money)
                    player.tree.nodes[player.hand_num].decisions[i].decisions[j].pass_value()
                    
                continue
            
            
            # 储存这一轮结束后的彩池和每个玩家的剩余的钱
            player_after_second_round = game.rest_players.copy()
            p3 = game.pot
            for num1 in range(game.players_num):
                player_money_after_second_round[num1] = game.players[num1].money
                pass
                
                
            # node = node[j].decisions
            
            # round 3
            for k in range(7):
                
                # node = player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions
                # 重置彩池，等于第一轮结束时的彩池
                game.pot = p3
                # 重置玩家
                game.rest_players = player_after_second_round.copy()
                # 重置玩家的钱
                for k1 in range(game.players_num):
                    game.players[k1].money = player_money_after_second_round[k1]
                # print('k',k)
                if k == 0: # fold
                    player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].value = -(current_money - player.money)
                    continue
                # 第二轮里想让这个玩家做i这个动作   
                if not (game.action(3,player,k)): # 如果不成功
                    flag = False
                    for t2 in range(3): # 尝试三次
                        flag = game.action(2,player,k) 
                        if flag: # 如果成功了，继续往下
                            break
                    if not flag:
                        continue
                    
                # 因为我们不让这个player 弃牌，所以留下来的玩家一定是player
                if len(game.rest_players) == 1:
                    if len(game.allin) == 0: # player 赢了，这个node的utility等于彩池
                        player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].value = game.pot - (current_money - player.money)
                        player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].pass_value()
                        continue
                    else:
                        winners_num = game.show_hand(player)
                        if winners_num > 0: # player 赢了
                            player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].value = game.pot / winners_num - (current_money - player.money)
                            player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].pass_value()
                            
                        else: # 输了
                            player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].value = -(current_money - player.money)
                            player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].pass_value()
                        continue
                
                #  第三轮就结束了，证明有人allin了
                if len(game.rest_players) == 0 and len(game.allin) != 0:
                    winners_num = game.show_hand(player)
                    if winners_num > 0: # player 赢了
                        player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].value = game.pot / winners_num - (current_money - player.money)
                        player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].pass_value()
                    else: # 输了
                        player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].value = -(current_money - player.money)
                        player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].pass_value()
                    continue    
                    
                # print(k)
                # print(type(node[k]))
                # node = node[k].decisions
                player_after_third_round = game.rest_players.copy()
                
                p4 = game.pot
                for num2 in range(game.players_num):
                    player_money_after_third_round[num2] = game.players[num2].money
            
                
                # round 4
                for l in range(7):
                    # print(player.tree.nodes[player.hand_num].decisions[6].decisions[4].decisions[4].decisions[3].value)
                    
                    # if(i == 2 and j == 2 and k == 2):
                    #     print(player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k])
                    # print(player.hand_num,i,j,k)
                    # node = player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].decisions
                    
                    game.pot = p4
                    game.rest_players = player_after_third_round.copy()
                     # 重置玩家的钱
                    for l1 in range(game.players_num):
                        game.players[l1].money = player_money_after_third_round[l1]
                        
                    
                    if l == 0: # fold
                        player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].decisions[l].value = -(current_money - player.money)
                        continue
                    # 第二轮里想让这个玩家做i这个动作   
                    if not (game.action(4,player,l)): # 如果不成功
                        flag = False
                        for t3 in range(3): # 尝试三次
                            flag = game.action(4,player,l) 
                            if flag: # 如果成功了，继续往下
                                break
                        if not flag:
                            continue
                        
                    # 正常到这第四轮结束就应该比大小了
                    if len(game.rest_players) == 1:
                        if len(game.allin) == 0:
                            player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].decisions[l].value = game.pot - (current_money - player.money)
                        else:
                            winners_num = game.show_hand(player)
                            if winners_num > 0: # player 赢了
                                player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].decisions[l].value = game.pot / winners_num - (current_money - player.money)
                            else: # 输了
                                player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].decisions[l].value = -(current_money - player.money)
                    elif len(game.rest_players) > 1:
                        winners_num = game.show_hand(player)
                        if winners_num > 0: # player 赢了
                            # print(i,j,k,l)
                            player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].decisions[l].value = game.pot / winners_num - (current_money - player.money)
                            # print(node[l].value)
                        else: # 输了
                            # print(i,j,k,l)
                            
                            player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].decisions[l].value = -(current_money - player.money)
                            # print(node[l].value)
                    
                    
                    
                    # print("node",player.tree.nodes[player.hand_num].decisions[i].decisions[j].decisions[k].decisions[l].value)
                    
                        
                    # if i == 6 and j == 4 and k == 4:
                    #     print(node[l].value)
                        
                            
