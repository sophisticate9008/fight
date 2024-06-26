# coding=utf-8
import traceback
import asyncio
import sys
from configs.config import NICKNAME
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import (
        GroupMessageEvent,
        GROUP,
        Bot,
        Message,
        MessageSegment
)
from utils.utils import get_message_text
from nonebot.internal.params import Arg
import random
import os
import time
import shutil
from nonebot.params import CommandArg
from .fight_frame import stats
path_fight = os.path.dirname(__file__)
path_fight.replace('\\', '/')
from configs.path_config import IMAGE_PATH, FONT_PATH
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from models.bag_user import BagUser
import nonebot
from utils.manager import withdraw_message_manager
from configs.config import Config
from utils.utils import is_number
from models.group_member_info import GroupInfoUser
from utils.data_utils import init_rank
from utils.message_builder import image,custom_forward_msg
from .picture_make import *
from ._model import Fight_record
__zx_plugin_name__ = "海滨的灼热乱斗"
__plugin_usage__ = """
usage:
    海滨乱斗:
        随机挑选2名英桀进行战斗 用户进行金币应援
        会生成对战赢的概率 根据概率获得金币倍率收益
        会扣除所得税百分之五
        海滨乱斗静默:
        不再展示战斗过程,也不再撤回消息
        指令:
        "海滨乱斗?静默", "[参数一] [参数二]"
    海滨应援会:
        随机挑选两名英桀进行战斗,60s内用户可选择支持的英桀和应援金额
        奖池为所有人的应援金币 * 胜者英桀倍率 * 0.95
        奖池分配为胜利英桀的支持者所应援的金币 / 支持者所应援的金币总额 * 奖池金额
        请勿联合刷金币，没什么意思
        指令:
        "海滨应援会", "应援 [目标] [金额]"
    海滨比赛:
        每个人应援的英桀是系统随机的 
        分为二人场，四人场，八人场，十二人场
        在二人场，四人场和八人场中，随机两两对决，胜者晋级，以此类推决出决胜英桀，其支援者获得（参与者数量 + 1） * 比赛设置金额 
        在十二人场中，在初赛过后会随机挑选两名英桀进行复活，继续参与赛制
        请勿联合刷金币，没什么意思
        指令:
        "海滨比赛 [2 4 8 12] [gold]", "助威"
    我的海滨乱斗概况
        指令:
        我的海滨乱斗概况
    次数榜:
        指令:
        乱斗次数榜 ?num
    赚钱榜:
        指令:
        乱斗赚钱榜 ?num
    输钱榜:
        指令:
        乱斗输钱榜 ?num
        
""".strip()
__plugin_des__ = "逐火英桀战斗模拟"
__plugin_cmd__ = ["海滨乱斗", "[参数一] [参数二]"]
__plugin_type__ = ("真寻小赌场",)
__plugin_version__ = 4.1
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
    "rst": "每天只能进行100次调用，你没有机会了",            # 回复的话，为None时不回复，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
    "status": True          # 此限制的开关状态
}
__plugin_configs__ = {
    "FIGHT_PROCESS": {
        "value": (20, 1),
        "help": "自动撤回，参1：延迟撤回战斗过程时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
        "default_value": (30, 1),
    },
    "FIGHT_TMP": {
        "value": (5, 1),
        "help": "自动撤回，参1：延迟撤回语句时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
        "default_value": (10, 1),
    },
    "FIGHT_RELAX": {
        "value": 20,
        "help": "战斗休息时间",
        "default_value": 20,
    },
    "FIGHT_YINGYUAN": {
        "value": 60,
        "help": "应援时间",
        "default_value": 60,
    },
    "FIGHT_COMPETE": {
        "value": 300,
        "help": "助威时间",
        "default_value": 300,
    },    
    "FIGHT_PICTURE": {
        "value": 1,
        "help": "0为q版, 1正常",
        "default_value": 1,
    },
}

fight_single = {}

players_support = {}

players_compete = {}

fight_num = 500

ready = on_command("海滨乱斗",permission=GROUP, priority=5, block=True)
fight_multi = on_command("海滨应援会", permission=GROUP, priority=5, block=True)
join_support = on_command("应援",permission=GROUP, priority=5, block=True)
fight_compete = on_command("海滨比赛", permission=GROUP, priority=5, block=True)
join_compete = on_command("助威", permission=GROUP, priority=5, block=True)
fight_sort = on_command("乱斗", permission=GROUP, priority=5, block=True)
fight_my = on_command("我的海滨乱斗概况", permission=GROUP, priority=5, block=True)


