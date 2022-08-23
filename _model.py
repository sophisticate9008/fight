

from services.db_context import db

class Fight_record(db.Model):
    __tablename__ = "fight_record"
    id = db.Column(db.Integer(), primary_key=True)
    group_id = db.Column(db.BigInteger(), nullable=False)
    uid = db.Column(db.BigInteger(),nullable=False)
    loss = db.Column(db.BigInteger(),nullable=False)
    gain = db.Column(db.BigInteger(),nullable=False)
    fight_count = db.Column(db.BigInteger(),nullable=False)
    @classmethod
    async def record(cls, group_id, uid, gold, type):
        query = cls.query.where((cls.group_id == group_id) & (cls.uid == uid))
        query = query.with_for_update()
        me = await query.gino.first()
        if type == 0:    
            if me:
                await me.update(loss = me.loss + gold).apply()
                await me.update(fight_count = me.fight_count + 1).apply()
            else:
                await cls.create(group_id = group_id, uid = uid, loss = gold, gain = 0, fight_count = 1)
        if type == 1:
            if me:
                await me.update(gain = me.gain + gold).apply()
                await me.update(fight_count = me.fight_count + 1).apply()
            else:
                await cls.create(group_id = group_id, uid = uid, loss = 0, gain = gold, fight_count = 1)
    @classmethod
    async def my(cls, group_id, uid):
        query = cls.query.where((cls.group_id == group_id) & (cls.uid == uid))
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            list_ = []
            list_.append(me.fight_count)
            list_.append(me.gain)
            list_.append(me.loss)
            return list_
        else:
            return 0
    @classmethod
    async def get_all_users(cls, group_id:int):
        if not group_id:
            query = await cls.query.gino.all()
        else:
            query = await cls.query.where((cls.group_id == group_id)).gino.all()
        return query

                                                
             

               
