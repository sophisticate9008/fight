





#1 进攻触发
#0 防守触发
import random





def skill_p( two, order, actType, isDisplay, inCal, txts:list, count) :
    
    first = 0
    second = 0
    
    if(order == 0) :
        first = 0
        second = 1
    
    else :
        first = 1
        second = 0
    
    #凯文技能
    if(two[first].skill == 0) :
        if(two[first].typePassive == actType and two[first].silence == 0 and two[first].mess == 0) :
            if(random.randint(1,100) < 30 and two[second].life < 30) :
                two[second].life = 0
                if(isDisplay == 1) :
                    txts.append("凯文触发了被动：炎热归零")
                two[first].isVictory = 1
                from .picture_make import image_add_text
                if isDisplay == 1:
                    image_add_text(count, txts,  text_color=(0, 0, 0), text_size=12)
                
                    for i in txts:
                        print(i)
                    print()
                txts.clear()
                return True
            
        

    
    #爱莉希雅技能
    if(two[first].skill == 1) :
        if(two[first].typePassive == actType and two[first].silence == 0) :
            if(random.randint(1,100) <= 35) :
                if(two[first].mess > 0) :
                    two[first].attacked += 11
                    if(isDisplay == 1) :
                        txts.append("爱莉希雅触发了被动：水花溅射")
                        txts.append("由于混乱,伤害返还")
                    from .fightFrame import calLife
                    calLife(two, order, isDisplay, first, second, 1, two[first].mess, txts, count)
                    if(two[first].life == 0) :
                        two[second].isVictory = 1
                        return True
                    
                    two[first].mess = 0
                
                else :
                    two[second].attacked += 11
                    if(isDisplay == 1) :
                        txts.append("爱莉希雅触发了被动：水花溅射")
                    
                
            

        

    
    #格蕾修技能
    if(two[first].skill == 2) :
        
        if(two[first].typePassive == actType and two[first].silence == 0) :
            if(random.randint(1,100) <= 40) :                    
                two[first].defensivenessInced += 2
                if(two[first].defensivenessInced <= 10) :
                    two[first].defensiveness += 2
                
                if(isDisplay == 1) :
                    txts.append("格蕾修触发了被动：沙滩监护人")
                    txts.append("防御力上升2点,目前防御力为{}".format(two[first].defensiveness))
                
            
        
        else :
            if(two[first].StateTimes_self >= 0) :
                if(two[first].Shield > 0) :
                    if(two[first].Shield > two[first].attacked) :
                        two[first].Shield -= two[first].attacked
                        two[first].attacked = 0
                    
                    if(two[first].Shield > 0 and two[first].attacked > two[first].Shield) :
                        two[first].attacked -= two[first].Shield
                        two[first].Shield = 0
                        two[first].StateTimes_self = 0
                        tmp = (int)(two[first].defensiveness * (random.randint(1, 200) + 200) / 100)
                        two[second].attacked = tmp - two[second].defensiveness
                        if(isDisplay == 1) :
                            txts.append("格蕾修护盾碎裂,对{}发动数值为{}的物理伤害".format (two[second].name, tmp))
                            txts.append("格蕾修受到剩余伤害{}".format(two[first].attacked))
                        from .fightFrame import calLife
                        calLife(two, order, isDisplay, first, second, 1, 0, txts, count)
                        if(two[first].life == 0) :
                            two[second].isDisplayVictory = 1
                            from .picture_make import image_add_text
                            if isDisplay == 1:
                                image_add_text(count, txts,  text_color=(0, 0, 0), text_size=12)
                            
                                for i in txts:
                                    print(i)
                                print()
                            txts.clear()
                            return True
                        
                        elif(two[second].life == 0) :
                            two[first].isDisplayVictory = 1
                            from .picture_make import image_add_text
                            if isDisplay == 1:
                                image_add_text(count, txts,  text_color=(0, 0, 0), text_size=12) 
                                                       
                                for i in txts:
                                    print(i)
                                print()
                            txts.clear()
                            return True
                        
                    
                
                
        
    

    #樱技能
    if(two[first].skill == 3) :
        if(two[first].typePassive == actType and two[first].silence == 0) :
            if(random.randint(1,100) <= 15) :
                if(two[first].mess == 0) :
                    if(two[first].attacked != 0) :
                        two[first].attacked = 0
                        if(isDisplay == 1) :
                            txts.append("樱触发了被动技能：夏之型.樱流，闪避了攻击")
                        
                    
                
                two[first].StateTimes_self = 1
            
            if(two[first].StateTimes_self >= 1 and two[first].StateTimes_op == two[first].StateTimes_op_st and two[first].StateTimes_op != 0) :
                if(isDisplay == 1) :
                    txts.append("樱没有获得附加状态")
                if two[first].state_ying_kesimo == 6:
                    two[first].state_ying_kesimo = 0
                two[first].free = 1
                two[first].StateTimes_op = 0
                two[first].StateTimes_op += two[first].state_ying_kesimo
                two[first].StateTimes_self = 0
            
        

    
    #阿波尼亚
    if(two[first].skill == 4) :
        
        if(two[first].typePassive == actType and two[first].silence == 0) :
            if(random.randint(1,100) <= 30) :
                if(two[first].mess > 0) :
                    two[first].silenceChanged = 1
                    two[first].StateTimes_op = 2
                    two[first].StateTimes_op_st = 2
                    if(isDisplay == 1) :
                        txts.append("阿波尼亚触发被动:该休息了,但由于混乱,返还自身".format(two[second].name))
                    
                
                else :

                    two[second].silenceChanged = 1
                    two[second].StateTimes_op = 1
                    two[second].StateTimes_op_st = 1
                    
                    if(isDisplay == 1) :
                        txts.append("阿波尼亚触发被动:该休息了".format (two[second].name))
                        
                    
                

            
        
    
    #华技能
    if(two[first].skill == 5) :
        if(two[first].swordStore >= 1) :
            two[first].swordStore =  two[first].swordStore + 1

        
        if(two[first].typePassive == actType) :


                two[first].attacked = int(round(two[first].attacked * 0.8))

        
        else :
            if(two[first].swordStore >= 3) :
                two[first].swordStore = 0
                two[first].defensiveness -= 3
                rands = random.randint(0, 24) + 10
                if(two[first].silence == 0) :
                    two[second].attacked += rands
                    if(isDisplay == 1) :
                        txts.append("华蓄力完成,攻击将附加{}元素伤害".format(rands))
                        txts.append("攻击后防御力下降3,当前防御力为{}".format(two[first].defensiveness))
                    
                
            
            
        
            
    
    #维尔薇
    if(two[first].skill == 6) :
        if(two[first].typePassive == actType) :
            if(two[first].life < 31) :
                two[first].only = 1
            
        
        if(two[first].only == 1 and two[first].used == 0 and inCal == 0) :
            rands1 = random.randint(0, 11) + 10
            rands2 = random.randint(0, 11) + 10
            rands3 = random.randint(0, 14) + 2
            two[first].life += rands1
            two[second].life += rands2
            two[first].attack += rands3
            if(isDisplay == 1) :
                txts.append("维尔薇释放大变活人")
                txts.append("维尔薇回复{}点血量,{}回复{}点血量".format (rands1, two[second].name, rands2))
                txts.append("维尔薇当前血量为{},{}当前血量为{}".format  (two[first].life, two[second].name, two[second].life))
                txts.append("维尔薇增加{}攻击力,当前攻击力为{}".format  (rands3, two[first].attack))
            
            two[first].used = 1
        
    
    #科斯魔
    if(two[first].skill == 7) :
        if(two[first].typePassive == actType and two[first].silence == 0) :
            if(random.randint(1,100) <= 15) :
                if(two[first].mess > 0) :
                    two[first].StateTimes_op = 6
                    two[first].stateHarmed = 4
                    if(isDisplay == 1) :
                        txts.append("科斯魔触发了被动技:不归之爪,但由于混乱,撕裂状态返还自身")
                    
                    
                
                else :
                    two[second].StateTimes_op = 6
                    two[second].StateTimes_op_st = 6
                    two[second].state_ying_kesimo = 6
                    two[second].stateHarmed = 4
                    if(isDisplay == 1) :
                        txts.append("科斯魔触发了被动技:不归之爪,{}进入撕裂状态".format  (two[second].name))
                    
                
            

        
    
    #梅比乌斯技能
    if(two[first].skill == 8) :
        if(two[first].typePassive == actType and two[first].silence == 0) :
            if(random.randint(1,100) <= 33) :
                if(two[first].mess > 0) :
                    two[first].defensiveness -= 3
                    if(two[first].defensiveness < 0) :
                        two[first].defensiveness = 0
                    
                    if(isDisplay == 1) :
                        txts.append("梅比乌斯触发被动技:不稳定物质,但由于混乱,状态返回自身")
                        txts.append("梅比乌斯防御力下降三点,当前防御力为:{}".format  (two[first].defensiveness))
        
                    
                
                else :
                    two[second].defensiveness -= 3
                    if(two[second].defensiveness < 0) :
                        two[second].defensiveness = 0
                    
                    if(isDisplay == 1) :
                        
                        txts.append("梅比乌斯触发被动：不稳定物质，{}防御力下降三点,当前防御力为:{}".format  (two[second].name, two[second].defensiveness))
        
                    
                
            
        
    
    #千劫技能
    if(two[first].skill == 9) :
        if(two[first].typePassive == actType and inCal == 1) :
            two[first].attack = 23 + int ((100 - two[first].life) / 5)
            if(isDisplay == 1) :
                txts.append("千劫被动:夏之狂热触发,增加攻击力,当前攻击力为{}".format  (two[first].attack))
            
        
    
    #猫猫技能
    if(two[first].skill == 10) :
        if(two[first].typePassive == actType and two[first].silence == 0) :
            if(random.randint(1,100) <= 30) :
                two[second].attacked += 30 - two[second].defensiveness
                if(isDisplay == 1) :
                    txts.append("帕朵菲莉丝召唤了罐头,发动了30点物理伤害")
                
            
        
    
    #伊甸技能
    if(two[first].skill == 11) :
        if(two[first].typePassive == actType and two[first].silence == 0) :
            if(random.randint(1,100) <= 50) :
                two[second].attacked += two[first].attack - two[second].defensiveness
                if(isDisplay == 1) :
                    txts.append("伊甸触发被动:海边协奏,额外普攻一次")
                
            
        
    
    return False