@ready.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            args: Message = CommandArg(),
            ):
    
    global fight_single
    msg = args.extract_plain_text().strip()
    
    uid = event.user_id
    group = event.group_id
    try:
        if fight_single[group]:
            pass
        else:
            fight_single[group] = {}
    except:
        fight_single[group] = {}
    fight_single[group][uid] = {}
    if msg == '静默':
        fight_single[group][uid]['silence'] = 1
    else:
        fight_single[group][uid]['silence'] = 0

    rands1 = int(random.randint(0, 11))
    rands2 = int(random.randint(0, 11))
    while(rands1 == rands2):
        rands1 = int(random.randint(0, 11))
        rands2 = int(random.randint(0, 11))
    list_prob = []
    
    stats(rands1, rands2, 0, fight_num, list_prob)
    
    list_beilv = []
    
    if list_prob[1] < fight_num / 100:
        list_beilv.append(100.00)
    else:
        list_beilv.append(fight_num / list_prob[1])
    if list_prob[3] < fight_num / 100:
        list_beilv.append(100.00)
    else:
        list_beilv.append(fight_num / list_prob[3])
        
    fight_single[group][uid]['list_beilv'] = list_beilv
     
    msg_id_0 = await bot.send(event, '随机到的两名英桀是\n{}  {}\n胜率分别为{:.2f}  {:.2f}\n 获胜获得金币乘数分别为{:.2f}  {:.2f}\n请选择支持目标和应援金, 0为前 1为后, 两个参数空格隔开'.format(list_prob[0], list_prob[2], float(list_prob[1] /fight_num), float(list_prob[3] / fight_num), float(list_beilv[0]), float(list_beilv[1])))
    fight_single[group][uid]['msg_id_0'] = msg_id_0
    fight_single[group][uid]['role_two'] = [rands1, rands2]


@ready.got('select')
async def _(bot: Bot,                                                                   
    event: GroupMessageEvent,
    select: Message = Arg("select")
    ): 

    uid = event.user_id
    group = event.group_id
    text = get_message_text(select)
    text_split = []
    text_split = text.split()
    if fight_single[group][uid]['silence'] == 0:    
        try:
            withdraw_message_manager.withdraw_message(
                event,
                fight_single[group][uid]['msg_id_0']["message_id"],
                Config.get_config("fight", "FIGHT_TMP"),
            )
        except:
            pass
    try:
        selRole = int (text_split[0])
        money_spend = int (text_split[1])
    except:
        fight_single[group][uid] = {}
        await ready.finish("参数不正确,消耗掉一次机会,若开始请重新输入【海滨乱斗】")
    if selRole != 0 and selRole != 1:
        fight_single[group][uid] = {}
        await ready.finish("参数不正确,消耗掉一次机会,若开始请重新输入【海滨乱斗】")
    gold_have = await BagUser.get_gold(uid, group)
    if gold_have < money_spend or money_spend < 0:
        fight_single[group][uid] = {}
        await ready.finish("你的金币不够或为负数,请下次看好你有多少金币并输入正数")
    await BagUser.spend_gold(uid, group, money_spend)
    list_fight = []
    list_role = fight_single[group][uid]['role_two']
    list_fight = stats(list_role[0], list_role[1], 1, 1, list_fight)
    path_fight1 = str(path_fight)
    txtss = list_fight[5]
    msg_list = []
    if fight_single[group][uid]['silence'] == 0:
        image_file_role1 = f"file:///{path_fight1}/resources/{list_role[0]}.jpg" 
        image_file_role2 = f"file:///{path_fight1}/resources/{list_role[1]}.jpg"
        msg_list.append(MessageSegment.image(image_file_role1))
        msg_list.append(MessageSegment.image(image_file_role2))
        for txts in txtss:
            msg_list.append(image(b64=pic2b64(image_add_text(txts))))
        try:
            msg_id = await bot.send_group_forward_msg(group_id=event.group_id, messages=custom_forward_msg(msg_list, bot.self_id))
            withdraw_message_manager.withdraw_message(
                event,
                msg_id["message_id"],
                Config.get_config("fight", "FIGHT_PROCESS"),
            )
        except:
            pass
    list_beilv = fight_single[group][uid]['list_beilv']
    fight_single[group][uid] = {}
    if int(selRole) == list_fight[4]:
        money_add = int (money_spend * list_beilv[int(selRole)] * 0.95 + money_spend * 0.05)
        await BagUser.add_gold(uid, group, money_add)
        await Fight_record.record(group, uid, money_add - money_spend, 1)
        gold_have = await BagUser.get_gold(uid, group)
        await ready.finish( '你支持的英桀获胜,你获得{}金币,当前金币为{}'.format(money_add, gold_have), at_sender=True)
    else:
        await Fight_record.record(group, uid, money_spend, 0)
        gold_have = await BagUser.get_gold(uid, group)
        await ready.finish( '你支持的英桀惜败,没有获得一个金币,当前金币为{}'.format(gold_have), at_sender=True)







