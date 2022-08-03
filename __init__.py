# coding=utf-8
from email.mime import image
from configs.config import NICKNAME
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import (
        GroupMessageEvent,
        MessageEvent,
        GROUP,
        Bot,
        Message
)
from utils.utils import get_message_text
from nonebot.internal.params import ArgStr, Arg
import random
import os
import time
import shutil
from nonebot.params import CommandArg
from .fightStats import stats
path_fight = os.path.dirname(__file__)
from configs.path_config import IMAGE_PATH, FONT_PATH
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from models.bag_user import BagUser
import nonebot
from utils.manager import withdraw_message_manager
from configs.config import Config
__zx_plugin_name__ = "海滨的灼热乱斗"
__plugin_usage__ = """
usage:
    随机挑选2名英桀进行战斗 用户进行金币投注
    会生成对战赢的概率 根据概率获得金币倍率收益
    会扣除所得税百分之五
    指令:
    "海滨乱斗", "[参数一] [参数二]"
""".strip()
__plugin_des__ = "逐火英桀战斗模拟"
__plugin_cmd__ = ["海滨乱斗", "[参数一] [参数二]"]
__plugin_type__ = ("真寻小赌场",)
__plugin_version__ = 2.2
__plugin_author__ = "冰蓝色光点"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["海滨乱斗 选择 [] []"],
}
__plugin_count_limit__ = {
    "max_count": 100,    # 每日次数限制数量
    "limit_type": "user",   # 监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
    "rst": "每天只能进行50次投注，你没有机会了",            # 回复的话，为None时不回复，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
    "status": True          # 此限制的开关状态
}
__plugin_configs__ = {
    "FIGHT_PROCESS": {
        "value": (5, 1),
        "help": "自动撤回，参1：延迟撤回语句时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
        "default_value": (5, 1),
    },
    "FIGHT_TMP": {
        "value": (15, 1),
        "help": "自动撤回，参1：延迟撤回色图时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
        "default_value": (15, 1),
    },
}

