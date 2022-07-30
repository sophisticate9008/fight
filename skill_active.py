
import random





#0 凯文
#1 爱莉希雅
#2 格蕾修
#3 樱
#4 阿波尼亚
#5 华
#6 维尔薇
#7 科斯魔
#8 梅比乌斯


def skill_a(two, order, isDisplay, txts, count) :
    
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
        two[first].attack += 5
        two[second].attacked += 25
        if(isDisplay == 1) :
            txts.append("凯文使用了清凉一剑")
            txts.append("凯文攻击力加5,当前攻击力为{}".format (two[first].attack))
            txts.append("凯文对发动了数值为25点的元素伤害")
            
        

    
    #爱莉希雅技能
    if(two[first].skill == 1) :
        rands = random.randint(0, 26) + 25
        two[second].attacked += rands - two[second].defensiveness
        two[second].StateTimes_op_st = 1
        two[second].StateTimes_op = 1
        two[second].AttackTmpChanged = -6
        if(isDisplay == 1) :
            txts.append("爱莉希雅发动了技能：夏梦水花")
            txts.append("爱莉希雅发动了数值为{}的物理伤害,并让对手攻击力下降6,直到下次行动结束".format  (rands))

        
    
    #格蕾修技能
    if(two[first].skill == 2) :
        if(two[first].Shield > 0) :
            two[first].Shield = 15
            two[second].attacked += two[first].defensiveness - two[second].defensiveness
            if(isDisplay == 1) :
                txts.append("格蕾修发动了技能：水彩泡影")
                txts.append("对{}发动了数值为{}的物理伤害并获得15点护盾值".format (two[second].name, two[first].defensiveness))
            
        
        else :
            two[first].Shield = 15
            if(isDisplay == 1) :
                
                txts.append("格蕾修发动了技能：水彩泡影")
                txts.append("格蕾修获得15点护盾值")
            

        
        two[first].StateTimes_self = 3
    
    #樱技能
    if(two[first].skill == 3) :
        rands = random.randint(0, 5) + 1
        two[first].life += rands
        if(two[first].life > 100) :
            two[first].life = 100
        
        two[second].attacked += (int)(two[first].attack * 1.3) - two[second].defensiveness
        if(isDisplay == 1) :
            txts.append("樱使用了技能：夏之型.瓜切")
            txts.append("回复了{}点的血量,当前血量为{}".format  (rands, two[first].life))
            txts.append("樱对{}发动了数值为{}的物理伤害".format  (two[second].name, (int)(two[first].attack * 1.3)))
        

    
    #阿波尼亚技能  
    if(two[first].skill == 4) :
        two[second].attacked = (int)(two[first].attack * 1.7) - two[second].defensiveness
        two[second].StateTimes_op = 1
        two[second].StateTimes_op_st = 1
        two[second].freechanged = 0


        if(isDisplay == 1) :
            txts.append("阿波尼亚释放了深蓝之槛")
            txts.append("封住了{}的行动并发动了数值为{}的物理伤害".format  (two[second].name, int(two[first].attack * 1.7)))
        
    
    #华技能
    if(two[first].skill == 5) :
        two[first].swordStore = 1
        two[first].defensiveness += 3
        two[first].StateTimes_self = 2
        if(isDisplay == 1) :
            txts.append("华发动技能：上伞若水，开始蓄力")
            txts.append("防御力加3, 当前防御力为{}".format  (two[first].defensiveness))
        
    
    #维尔薇技能
    if(two[first].skill == 6) :
        two[second].attacked = two[first].attack - two[second].defensiveness
        if(isDisplay == 1) :
            txts.append("维尔薇发动技能:创(造)力")
            txts.append("释放了{}的物理伤害".format  (two[first].attack))
        
        two[second].StateTimes_op = 6
        two[second].StateTimes_op_st = 6
        two[second].messChanged = 5
    
    #科斯魔技能
    if(two[first].skill == 7) :
        rands = []
        for i in range(4):
            rands.append(random.randint(0 ,11) + 11)
        for i in range(4):
            if(rands[i] - two[second].defensiveness > 0):
                two[second].attacked += rands[i] - two[second].defensiveness
        if(isDisplay == 1) :
            txts.append("科斯魔进行4次攻击,伤害分别为{} {} {} {}".format ( rands[0], rands[1], rands[2], rands[3]))
        if(two[second].StateTimes_op > 0) :     
            two[second].attacked += 12          
            if(isDisplay == 1) :
                txts.append("{}处于撕裂状态,4次伤害分别附加3点元素伤害".format  (two[second].name))
            
        

    
    #梅比乌斯技能
    if(two[first].skill == 8) :
        two[second].attacked = 33 - two[second].defensiveness
        if(isDisplay == 1) :
            txts.append("梅比乌斯释放技能:栖影水枪,对{}发动33点物理伤害".format  (two[second].name))

        
        if(random.randint(1,100) <= 33) :
            if(two[first].priority == 1) :
                two[second].StateTimes_op = 1                    
            
            else :
                two[second].StateTimes_op = 3
                two[second].StateTimes_op_st = 3
            

            two[second].freechanged = 0
            if(isDisplay == 1) :
                txts.append("{}陷入了沉睡".format  (two[second].name))
            
        
    
    #千劫技能
    if(two[first].skill == 9) :
        if(two[first].life > 11) :
            two[first].life -= 10
            rands = random.randint(0, 20) + 1
            two[second].attacked += 45 - two[second].defensiveness + rands
            two[first].StateTimes_self_jie = 2
            if(two[second].skill == 4) :
                two[first].StateTimes_self_jie = 0
                
            two[first].freechanged = 0
            if(isDisplay == 1) :
                txts.append("千劫释放技能:盛夏燔祭,血量减10,当前血量为{}".format  (two[first].life))
                txts.append("千劫发动45点物理伤害,并附加{}的元素伤害".format  (rands))
            
        
        else :
            two[second].attacked = two[first].attack - two[second].defensiveness
            if(isDisplay == 1) :
                txts.append("千劫血量不足以释放技能,变为发动一次普攻")
            
        
    
    #猫猫技能
    if(two[first].skill == 10) :
        two[second].attacked += 30 - two[second].defensiveness
        two[first].life += two[second].attacked
        if(two[first].life > 100) :
            two[first].life = 100
        
        if(isDisplay == 1) :
            txts.append("帕朵菲莉丝对{}造成了{}的伤害并回复了同等血量".format (two[second].name, two[second].attacked))
            txts.append("帕朵菲莉丝当前生命值为{}".format  (two[first].life))
        
        
        
    
    #伊甸技能
    if(two[first].skill == 11) :
        two[first].attack += 4
        two[first].speedChanged = 20
        
        if(isDisplay == 1) :
            txts.append("伊甸释放技能:闪亮登场,攻击力加4,当前攻击力为{}".format  (two[first].attack))
            txts.append("伊甸下回合先攻")
        
        if(two[first].mess > 0) :
            two[first].StateTimes_self += 2
            two[first].attacked += two[first].attack - two[first].defensiveness
            two[first].StateTimes_op = 1
            from .fightFrame import calState
            calState(two, 0, txts)
            if(isDisplay == 1) :
                txts.append("伊甸发动一次普攻,但由于混乱返还自身")
            from .fightFrame import calLife
            calLife(two, order, isDisplay, first, second, 1, 1, txts, count)
            
        
        else :
            two[first].StateTimes_self += 1
            two[second].attacked += two[first].attack - two[second].defensiveness
            if(isDisplay == 1) :
                txts.append("伊甸发动一次普攻")
            
        

    
    return two