@fight_multi.handle()
async def _(
    bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()
):
    global players_support

    time_yingyuan = float(Config.get_config("fight", "FIGHT_YINGYUAN"))
    group = event.group_id
    try:
        
        try:
            if players_support[group][0]:
                await fight_multi.finish('已经有应援会在进行了,请直接应援')
        except KeyError:
            pass
        
        #随机部分

        rands1 = int(random.randint(0, 11))
        rands2 = int(random.randint(0, 11))
        while(rands1 == rands2):
            rands1 = int(random.randint(0, 11))
            rands2 = int(random.randint(0, 11))
        list_prob = []
        stats(rands1, rands2, 0, fight_num, list_prob)
        list_beilv = []
        if list_prob[1] < fight_num / 100:
            list_beilv.append(100.00)
        else:
            list_beilv.append(fight_num / list_prob[1])
        if list_prob[3] < fight_num / 100:
            list_beilv.append(100.00)
        else:
            list_beilv.append(fight_num / list_prob[3])
        await bot.send(event, '随机到的两名英桀是{}  {}\n将不再显示概率\n请发送 应援 [0 or 1] [money]'.format(list_prob[0], list_prob[2]))
        
        #等待部分
        list_role = [rands1, rands2]
        players_support[group] = {}
        players_support[group][0] = {}
        players_support[group]['time'] = time.time()
        players_support[group][0]['multi_number'] = 0
        players_support[group][0]['uid_list'] = []
        await asyncio.sleep(time_yingyuan)#时间修改
        dict_all = {}
        #清单发送
        for i in range(1, len(players_support[group]) - 1):
            dict_all[i] = {}
            dict_all[i]["name"] = players_support[group][i]["name"]
            role_sup = players_support[group][i]["support"]
            role_num = list_role[role_sup]
            dict_all[i]["support"] = await int_to_name(role_num)
            dict_all[i]["money"] = players_support[group][i]["money"]
        img_yingyuandan = image_add_name(dict_all,  list_role)
        msg_tuple = ()
        await bot.send(event, '应援时间已过,开始战斗\n以下是应援清单')
        msg_tuple = ('', image(b64=pic2b64(img_yingyuandan)))
        await fight_multi.send(Message(msg_tuple))
        msg_tuple = ()
        
        #战斗主体
        list_return = []
        list_return = await begin_fight(list_role, bot, list_return)
        await bot.send_group_forward_msg(group_id=group, messages=custom_forward_msg(list_return[0], bot.self_id))
        money_sum = 0
        money_sum_vic = 0
        #奖池计算
        for i in range(1, len(players_support[group]) - 1):
            money_sum += players_support[group][i]["money"]
            
        money_pool = list_beilv[list_return[1]] * money_sum * 0.95
        list_vic = []
        #胜者统计
        for i in range(1, len(players_support[group]) - 1):
            if players_support[group][i]["support"] == list_return[1]:
                money_sum_vic += players_support[group][i]["money"]
                list_vic.append(i)
        kwarg_award = {}
        #奖池分配
        for i in list_vic:
            money_add = int (players_support[group][i]["money"] / money_sum_vic * money_pool)
            kwarg_award[i] = {}
            kwarg_award[i]["name"] = players_support[group][i]["name"]
            kwarg_award[i]["money"] = money_add
            await BagUser.add_gold(players_support[group][i]["uid"], group, money_add)
        role_win = await int_to_name(list_role[list_return[1]])
        img_pool_divide = image_win( kwarg_award, role_win)
        

        await bot.send(event, f"战斗结束，获胜者为{list_return[2].name}\n奖池金额为({int(money_pool)})\n分配情况如下")
        msg_tuple = ("", image(b64=pic2b64(img_pool_divide)))
        await fight_multi.send(Message(msg_tuple))

        players_support[group] = {}

    except KeyError as e:
        # 捕获 KeyError 并输出具体的错误信息
        traceback.print_exc()  # 打印堆栈信息，包括文件名和行号
        print(f"KeyError occurred at line {traceback.extract_tb(e.__traceback__)[0].lineno}")
        players_support[group] = {}
        await fight_multi.finish('键错误,强行初始化')
    except:
        traceback.print_exc()  # 打印堆栈信息，包括文件名和行号
        print(f"KeyError occurred at line {traceback.extract_tb(e.__traceback__)[0].lineno}")
        players_support[group] = {}
        await fight_multi.finish('未知错误,强行初始化')
    
    
