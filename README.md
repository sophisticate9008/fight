#
崩坏三十二英桀自由组合战斗模拟
适配真寻bot的插件
第一次写
完全是看代码猜nonebot框架意思 
真寻启动一次修改一句  
重启了不下50次  
有影响战果的战斗逻辑错误请发截图
没那么高的技术  
输错参数就得重新输入海滨乱斗  
似乎得初始化那么一次
#
投注默认为50次

需要修改请到真寻目录/data/configs/plugins2count.yaml修改 实际使用次数为max_count / 2
#
2022/8/11
修复初始化问题（感谢yuan488

修复比赛奖金实际未到账(仅修改一个变量，可以根据修改历史修改)

修复奖金倍率固定为五的问题，可以根据修改历史修改

#
2022/8/10

新增海滨比赛功能

配置文件configs.yaml有新参数注意查看
#
2022/8/9

少了一张12.png已补
#
2022/8/8

考虑到手机用户在人数较少的时候列表不能一目了然，应援单列表将附着在英桀q版图片下方单独发送

分配列表附着英桀图片下方，想加图请直接塞到resources/{名字}中，不用修改名字，不想要图的也可以删掉相应目录中的图片，分配列表将以原始形态发送
#
2022/8/7

增加没有应援会在进行的提示
修复没有应援会进行的时候进行应援会导致key错误而造成阻塞
修复两个都投导致可以刷钱的规则漏洞
增加应援结束后的应援清单
分配也将以图片形式显示
#
2022/8/6

新增海滨后援会功能
详情查看__init__.py

#
2022/8/3

添加语言撤回 可以从config.yaml修改时间
#
2022/7/30

昨日并没有修复樱问题，今日才修复 

修复格蕾修炸盾后造成一方生命值为0的判定问题  

修复【混乱】攻击返还自身造成自身生命值为零，但没有结束回合，且判定胜负延迟或未判定的问题

修复科斯魔对战任何人胜率为0的问题(伤害计算写到显示控制里了）

最大倍率改为100，倍率和胜率【显示】为小数点后两位

修复倍率不符问题

修改抽点为收益抽点

修复炸盾和混乱致死不显示的问题
#
2022/7/29  

添加梅比乌斯被动触发文案  

修复樱在获得撕裂状态后再次受到撕裂状态且被闪避后清除已有撕裂状态的问题  

发现开始和投注都会消耗使用次数  

所以各位改每日限制的时候改成偶数并且将提示语的次数除以2
#
2022/7/28

修复金币结算  

金币结算添加艾特 避免混淆  

修复除0bug  

修复金币倍率固定bug  

