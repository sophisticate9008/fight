
from .Role import Role
from .fightFrame import fight

def creates(list_info, left,  right,  n,  isDisplay) :
    
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
    for i in range(n) :
        left1 = roles[left]
        right1 = roles[right]
        two =  [Role] * 2
        fight( left1, right1, isDisplay, two)
        if roles[left].isDisplayVictory == 1 :
            # print( "{}获胜".format (roles[left].name))
            list_info.append(left)
            list_info.append(roles[left].count)
            return list_info
        
        else :
            # print( "{}获胜".format (roles[right].name))
            list_info.append(right)
            list_info.append(roles[right].count)
            return list_info
        
        

    
    return 0 