@join_support.handle()
async def _(
    bot: Bot, event: GroupMessageEvent, state: T_State, arg: Message = CommandArg()
):
    global players_support
    time_yingyuan = float(Config.get_config("fight", "FIGHT_YINGYUAN"))
    uid = event.user_id
    group = event.group_id
    msg = arg.extract_plain_text().strip()
    msg = msg.split()
    if len(msg) == 2:
        msg_sup = msg[0]
        msg_money = msg[1]
        gold_have = await BagUser.get_gold(uid, group)
        try:
            if time.time() - players_support[group]['time'] < time_yingyuan:
                if is_number(msg_sup) and is_number(msg_money):
                    if int(msg_sup) == 0 or int(msg_sup) == 1:
                        if int(msg_money) >= 0 and int(msg_money) <= gold_have:
                            if uid not in players_support[group][0]['uid_list']:
                                players_support[group][0]['uid_list'].append(uid)
                                players_support[group][0]['multi_number'] += 1
                                multi_number = players_support[group][0]['multi_number']
                                players_support[group][multi_number] = {}
                                players_support[group][multi_number]["uid"] = uid
                                players_support[group][multi_number]["support"] = int(msg_sup)
                                players_support[group][multi_number]["money"] = int(msg_money)
                                await BagUser.spend_gold(uid, group, int(msg_money))
                                if user := await GroupInfoUser.get_or_none(user_qq=uid, group_id=group):
                                    user_name = user.user_name
                                else:
                                    user_name = str(uid)
                                players_support[group][multi_number]["name"] = user_name                                
                            else:
                                await join_support.finish("铁咩,只能投一次啊喂",at_sender=True)                            
        except KeyError:
            players_support[group][0]['uid_list'] = []
            await join_support.finish("没有应援会在进行哦")


#战斗函数加合并消息函数
async def begin_fight(list_role, bot, list_return) :
    list_fight = []
    msg_list = []
    list_fight = stats(list_role[0], list_role[1], 1, 1, list_fight)
    path_fight1 = str(path_fight)
    txtss = list_fight[5]
    image_file_role1 = f"file:///{path_fight1}/resources/{list_role[0]}.jpg" 
    image_file_role2 = f"file:///{path_fight1}/resources/{list_role[1]}.jpg"    
    msg_list = []
    msg_list.append(MessageSegment.image(image_file_role1))
    msg_list.append(MessageSegment.image(image_file_role2))
    for txt in txtss:
        msg_list.append(image(b64=pic2b64(image_add_text(txt))))
        
    vic_role = list_fight[4]
    list_return.append(msg_list)
    list_return.append(vic_role)
    if vic_role == 0:
        list_return.append(list_fight[6])
        list_return.append(list_fight[7])
    else :
        list_return.append(list_fight[7])
        list_return.append(list_fight[6])
    return list_return
            
async def int_to_name(number):
    list_role = ['凯文', "爱莉希雅", "格蕾修", "樱", "阿波尼亚", "华", "维尔薇", "科斯魔", "梅比乌斯", "千劫", "帕朵菲莉丝", "伊甸"]
    name = list_role[number]
    return name    
        
