from itertools import combinations

            
def get_card_suit_id(card_id):
    return card_id & 3

def get_card_num_id(card_id):
    return (card_id >> 2)
    


def eval_hand(hand:list) -> int: #11 , 9 -> 1,3
    # l = [['AA','AKs','AQs','AJs','ATs','A9s','A8s','A7s','A6s','A5s','A4s','A3s','A2s'],
    #      ['AKo','KK','KQs','KJs','KTs','K9s','K8s','K7s','K6s','K5s','K4s','K3s','K2s'],
    #      ['AQo','KQo','QQ','QJs','QTs','Q9s','Q8s','Q7s','Q6s','Q5s','Q4s','Q3s','Q2s'],
    #      ['AJo','KJo','QJo','JJ','JTs','J9s','J8s','J7s','J6s','J5s','J4s','J3s','J2s'],
    #      ['ATo','KTo','QTo','JTo','TT','T9s','T8s','T7s','T6s','T5s','T4s','T3s','T2s'],
    #      ['A9o','K9o','Q9o','J9o','T9o','99','98s','97s','96s','95s','94s','93s','92s'],
    #      ['A8o','K8o','Q8o','J8o','T8o','98o','88','87s','86s','85s','84s','83s','82s'],
    #      ['A7o','K7o','Q7o','J7o','T7o','97o','87o','77','76s','75s','74s','73s','72s'],
    #      ['A6o','K6o','Q6o','J6o','T6o','96o','86o','76o','66','65s','64s','63s','62s'],
    #      ['A5o','K5o','Q5o','J5o','T5o','95o','85o','75o','65o','55','54s','53s','52s'],
    #      ['A4o','K4o','Q4o','J4o','T4o','94o','84o','74o','64o','54o','44','43s','42s'],
    #      ['A3o','K3o','Q3o','J3o','T3o','93o','83o','73o','63o','53o','43o','33','32s'],
    #      ['A2o','K2o','Q2o','J2o','T2o','92o','82o','72o','62o','52o','42o','32o','22'],]
    hand.sort()
    a = get_card_suit_id(hand[0])
    b = get_card_suit_id(hand[1]) 
    big = get_card_num_id(hand[0]) # 0-12
    small = get_card_num_id(hand[1])

    i = 12 - big
    j = 12 - small         
    if a == b: # suit
        return j * 13 + i
    else: 
        return i * 13 + j
    

def display_card(card_id:int) -> str:
    
    num = get_card_num_id(card_id)
    if num == 12: display = 'A'
    elif num == 8: display = 'T'
    elif num == 9: display = 'J'
    elif num == 10: display = 'Q'
    elif num == 11: display = 'K'
    else: display = str(num+2)
    
    suit = get_card_suit_id(card_id)
    if suit == 0: display += '♠'
    elif suit == 1: display += '♥'
    elif suit == 2: display += '♦'
    else: display += '♣'
    return display

def display_hand(hand:list) -> None:
    hand_display = []
    for i in hand:
        hand_display.append(display_card(i))
    print(hand_display)
    
# 8 同花顺：比最大的牌即可。牌型分就是最大牌的数字大小
# 7 四条：牌型分需要先比四条的数字，再比单牌的数字。所以牌型分是个二维的结构：（四条的数字, 单牌的数字）
# 6 葫芦：牌型分是个二维的结构：（三条的数字, 一对的数字）
# 5 同花：牌型分是个五维的结构，从大到小排列的5个牌的数字
# 4 顺子：牌型分就是最大牌的数字大小
# 3 三条：牌型分是个三维的结构：（三条的数字, 较大单牌的数字, 较小单牌的数字）
# 2 两对：牌型分是个三维的结构：（较大对子的数字, 较小对子的数字, 单牌的数字）
# 1 一对：牌型分是个三维的结构：（对子的数字, 最大单牌的数字, 第二大单牌的数字, 第三大单牌的数字）
# 0 高牌：牌型分是个五维的结构，从大到小排列的5个牌的数字

def is_flush(five_cards):
    s = get_card_suit_id(five_cards[0])
    for c in five_cards[1:]:
        if s != get_card_suit_id(c):
            return False
    return True

# 顺子：牌型分就是最大牌的数字大小
def is_straight(five_cards) -> tuple:
    nums = sorted([get_card_num_id(c) for c in five_cards])
    if nums == [0, 1, 2, 3, 12]:
        return True, [3]
    n4 = nums[4]
    for i, n in enumerate(nums[:4]):
        if n4 - n != 4 - i:
            return False, [0]
    return True, [n4]
    

def get_type(five_cards):
    straight, straight_value = is_straight(five_cards)
    flush = is_flush(five_cards)
    if flush and straight:
        return 8, straight_value
    if flush:
        return 5, None  # sorted([get_card_num_id(c) for c in five_cards], reverse=True)
    if straight:
        return 4, straight_value
    nums = [0] * 13
    for card in five_cards:
        nums[get_card_num_id(card)] += 1
    max_freq = max(nums)
    if max_freq == 1:
        return 0, None  # sorted([get_card_num_id(c) for c in five_cards], reverse=True)
    if max_freq == 4:
        return 7, None  # [nums.index(4), nums.index(1)]
    if max_freq == 3:
        if min(nums) == 2:
            return 6, None  # [nums.index(3), nums.index(2)]
        return 3, None
    # max_freq == 2
    if nums.count(2) == 1:
        return 1, None
    return 2, None

def get_value(t, v, five_cards):
    if v is not None:
        return v
    if t in (0, 5):
        return sorted((get_card_num_id(c) for c in five_cards), reverse=True)
    nums = [0] * 13
    for card in five_cards:
        nums[get_card_num_id(card)] += 1
    return sorted(list(set(get_card_num_id(c) for c in five_cards)), reverse=True, key=lambda x: (nums[x] << 5) + x)
    
def get_max_score(seven_cards:list) -> tuple:
    max_type = -1
    res = []
    for cards in combinations(seven_cards, 5):
        t, v = get_type(cards)
        if t > max_type:
            max_type = t
            res = [(t, v, cards)]
        elif t == max_type:
            res.append((t, v, cards))
    print(res)
    max_value = get_value(*res[0])
    for r in res[1:]:
        value = get_value(*r)
        if value > max_value:
            max_value = value
    return max_type, max_value

