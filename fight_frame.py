from .Roles import *
from typing import List

def stats(left, right, is_display, n, list_prob:list):
    count_l = 0
    count_r = 0
    role1 = get_role(left)
    role2 = get_role(right)
    result = {}
    for i in range(n):
        result = fight(left, right, is_display)
        if role1.name == result["winner"]:
            count_l += 1
        else:
            count_r += 1
    list_prob.append(role1.name)
    list_prob.append(count_l)
    list_prob.append(role2.name)
    list_prob.append(count_r)
    list_prob.append(0  if result["winner"] == role1.name else 1)
    list_prob.append(result["txtss"])
    list_prob.append(role1)
    list_prob.append(role2)
    return list_prob
    
def fight(left, right, is_display):
    result = {}
    txtss: List[List[str]] = []
    role1: RoleBase = get_role(left)
    role2: RoleBase = get_role(right)
    role1.enemy = role2
    role2.enemy = role1
    role1.init()
    role2.init()
    role1.is_display = is_display
    role2.is_display = is_display
    role1.result = result
    role2.result = result
    roles = [RoleBase] * 2
    count_turn = 0
    while role1.blood > 0 and role2.blood > 0:
        count_turn += 1
        txts = []
        txts.append(f"第{count_turn}回合")
        if role1.speed >= role2.speed:
            roles[0] = role1
            roles[1] = role2
        else:
            roles[0] = role2
            roles[1] = role1

        for role in roles:
            role.turn_init()
            role.txts = txts
            
        for role in roles:
            role.turn_begin()
        if is_display:
            txtss.append(txts)
    result["txtss"] = txtss
    result["count"] = count_turn
    return result

def get_role(id: int):
    if id == 0:
        return KaiWen(id, "凯文", 21, 20, 11, 3, 0.3, 1)
    elif id == 1:
        return Elysia(id, "爱莉希雅", 20, 21, 8, 2, 0.35, 1)
    elif id == 2:
        return GeLeiXiu(id, "格蕾修", 18, 16, 11, 3, 0.4, 1)
    elif id == 3:
        return Sakura(id, "樱", 27, 24, 10, 2, 0.15, 0)
    elif id == 4:
        return ABoNiYa(id, "阿布尼亚", 30, 21, 10, 4, 0.3, 1)
    elif id == 5:
        return Hua(id, "华", 15, 21, 12, 2, 1, 0)
    elif id == 6:
        return WeiErWei(id, "维尔薇", 25, 20, 12, 3, 1, 0)
    elif id == 7:
        return KeSiMo(id, "科斯魔", 19, 19, 11, 2, 0.15, 1)
    elif id == 8:
        return MeiBiWuSi(id, "梅比乌斯", 23, 21, 11, 3, 0.33, 1)
    elif id == 9:
        return QianJie(id, "千劫", 26, 23, 9, 3, 1, -1)
    elif id == 10:
        return PaDuoFeiLiSi(id, "帕朵菲利斯", 24, 17, 10, 3, 0.3, 1)
    elif id == 11:
        return YiDian(id, "伊甸", 16, 16, 12, 2, 0.5, 1)
    
# if __name__ == "__main__":
#     # for i in range(1, 12):
#     #     for j in range(1, 12):
#     #         if i != j:
#     #             stats(i,j,0,1,[])
#     #             pass
    
#     fight(1, 3, 1)
