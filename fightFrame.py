


from .picture_make import image_add_text

#只使用一次的函数


from .skill_passive import skill_p
from .skill_active import skill_a
def onlyUse(two, isDispaly, actType, txts, count) :
    
    for i in range(2) :
        if two[i].skill == 6 :
            skill_p( two, i, actType, isDispaly, 0, txts, count)
        
        if two[i].only == 1 and two[i].used == 0 :
            skill_p( two, i, actType, isDispaly, 0, txts, count)
        
    

    return 
    





#显示
def displays (two,  count,  isDispaly, txts):
    if isDispaly == 1 :
        txts.append("第{}回合后: {}血量剩余{} {}血量剩余{}".format  (count, two[0].name, two[0].life, two[1].name, two[1].life))
        
    

    return None

#判断先后手
def   prioritys (left,  right,  two) :
    if left.priority != 1 and right.priority != 1 :
        if left.speed > right.speed :
            left.priority = 1
        
        else :
            right.priority = 1
        
    
    if left.priority > right.priority :
        two[0] = left
        two[1] = right
    
    else :
        two[0] = right
        two[1] = left
    
    return two

#防守判定&血量计算
def   calLife(  two,  order,  isDispaly,  attackPer,  defensePer,  detail,  mess ,txts, count):
    #混乱伤害显示调换
    inCal = 1
    if mess > 0 :
        tmp = 0
        tmp = defensePer
        defensePer = attackPer
        attackPer = tmp

    
    #进攻的现在防守
    if order == 1 :
        order = 0
    
    else :
        order = 1
    
    #挑选对应防守被动
    for i in range(2):
        
        if skill_p( two, i, 0, isDispaly, inCal, txts, count):
            return True
        two[i].life -= two[i].attacked
    
    if isDispaly == 1 :
        if two[defensePer].life <= 0:
            two[defensePer].life = 0
        
        if detail == 1 and two[defensePer].attacked != 0 :
            txts.append("{}减少了{}的血量,当前血量：{}".format  (two[defensePer].name, two[defensePer].attacked, two[defensePer].life))
        
        else :
            txts.append("{}当前血量:{}".format  (two[defensePer].name, two[defensePer].life))
        
    
    two[attackPer].attacked = 0
    two[defensePer].attacked = 0        
    return False


#状态计算
def calState(two,  isDispaly, txts, attacker):
    #撕裂伤害bug太多，单独计算
    if two[attacker].tear_time > 0:
        if two[attacker].tear_time > 0 and two[attacker].tear_time < 4: 
            
            two[attacker].life -= two[attacker].stateHarmed
            if isDispaly == 1:
                txts.append("{}受到撕裂伤害: 4".format(two[attacker].name))
        two[attacker].tear_time -= 1
                    
    
    for i in range(2) :
        #施加状态
        if two[i].StateTimes_op > 0 :
            
            two[i].attack += two[i].AttackTmpChanged 
            two[i].effected = 1
            two[i].StateTimes_op = two[i].StateTimes_op - 1
            two[i].state_ying_kesimo -= 1
            if two[i].state_ying_kesimo < 0:
                two[i].state_ying_kesimo = 0
            two[i].defensiveness += two[i].defensivenessTmpChanged
            two[i].silence = two[i].silenceChanged
            two[i].free = two[i].freechanged
            if two[i].skill != 11 :
                two[i].freechanged = 1
            
            elif two[i].StateTimes_op < 2 :
                two[i].freechanged = 1
            

            if two[0].skill == 9 and two[1].skill == 6 :
                if two[0].StateTimes_op >= 4 :
                    two[0].freechanged = 0
                
                else :
                    two[0].freechanged = 1
                

            
            two[i].silenceChanged = 0
            two[i].mess = two[i].messChanged
            if isDispaly == 1 :
                if two[i].silence == 1 :
                    txts.append("{}被沉默,无法释放主被动".format  (two[i].name))
                
                if two[i].free == 0 :
                    txts.append("{}本回合无法行动".format  (two[i].name))
                

            

            if two[i].StateTimes_op <= 0 :
                two[i].effected = 2
            
        
        elif two[i].effected == 2 :
            two[i].attack -= two[i].AttackTmpChanged
            two[i].defensiveness -= two[i].defensivenessTmpChanged
            two[i].silence = two[i].silenceChanged
            two[i].free = two[i].freechanged
            two[i].mess = 0
            two[i].messChanged = 0
            two[i].effected = 0
        else :
            pass
        #自身状态
        if two[i].StateTimes_self > 0:           
            two[i].StateTimes_self = two[i].StateTimes_self - 1
            two[i].effectedSelf = 1
            two[i].speed += two[i].speedChanged 

            if two[i].StateTimes_self <= 0 :
                two[i].effectedSelf = 2 
            
        
        elif two[i].effectedSelf == 2:
            two[i].speed -= two[i].speedChanged
            two[i].stateHarmed = 0
            two[i].free = two[i].freechanged
            two[i].effectedSelf = 0
        else:
            pass
        
        #千劫特有状态
        if two[i].StateTimes_self_jie > 0 :
            two[i].effectedSelf_jie = 1
            two[i].StateTimes_self_jie = two[i].StateTimes_self_jie - 1;
            two[i].free = two[i].freechanged
            if two[i].StateTimes_self_jie <= 0:
                two[i].effectedSelf_jie = 2
            
        
        elif two[i].effectedSelf_jie == 2 :
            two[i].freechanged = 1
            two[i].free = two[i].freechanged
            two[i].effectedSelf_jie = 0
        
        else :
            pass
    
    return two



