


import random
from .Role import Role
from .fightCreate import creates





def stats(rands1, rands2, isDisplay, n, list_prob:list):
        rands = 0
        roles = []
        roles.append(Role("凯文", 20, 11, 21, 3, 0, 1))
        roles.append(Role("爱莉希雅", 21, 8, 20, 2, 1, 1))
        roles.append(Role("格蕾修", 16, 11, 18, 3, 2, 1))
        roles.append(Role("樱", 24, 10, 27, 2, 3, 0))
        roles.append(Role("阿波尼亚", 21, 10, 30, 4, 4, 1))
        roles.append(Role("华", 21, 12, 15, 2, 5, 0))
        roles.append(Role("维尔薇", 20, 12, 25, 3, 6, 0))
        roles.append(Role("科斯魔", 19, 11, 19, 2, 7, 1)) 
        roles.append(Role("梅比乌斯", 21, 11, 23, 3, 8, 1))
        roles.append(Role("千劫", 23, 9, 26, 3, 9, 1) )
        roles.append(Role("帕朵菲莉丝", 17, 10, 24, 3, 10, 1))
        roles.append(Role("伊甸", 16, 12, 16, 2, 11, 1))
        left = rands1
        right = rands2
        count_l = 0.0
        count_r = 0.0
        list_info = []
        for i in range(n) :
            creates(list_info, left, right, n, isDisplay)
            if list_info[0] == left :

                count_l = count_l + 1
                roles[left].isDisplayVictory = 1
                roles[left].count = list_info[1]
            else :
                count_r = count_r + 1
                roles[right].isDisplayVictory = 1
                roles[left].count = list_info[1]
            list_info.clear()
        list_prob.append(roles[left].name)
        list_prob.append((count_l))
        list_prob.append(roles[right].name)
        list_prob.append((count_r))
        list_prob.append(roles[left])
        list_prob.append(roles[right])
        return list_prob
        
        
    