@fight_compete.handle()
async def _(
    bot: Bot, event: GroupMessageEvent, state: T_State, arg: Message = CommandArg()
):  
    global players_compete
    
    list_win = []
    list_lost = []
    
    time_compete = float(Config.get_config("fight", "FIGHT_COMPETE"))
    time_relax = int(Config.get_config("fight", "FIGHT_RELAX"))
    uid = event.user_id
    group = event.group_id
    msg = arg.extract_plain_text().strip()
    msg = msg.split()
    try:
        try:        
            if players_compete[group][0]:
                await fight_compete.finish("已经有比赛在进行了，请直接参与")
        except KeyError:
            pass
        if len(msg) == 2:
            mode_compete = msg[0]
            cost_compete = msg[1]

            if is_number(mode_compete) and is_number(cost_compete):
                mode_com = int(mode_compete)
                cost_com = int(cost_compete)
                if mode_com == 2 or mode_com == 4 or mode_com == 8 or mode_com == 12:
                    list_mode_cost = []
                    list_mode_cost.append(mode_com)
                    list_mode_cost.append(cost_com)
                    
                    players_compete[group] = {}
                    players_compete[group][0] = {}
                    players_compete[group][0]['time'] = time.time()
                    players_compete[group][0]['uid_list_compete'] = []
                    players_compete[group][0]['list_mode_cost'] = list_mode_cost
                    players_compete[group][0]['com_number'] = 0
                    
                    
                    await bot.send(event,'开始，请输入 [助威] 参与')
                else:
                    await fight_compete.finish("不正确,未能开始")
            else:
                await fight_compete.finish("不正确,未能开始")
        else:
            await fight_compete.finish("不正确,未能开始")

        time_compete_tmp = int(time_compete)
        for i in range(time_compete_tmp):
            if run_now(players_compete, list_mode_cost[0] , group):
                break
            else:
                await asyncio.sleep(1)
        
        if len (players_compete[group]) - 1 != mode_com:
            
            players_compete[group] = {}
            list_mode_cost = []
            await fight_compete.finish('人数不够,比赛取消')
        count_com = mode_com
        role_sel = random.sample(range(12), mode_com)
        for i in range(mode_com):
            players_compete[group][i + 1]["support"] = role_sel[i]
            list_win.append(role_sel[i])
        txts = {}
        for i in range(mode_com):
            txts[i + 1] = {}
            txts[i + 1]['support'] = players_compete[group][i + 1]["support"]
            txts[i + 1]['name'] = players_compete[group][i + 1]['name']
        compete = image_compete(txts, mode_com)
        msg_tuple = (f"人已满,助威表单如下,{time_relax}s后开始战斗", image(b64=pic2b64(compete)))
        
        await fight_compete.send(Message(msg_tuple))
        await asyncio.sleep(time_relax)
        
        while (count_com % 2 == 0):
            list_mess = []
            if int(count_com) == 6:
                relive = random.sample(list_lost, 2)
                list_win.append(relive[0])
                list_win.append(relive[1])
                count_com += 2
                name_tmp1 = await int_to_name(relive[0])
                name_tmp2 = await int_to_name(relive[1])
                msg_id = await bot.send(event,f'获得复活赛资格的英桀为{name_tmp1}, {name_tmp2}')
                try:
                    withdraw_message_manager.withdraw_message(
                        event,
                        msg_id["message_id"],
                        Config.get_config("fight", "FIGHT_TMP"),
                    )
                except:
                    pass
            list_mess = random.sample(list_win, int (count_com))
            list_win = []
            index_tmp = 0
            while(index_tmp < int (count_com)):
                list_return = []
                list_role = []
                list_role.append(list_mess[index_tmp])
                list_role.append(list_mess[index_tmp + 1])
                await begin_fight(list_role, bot, list_return)
                name_l = await int_to_name(list_role[0])
                name_r = await int_to_name(list_role[1])
                msg_id = await bot.send(event, f'现在是{name_l}和{name_r}的战斗')
                try:
                    withdraw_message_manager.withdraw_message(
                        event,
                        msg_id["message_id"],
                        Config.get_config("fight", "FIGHT_TMP"),
                    )
                except:
                    pass            
                msg_id = await bot.send_group_forward_msg(group_id=group, messages=custom_forward_msg(list_return[0], bot.self_id))
                try:
                    withdraw_message_manager.withdraw_message(
                        event,
                        msg_id["message_id"],
                        Config.get_config("fight", "FIGHT_PROCESS"),
                    )
                except:
                    pass              
                list_win.append(list_return[2].id)
                list_lost.append(list_return[3].id)
                index_tmp += 2
                if count_com > 2:
                    await asyncio.sleep(time_relax)
                else:
                    pass
            if len(list_win) > 1:
                list_win_name = []
                for i in list_win:
                    list_win_name.append(await int_to_name(i))
                
                msg_id = await bot.send(event, f'晋级的英桀为{list_win_name}\n{time_relax}s后继续战斗')
                try:
                    withdraw_message_manager.withdraw_message(
                        event,
                        msg_id["message_id"],
                        Config.get_config("fight", "FIGHT_TMP"),
                    )
                except:
                    pass              
                
                await asyncio.sleep(time_relax)#时间修改
            if len(list_win) == 1:
                win_player = 0
                win_name = await int_to_name(list_win[0])
                for i in range(mode_com):
                    await BagUser.spend_gold(players_compete[group][i + 1]["uid"], group, list_mode_cost[1])
                    if players_compete[group][i + 1]['support'] == list_win[0]:
                        win_player = i + 1
                await BagUser.add_gold(players_compete[group][win_player]['uid'], group, list_mode_cost[1] * (list_mode_cost[0] + 1))
                #初始化
                win_name_player = players_compete[group][win_player]['name']
                await bot.send(event, f'{win_name}取得了最终胜利\n{win_name_player}因此获得了{cost_com * mode_com + cost_com}金币')
                players_compete[group] = {}
            count_com = int(count_com / 2)
    except KeyError:
        players_compete[group] = {}
        await fight_compete.finish('键错误,强行初始化')            
    