ready = on_command("海滨乱斗",permission=GROUP, priority=5, block=True) 
@ready.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    path_fight_temp = str((IMAGE_PATH / "fight" / "temp").absolute()) + "/"
    await deltemp(path_fight_temp)
    rands1 = int(random.randint(0, 11))
    rands2 = int(random.randint(0, 11))
    while(rands1 == rands2):
        rands1 = int(random.randint(0, 11))
        rands2 = int(random.randint(0, 11))
    list_prob = []
    stats(rands1, rands2, 0, 10000, list_prob)
    list_beilv = []
    if list_prob[1] < 100:
        list_beilv.append(100.00)
    else:
        list_beilv.append(10000 / list_prob[1])
    if list_prob[3] < 100:
        list_beilv.append(100.00)
    else:
        list_beilv.append(10000 / list_prob[3])
    global msg_id_0 
    msg_id_0 = await bot.send(event, '随机到的两名英桀是\n{}  {}\n胜率分别为{:.2f}  {:.2f}\n 获胜获得金币倍率分别为{:.2f}  {:.2f}'.format(list_prob[0], list_prob[2], float(list_prob[1] /10000), float(list_prob[3] / 10000), float(list_beilv[0]), float(list_beilv[1])))

    global msg_id_1
    msg_id_1 = await bot.send(event, '请选择你的支持目标和投注金额, 0为前 1为后, 两个参数空格隔开')
    state['role_two'] = [rands1, rands2]
    state['beilv'] = list_beilv
    @ready.got('select')
    async def _(bot: Bot,                                                                   
        event: GroupMessageEvent,
        state: T_State,
        select: Message = Arg("select")

        ): 
        uid = event.user_id
        group = event.group_id
        text = get_message_text(select)
        text_split = []
        text_split = text.split()
        try:
            withdraw_message_manager.withdraw_message(
                event,
                msg_id_0["message_id"],
                Config.get_config("fight", "FIGHT_TMP"),
            )
            withdraw_message_manager.withdraw_message(
                event,
                msg_id_1["message_id"],
                Config.get_config("fight", "FIGHT_TMP"),
            )
        except:
            pass

        try:
            selRole = int (text_split[0])
            money_spend = int (text_split[1])
        except:
            await ready.finish("参数不正确,消耗掉一次机会,若开始请重新输入【海滨乱斗】")
        if selRole != 0 and selRole != 1:
            await ready.finish("参数不正确,消耗掉一次机会,若开始请重新输入【海滨乱斗】")
        gold_have = await BagUser.get_gold(uid, group)
        if gold_have < money_spend:
            await ready.finish("你的钱不够,请下次看好你有多少金币，若开始请重新输入【海滨乱斗】")
        await BagUser.spend_gold(uid, group, money_spend)
        try:
            msg_id = await bot.send(event, '以下是战斗过程')
            withdraw_message_manager.withdraw_message(
                event,
                msg_id["message_id"],
                Config.get_config("fight", "FIGHT_TMP"),
            )
        except:
            pass
        list_fight = []
        list_role = state['role_two']
        list_fight = stats(list_role[0], list_role[1], 1, 1, list_fight)
        count = list_fight[4].count
        path_fight1 = str(path_fight)
        
        msg_list = []
        image_file_role1 = f"file:///{path_fight1}/resources/{list_role[0]}.jpg" 
        image_file_role2 = f"file:///{path_fight1}/resources/{list_role[1]}.jpg"
        msg_list = await chain_reply(bot, msg_list, image_file_role1)
        msg_list = await chain_reply(bot, msg_list, image_file_role2)
        path_fight_temp = str((IMAGE_PATH / "fight" / "temp").absolute()) + "/"
        
        for i in range(count):
            image_file = f"file:///{path_fight_temp}{i}.png"
            msg_list = await chain_reply(bot, msg_list, image_file)
        try:
            msg_id = await bot.send_group_forward_msg(group_id=event.group_id, messages=msg_list)
            withdraw_message_manager.withdraw_message(
                event,
                msg_id["message_id"],
                Config.get_config("fight", "FIGHT_PROCESS"),
            )
        except:
            pass
        list_beilv = state['beilv']
        if int(selRole) == 0:
            if(list_fight[4].isDisplayVictory == 1):
                money_add = int (money_spend * list_beilv[0] * 0.95 + money_spend * 0.05)
                await BagUser.add_gold(uid, group, money_add)
                gold_have = await BagUser.get_gold(uid, group)
                await ready.finish( '你支持的英桀获胜,你获得{}金币,当前金币为{}'.format(money_add, gold_have), at_sender=True)
                    
            else:
                gold_have = await BagUser.get_gold(uid, group)
                await ready.finish( '你支持的英桀惜败,没有获得一个金币,当前金币为{}'.format(gold_have), at_sender=True)
                
        if int(selRole) == 1:
            if(list_fight[5].isDisplayVictory == 1):
                money_add = int (money_spend * list_beilv[1] * 0.95 + money_spend * 0.05)
                await BagUser.add_gold(uid, group, money_add)
                gold_have = await BagUser.get_gold(uid, group)
                await ready.finish( '你支持的英桀获胜,你获得{}金币,当前金币为{}'.format(money_add, gold_have), at_sender=True)
                
            else:
                gold_have = await BagUser.get_gold(uid, group)
                await ready.finish('你支持的英桀惜败,你没有获得一个金币,当前金币为{}'.format(gold_have), at_sender=True)
                

                    
    async def chain_reply(bot, msg_list, image):
        
        data = {
            "type": "node",
            "data": {
                "name": f"{NICKNAME}",
                "uin": f"{bot.self_id}",
                "content": [
                    {"type": "text", "data": {"text": ""}},
                    {"type": "image", "data": {"file": image}},
                ],
            },
        }
        msg_list.append(data)
        return msg_list
async def deltemp(path:str):
    try:
        shutil.rmtree(path)
    except:
        pass



                
async def chain_reply(bot, msg_list, image):
    
    data = {
        "type": "node",
        "data": {
            "name": f"{NICKNAME}",
            "uin": f"{bot.self_id}",
            "content": [
                {"type": "text", "data": {"text": ""}},
                {"type": "image", "data": {"file": image}},
            ],
        },
    }
    msg_list.append(data)
    return msg_list
async def deltemp(path:str):
    try:
        shutil.rmtree(path)
    except:
        pass
