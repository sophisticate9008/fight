

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
        if me := await cls.get_or_none(uid=uid, group_id=group_id):
            me.loss -= (type -1) * gold
            me.gain += type * gold
            me.fight_count += 1
            await me.save()
        else:
            await cls.create(
                uid=uid,
                group_id=group_id,
                loss = -(type -1) * gold,
                gain = type * gold,
                fight_count = 1)
    @classmethod
    async def my(cls, group_id, uid):
        if me := await cls.get_or_none(uid=uid, group_id=group_id):
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

                                                
             

               
