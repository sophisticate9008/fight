import random
from .RoleBase import RoleBase
import copy

saved_state = None
class KaiWen(RoleBase):
    def skill_action(self):
        self.attack += 5
        self.ap += 25
        text = f"凯文-清凉一剑触发,攻击力加5,造成25点魔法伤害"
        self.text_handle(text)
    
    def skill_passive(self):
        if self.chaos:
            return
        if(self.enemy.blood <= 30):
            self.enemy.blood = 0
            text = f"凯文-炎热归零触发,敌方血量归零"
            self.text_handle(text)



class Elysia(RoleBase):
    
    def skill_action(self):
        rand = random.randint(25, 50)
        self.ad += rand
        text = f"爱莉希雅-夏梦之花发动,造成{rand}点物理伤害,对手下次行动攻击力-6"
        self.text_handle(text)
        self.enemy.original_funcs["elysia>action"] = self.enemy.action
        def update_enemy_action(self:'RoleBase',func):
            def wrapper():
                self.attack -= 6
                func()
                self.attack += 6
                self.action = self.original_funcs["elysia>action"]
            return wrapper
        
        self.enemy.action = update_enemy_action(self.enemy,self.enemy.action)
    
    def skill_passive(self):
        text = "爱莉希雅-水花溅射触发,造成11点魔法伤害"
        if self.chaos:
            self.enemy.ap += 11
            text += "但由于混乱返回自身"
        else:
            self.ap += 11
            
        self.text_handle(text)


class GeLeiXiu(RoleBase):
    defence_add = 0
    def skill_action(self):
        text = "格蕾修-水彩泡影发动,获得15点护盾"
        if self.shield > 0:
            self.ad += self.defence
            text += f"由于护盾未碎裂,对对手造成{self.defence}点伤害"
        self.shield = 15
        self.text_handle(text)


    def cal_harmed(self):
        harmed = 0
        super().cal_harmed()
        if self.shield > 0:
            self.harmed_rest = self.harmed - self.shield if self.harmed - self.shield > 0 else 0
            self.shield -= self.harmed
            self.harmed = self.harmed_rest
            harmed = self.harmed
            self.harmed_rest = 0
            self.cal_blood()

            if self.shield <= 0:
                self.shield = 0
                self.shield_boom()
        return harmed

    def skill_passive(self):
        if self.defence_add < 10:
            
            self.defence_add += 2
            self.defence += 2
            text = f'格蕾修-沙滩监护人触发,防御力+2,当前为{self.defence}'
            self.text_handle(text)

    def shield_boom(self):
        
        rand = random.randint(200, 400)
        self.ad += self.defence * rand // 100
        text = f"格蕾修护盾碎裂,对敌方造成{self.defence * rand // 100}点物理伤害"
        self.text_handle(text)
        self.cal_and_trigger()

        
        
class Sakura(RoleBase):
    rand_dodge = 100
    action_able = True
    def skill_action(self):
        rand = random.randint(1, 5)
        self.blood = self.blood + rand if self.blood + rand < 100 else 100
        self.ad += self.attack * 130 // 100
        text = f"樱-夏之型-瓜切发动,回复了{rand}点血量, 对敌方造成{self.attack * 130 // 100}点物理伤害"
        self.text_handle(text)
        
    def init(self):
        super().init()
        def update_turn_begin(self: 'RoleBase', func):
            def wrapper():
                global saved_state
                saved_state = copy.deepcopy(self.enemy)
                func()
            return wrapper
        #对面回合开始时保留樱状态,闪避后回溯
        self.enemy.turn_begin = update_turn_begin(self.enemy, self.enemy.turn_begin)
    
    def cal_tear_harm(self):
        super().cal_tear_harm()
        global saved_state
        saved_state = copy.deepcopy(self)
    
    def judge_action(self):
        if self.action_num < 1:
            self.action_able = False
        else:
            self.action_able = True
        super().judge_action()

    def skill_passive(self):
        if self.rand_dodge > self.prob_p * 100:
            self.rand_dodge = random.randint(1, 100)
            self.judge_dodge()
        else:
            self.judge_dodge()
    def judge_dodge(self):

        if self.rand_dodge <= self.prob_p * 100:
            if not self.action_able:
                return            
            self.enemy.ap = 0
            self.enemy.ad = 0
            self.harmed = 0
            text = f"樱-夏之型-樱流触发,闪避了"
            self.text_handle(text)
            
    def turn_init(self):
        super().turn_init()
        self.rand_dodge = random.randint(1, 100)
    def cal_blood(self):
        if self.rand_dodge > self.prob_p * 100:
            super().cal_blood()
        else:
            if not self.action_able:
                return
            global saved_state
            update_dict = {}
            for key, value in saved_state.__dict__.items():
                if key != "enemy" and key != "original_funcs" and key != "result":
                    update_dict[key] = value
            self.__dict__.update(update_dict)
            self.count_turn = self.enemy.count_turn
            for key in self.original_funcs.keys():
                args = key.split(">") 
                setattr(self, args[1], self.original_funcs[key])
            self.enemy.ad = 0
            self.enemy.ap = 0

        
        
    def skill_passive_trigger(self, type_p: int):
        if self.type_p == type_p:
            self.skill_passive()
            
