

from tortoise import fields
from services.db_context import Model
class Fight_record(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    
    group_id = fields.BigIntField()
    uid = fields.BigIntField()
    loss = fields.BigIntField()
    gain = fields.BigIntField()
    fight_count = fields.IntField()
    class Meta:
        table = 'fight_record'
        table_description = "海滨乱斗数据简单记录"
        unique_together = ("uid", "group_id")
        
    @classmethod
    async def record(cls, group_id, uid, gold, type):
        if me := cls.get_or_none(uid=uid, group_id=group_id):
            gold_loss = me.loss
            gold_gain = me.gain
            fight_count = me.fight_count + 1
        else:
            gold_loss = 0
            gold_gain = 0
            fight_count = 1
        if type == 0:
            await cls.update_or_create(
                uid=uid,
                group_id=group_id,
                loss=gold + gold_loss,
                fight_count=fight_count,
                gain=gold_gain
            )                
        else:
            await cls.update_or_create(
                uid=uid,
                group_id=group_id,
                loss=gold_loss,
                fight_count=fight_count,
                gain=gold_gain + gold
            )              
    @classmethod
    async def my(cls, group_id, uid):
        if me := cls.get_or_none(uid=uid, group_id=group_id):
            list_ = []
            list_.append(me.fight_count)
            list_.append(me.gain)
            list_.append(me.loss)
            return list_
        else:
            return 0
    @classmethod
    async def get_all_users(cls, group_id:int):
        return await cls.filter(group_id = group_id).all()

                                                
             

               
