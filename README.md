#
崩坏三十二英桀战斗模拟
适配真寻bot的插件


第一次写
完全是看代码猜nonebot框架意思 
真寻启动一次修改一句  
重启了不下50次  
有影响战果的战斗逻辑错误请发截图
没那么高的技术  
输错参数就得重新输入海滨乱斗  
似乎得初始化那么一次  
抢着发可能会吞钱
#
2022/7/28

修复金币结算  

金币结算添加艾特 避免混淆  

修复除0bug  

修复金币倍率固定bug  

#
2022/7/29  

添加梅比乌斯被动触发文案  

修复樱在获得撕裂状态后再次受到撕裂状态且被闪避后清除已有撕裂状态的问题  

发现开始和投注都会消耗使用次数  

所以各位改每日限制的时候改成偶数并且将提示语的次数除以2
#
2022/7/30

仔细想想没修复上述樱问题，今天才改对。  

修复格蕾修炸盾后造成一方生命值为0的判定问题  

修复【混乱】攻击返还自身造成自身生命值为零，但没有结束回合，且判定胜负延迟或未判定的问题

修复科斯魔对战任何人胜率为0的问题(伤害计算写到显示控制里了）