@join_compete.handle()
async def _(
    bot: Bot, event: GroupMessageEvent, state: T_State, arg: Message = CommandArg()
):
    global players_compete
    time_compete = float(Config.get_config("fight", "FIGHT_COMPETE"))
    uid = event.user_id
    group = event.group_id
    try: 
        gold_have = await BagUser.get_gold(uid, group)
        try:
            if time.time() - players_compete[group][0]["time"] < time_compete:
                
                if uid not in players_compete[group][0]['uid_list_compete']:
                    list_mode_cost = players_compete[group][0]['list_mode_cost']
                    if len(players_compete[group][0]['uid_list_compete']) < list_mode_cost[0]:
                        if gold_have > list_mode_cost[1]:
                            players_compete[group][0]['uid_list_compete'].append(uid)
                            players_compete[group][0]['com_number'] += 1
                            com_number = players_compete[group][0]['com_number']
                            players_compete[group][com_number] = {}
                            if user := await GroupInfoUser.get_or_none(user_qq=uid, group_id=group):
                                user_name = user.user_name
                            else:
                                user_name = str(uid)
                            players_compete[group][com_number]['name'] = user_name
                            players_compete[group][com_number]['uid'] = uid                            
                        else:
                            await join_compete.finish("金币不够", at_sender = True)
                    else:
                        await join_compete.finish("人满了", at_sender = True)
                else:
                    await join_compete.finish("已经参与了", at_sender = True)        
        except KeyError:
            await join_compete.finish("比赛未开启") 
    except KeyError:

        players_compete[group] = {}

       
        await join_compete.finish("键错误,强行初始化")        


def run_now(players_compete:dict, mode_com, group:int):
    if len(players_compete[group]) - 1 == mode_com:
        return True
    else:
        return False

@fight_my.handle()
async def _(
    bot: Bot, event: GroupMessageEvent, state: T_State, arg: Message = CommandArg()
):
    global players_compete
    uid = event.user_id
    group = event.group_id
    list_my = await Fight_record.my(group, uid)
    if list_my == 0:
        await fight_my.finish('你还没有参加过海滨乱斗', at_sender = True)
    else:
        msg = '你一共参加了{}次海滨乱斗,曾赢过{}金币, 共输掉{}金币'.format(list_my[0], list_my[1], list_my[2])
        await fight_my.finish(msg, at_sender = True)

@fight_sort.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    msg_ = msg.split()
    type_ = msg_[0]
    try:    
        num = msg_[1]
        if is_number(num) and 51 > int(num) > 10:
            num = int(num)
        else:
            num = 10        
    except:
        num = 10
    
    all_users = await Fight_record.get_all_users(event.group_id)
    all_user_id = [user.uid for user in all_users]
    if type_ == '次数榜':
        
        all_user_data = [int(user.fight_count) for user in all_users]
        rank_image = await init_rank("乱斗次数榜", all_user_id, all_user_data, event.group_id, num)
        if rank_image:
            await fight_sort.finish(image(b64=rank_image.pic2bs4()))
    if type_ == '赚钱榜':
        all_user_data = [int(user.gain) for user in all_users]
        rank_image = await init_rank("乱斗赚钱榜", all_user_id, all_user_data, event.group_id, num)
        if rank_image:
            await fight_sort.finish(image(b64=rank_image.pic2bs4()))        
    
    if type_ == '输钱榜':
        all_user_data = [int(user.loss) for user in all_users]
        rank_image = await init_rank("乱斗输钱榜", all_user_id, all_user_data, event.group_id, num)
        if rank_image:
            await fight_sort.finish(image(b64=rank_image.pic2bs4()))       
