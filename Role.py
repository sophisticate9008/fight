


class Role:
    life = 100
    defensiveness = 0
    attack = 0
    speed = 0
    cd = 0
    name = ""
    isConfusion = 0
    priority = 0
    free = 1
    Shield = 0
    count = 0
    skill = 0
    StateTimes_op = 0
    StateTimes_self = 0
    stateHarmed = 0
    AttackTmpChanged = 0
    typePassive = 0
    attacked = 0
    defensivenessTmpChanged = 0
    isDisplayVictory = 0
    effected = 1
    defensivenessInced = 0
    StateTimes_op_st = 0
    silence = 0
    freechanged = 1
    swordStore = 0
    silenceChanged = 0
    effectedSelf = 0
    mess = 0
    messChanged = 0
    only = 0
    used = 0
    speedChanged = 0
    StateTimes_self_jie = 0
    effectedSelf_jie = 0
    messPassed = 0    
    count = 0
    def __init__(self, name,  attack,  defensiveness,  speed,  cd,  skill,  typePassive):
        self.name = name
        self.defensiveness = defensiveness
        self.attack = attack
        self.speed = speed
        self.cd = cd
        self.skill = skill
        self.typePassive = typePassive
    


