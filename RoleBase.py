import random
from typing import Dict

class RoleBase:
    is_display: bool = True
    ad: int = 0
    ap: int = 0
    id: int = 0
    speed: int = 0
    blood:int = 100
    attack: int = 0
    cd: int = 0
    action_num: int = 0
    name: str = ""
    harmed: int = 0
    defence: int = 0
    prob_p: float = 0.0
    count_turn: int = 0
    enemy: 'RoleBase' = None
    shield: int = 0
    type_p: int = 0
    silent: bool = False
    chaos: bool = False
    tear: int = 0
    def __init__(self, id: int, name: str, speed: int, attack: int, defence: int, cd: int, prob_p: float, type_p: int):
        self.name = name
        self.speed = speed
        self.attack = attack
        self.defence = defence
        self.cd = cd
        self.prob_p = prob_p
        self.id = id
        self.type_p = type_p
        self.original_funcs: Dict[str,any] = {}
    def init(self):
        self.tear = 0 #使其出现在__dict__中
    def turn_init(self):
        self.count_turn += 1
        self.action_num += 1
        self.silent = False
    def turn_begin(self):
        self.cal_tear_harm()
        self.judge_action()
    def text_handle(self, text:str):
        if self.is_display == 1:
            self.txts.append(text)

    def cal_tear_harm(self):
        if self.tear > 0:
            self.tear -= 1
            self.blood -= 4
            text = f"{self.name}由于撕裂,血量减少4点,剩余血量{self.blood}"
            self.text_handle(text)
        self.judge_winner()
    def judge_action(self):
        if self.action_num < 1 :
            text = f"{self.name}无法行动"
            self.text_handle(text)
        else:
            self.action_num -= 1
            self.action()
            
        
        
    def skill_passive_trigger(self, type_p: int):  #1攻击  0 防御
        
        if not self.silent:
            if self.type_p == type_p:
                rand = random.randint(1, 100)
                if rand <= self.prob_p * 100:
                    self.skill_passive()
                    if self.type_p == 1:
                        if self.chaos:
                            self.cal_harmed()
                            self.cal_blood()
                        else:
                            self.enemy.cal_harmed()
                            self.enemy.cal_blood()
                    
    def action(self): 
        if self.count_turn % self.cd == 0 and not self.silent:
            self.skill_action()
        else :
            self.attack_normal()
            
        self.skill_passive_trigger(1)
        self.cal_and_trigger()
    
    def cal_and_trigger(self):
        self.enemy.skill_passive_trigger(0)
        self.enemy.cal_harmed()
        self.enemy.cal_blood()

        
    def cal_blood(self): # 计算血量
        self.blood -= self.harmed
        if self.harmed > 0:
            text = f"{self.name}实际受到{self.harmed}点伤害，当前剩余血量{self.blood}点"
            self.text_handle(text)
        self.harmed = 0
        self.judge_winner()
    def judge_winner(self):
        if self.blood <= 0:
            if self.result.get("winner"):
                pass
            else:
                self.result["winner"] = self.enemy.name
    def cal_harmed(self): # 计算伤害
        self.harmed += self.enemy.ap
        self.harmed += self.enemy.ad - self.defence if self.enemy.ad - self.defence > 0 else 0
        self.enemy.ad = 0
        self.enemy.ap = 0
        
    def attack_normal(self): # 普通攻击
        text = f'{self.name}发动普通攻击,造成{self.attack}点伤害'
        if self.chaos:
            text += '但由于混乱，返还自身'
            self.text_handle(text)
            self.enemy.ad += self.attack
            self.cal_harmed()
            self.cal_blood()
        else:
            self.ad += self.attack
            self.text_handle(text)
        self.chaos = False


    def skill_action(self): # 主动
        pass
    def skill_passive(self): # 被动
        pass
        
    