class ABoNiYa(RoleBase):
    def skill_action(self):
        self.ad += self.attack * 170 // 100
        self.enemy.action_num = 0
        text = f"阿波尼亚-深蓝之槛发动,造成{self.ad}点伤害.封禁对手行动"
        self.text_handle(text)
    
    def action(self):
        self.skill_passive_trigger(1)
        if self.count_turn % self.cd == 0 and not self.silent:
            self.skill_action()
        else :
            self.attack_normal()
            
        self.cal_and_trigger()
    
    def skill_passive(self):
        text = f"阿波尼亚-该休息了触发,造成沉默"
        if self.chaos:
            text += "但由于混乱,返还自身"
            self.silent = True
        else:
            self.enemy.silent = True
        self.text_handle(text)
        
class Hua(RoleBase):
    def skill_action(self):
        self.defence += 3
        text = f"华-上伞若水发动,开始蓄力,期间防御力+3,当前为{self.defence}"
        self.text_handle(text)   
        self.original_funcs["hua"] = self.attack_normal
        def update_attack_normal(self: 'RoleBase',func):
            def wrapper():
                self.defence -= 3
                rand = random.randint(10, 33)
                
                text = f"华蓄力完成,防御力恢复,当前为{self.defence},攻击附加{rand}点魔法伤害(无视混乱)"
                self.text_handle( text)
                func()
                self.ap += rand
                self.attack_normal = self.original_funcs["hua"]
            return wrapper
        
        self.attack_normal = update_attack_normal(self,self.attack_normal)
    
    def cal_harmed(self):
        super().cal_harmed()
        self.harmed = self.harmed * 0.8 // 1   

class WeiErWei(RoleBase):
    skill_once = False
    def skill_action(self):
        self.ad += self.attack
        self.enemy.chaos = True
        text = f"维尔薇-创(造)力发动,造成{self.ad}点伤害,并使对手混乱"
        self.text_handle(text)
    
    def skill_passive(self):
        def update_turn_begin(self:'RoleBase',func):
            def wrapper():
                if not self.skill_once:
                    if self.blood <= 30:
                        self.skill_once = True
                        rand1 = random.randint(10, 20)
                        rand2 = random.randint(10, 20)
                        rand3 = random.randint(2, 15)
                        self.blood += rand1
                        self.enemy.blood += rand2
                        self.attack += rand3
                        text = f"维尔薇-大变活人触发,自身获得{rand1}血量,敌方获得{rand2}血量,自身攻击+{rand3}"
                        self.text_handle(text)
                func()
                
            return wrapper
        
        self.turn_begin = update_turn_begin(self,self.turn_begin)

class KeSiMo(RoleBase):
    def skill_action(self):
        text = f"科斯魔-邪渊之钩发动,分别造成"
        for i in range(4):
            rand = random.randint(11, 22)
            text += f" {rand} "
            if self.enemy.tear > 0:
                self.ap += 3
            self.enemy.harmed += rand - self.enemy.defence if rand - self.enemy.defence > 0 else 0
        if self.enemy.tear > 0:
            text += f"由于对手陷入撕裂状态,分别附加3点魔法伤害"
        self.text_handle(text)
    def skill_passive(self):
        text = f"科斯魔-不归之爪触发,造成撕裂效果"
        if self.chaos:
            text += f"但由于混乱,返还自身"
            self.tear = 3
        else:
            self.enemy.tear = 3
        self.text_handle(text)
            