#对战主体
def   fight(  left,  right,  isDispaly,  two) :
    count = 0
    txts = []
    while left.life > 0 and right.life > 0:
        #回合数
        count = count + 1
        two[0].count = count
        two[1].count = count
        prioritys( left, right, two)#排顺序
        onlyUse( two, isDispaly, 0, txts, count)
        #第一位进攻
        for i in range(2) :
            ordinal_0 = 0
            ordinal_1 = 1
            if i == 1 :
                ordinal_0 = 1
                ordinal_1 = 0
            
            if two[ordinal_0].free != 0:
                two[ordinal_0].count = two[ordinal_0].count + 1
                #技能
                if count % two[ordinal_0].cd == 0 and two[ordinal_0].silence == 0 :
                    if two[ordinal_0].skill == 9 :
                        skill_p( two, i, 1, isDispaly, 1, txts, count)
                    
                    skill_a( two, i, isDispaly, txts, count)
                    
                    if skill_p( two, i, 1, isDispaly, 0, txts, count):
                        return two
                    #挑选对应进攻被动

                    if calLife( two, i, isDispaly, ordinal_0, ordinal_1, 1, 0, txts, count):
                        return two
                    calState( two, isDispaly, txts, ordinal_0)#计算状态
                    if two[ordinal_1].life <= 0 :
                        two[ordinal_0].isDisplayVictory = 1
                        if(isDispaly == 1):
                            image_add_text(count, txts,  text_color=(0, 0, 0), text_size=12)
                            for i in txts:
                                print(i)
                            print()
                        
                        txts.clear()
                        return two
                    
                    
                
                #普攻
                else :
                    if two[ordinal_0].skill == 9 :
                        skill_p( two, i, 1, isDispaly, 1, txts, count)
                    
                    if two[ordinal_0].mess > 0 :
                        if isDispaly == 1 :
                            # txts.append("{}处于混乱状态,普攻将返还自身".format  (two[ordinal_0].name))
                            txts.append("{}处于混乱状态,普攻将返还自身".format  (two[ordinal_0].name))
                        
                        two[ordinal_0].attacked = two[ordinal_0].attack - two[ordinal_0].defensiveness
                        two[ordinal_0].StateTimes_op = 1
                        
                        
                    else :
                        two[ordinal_1].attacked = two[ordinal_0].attack - two[ordinal_1].defensiveness
                        if isDispaly == 1 :
                            # txts.append("{}进行普攻".format (two[ordinal_0].name))
                            txts.append("{}进行普攻".format (two[ordinal_0].name))
                                                                    
                    if skill_p( two, i, 1, isDispaly, 0, txts, count):
                        return two
                    #挑选对应进攻被动
                    if calLife( two, i, isDispaly, ordinal_0, ordinal_1, 1, two[ordinal_0].mess, txts, count):
                        return two
                    calState( two, isDispaly, txts, ordinal_0) 
                    if two[ordinal_1].life <= 0:
                        two[ordinal_0].isDisplayVictory = 1
                        if isDispaly == 1:
                            image_add_text(count, txts,  text_color=(0, 0, 0), text_size=12)
                            for i in txts:
                                print(i)
                            print()
                        txts.clear()
                        return two
                    if two[ordinal_0].life <= 0:
                        two[ordinal_1].isDisplayVictory = 1
                        if isDispaly == 1:
                            image_add_text(count, txts,  text_color=(0, 0, 0), text_size=12)
                            for i in txts:
                                print(i)
                            print()
                        txts.clear()
                        return two
                    
                    

                
                                    
            
            
        
        displays(two, count, isDispaly, txts)#血量显示
        two[0].priority = 0
        two[1].priority = 0
        if isDispaly == 1:
            image_add_text(count, txts,  text_color=(0, 0, 0), text_size=12)
        
        
            for i in txts:
                print(i)
            print()
        txts.clear()

    return two