class MeiBiWuSi(RoleBase):
    def action(self):
        if self.count_turn % self.cd == 0:
            self.skill_action()
        else :
            self.attack_normal()
            self.skill_passive_trigger(1)
            
        self.cal_and_trigger()
        
    def skill_action(self):
        self.ad += 33
        rand = random.randint(1, 100)
        text = f"梅比乌斯-栖影水枪发动,造成33点物理伤害"
        if rand <= 33:
            self.enemy.action_num -= 1
            text += "并让敌方陷入昏迷"
        self.text_handle(text)
    def skill_passive(self):
        text = "梅比乌斯-不稳定物质触发,对对手造成防御力-2的效果"
        if self.chaos:
            self.defence = self.defence - 2 if self.defence - 2 > 0 else 0
            text += f"但由于混乱,返还自身,自身防御力为{self.defence}"
        else:
            self.enemy.defence = self.enemy.defence - 2 if self.enemy.defence - 2 > 0 else 0
            text += f"对手防御力为{self.enemy.defence}(闪避前)"
        self.text_handle(text)
            
class QianJie(RoleBase):
    def skill_action(self):
        
        if self.blood >= 11:
            self.blood -= 10
            self.ad += 45
            rand = random.randint(1, 20)
            self.ap += rand
            self.action_num -= 1
            text = f"千劫-盛夏燔祭发动,血量-10,当前为{self.blood},造成45点物理伤害并附带{rand}点魔法伤害并休息一回合"
            self.text_handle(text)
    def skill_passive(self):
        self.attack = 23 + (100 - self.blood) // 5
        text = f"千劫-夏之狂热触发,攻击力增加，当前为{self.attack}"
        self.text_handle(text)
    def action(self):
        self.skill_passive()
        super().action()

class PaDuoFeiLiSi(RoleBase):
    def skill_action(self):
        self.ad += 30
        text = f"帕朵菲利斯-沙滩寻宝发动,造成{self.ad}点伤害"
        self.text_handle(text)
        self.enemy.original_funcs["paduofeilisi>cal_harmed"] = self.enemy.cal_harmed
        def update_enemy_cal_harmed(self:'RoleBase',func):
            def wrapper():
                temp = func()
                blood_recovery = self.harmed
                if temp != None and blood_recovery == 0:
                    blood_recovery = temp
                self.enemy.blood = self.enemy.blood + blood_recovery if self.enemy.blood + blood_recovery < 100 else 100

                if blood_recovery > 0:
                    text = f"帕朵菲利斯-沙滩寻宝效果,恢复{blood_recovery}点血量,当前血量{self.enemy.blood}"
                    self.text_handle(text)
                self.cal_harmed = self.original_funcs['paduofeilisi>cal_harmed']
            return wrapper
        
        self.enemy.cal_harmed = update_enemy_cal_harmed(self.enemy,self.enemy.cal_harmed)
        self.cal_and_trigger()
    
    
    def skill_passive(self):
        text = f"帕朵菲利斯-最佳搭档触发,造成30点物理伤害"
        self.enemy.harmed += 30 - self.enemy.defence
        self.text_handle(text)
        
class YiDian(RoleBase):
    def skill_action(self):
        text = "伊甸-闪亮登场发动,攻击力+4,并发动普通攻击且下次先攻"
        self.text_handle(text)
        self.attack += 4
        self.attack_normal()
        self.origin_speed = self.speed
        self.speed += 100
        self.original_funcs['yidian'] = self.turn_begin
        def update_turn_begin(self:'RoleBase',func):
            def wrapper():
                func()
                self.speed = self.origin_speed
                self.turn_begin = self.original_funcs['yidian']
            return wrapper
        self.turn_begin = update_turn_begin(self,self.turn_begin)
        
    def skill_passive(self):
        text = "伊甸-海边协奏触发,额外发动一次普通攻击"
        if self.chaos:
            text += "但由于混乱,返还自身"
            self.harmed += self.attack - self.defence
        else :
            self.enemy.harmed += self.attack - self.enemy.defence
        self.text_handle(text)