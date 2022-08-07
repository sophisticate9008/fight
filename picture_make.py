# # -*- coding: utf-8 -*-
# #先导入所需的包
# from PIL import ImageFont, Image, ImageDraw

# #导入本地字体路径及设置字体大小
# font = ImageFont.truetype("D:/5.app/vs/python/fight/fonts/yuanshen.ttf",13)
# #打开本地所需图片
# imageFile = "D:/5.app/vs/python/fight/hei.png"
# im1=Image.open(imageFile)

# # 在图片上添加文字 
# draw = ImageDraw.Draw(im1)
# draw.text((0, 0),"你好啊!",(255,255,0),font=font)
# draw = ImageDraw.Draw(im1)

# im1.save("result.png")
# from PIL import Image,ImageFont,ImageDraw
# import os
# from PIL import Image,ImageFont,ImageDraw
# import pandas as pd

# # text=str(pd.read_csv(r'D:/output.csv',encoding='gbk'))
# text = u"这是一段测试文本，test 123。"
# im = Image.new("RGB", (300, 50), (255, 255, 255))
# dr = ImageDraw.Draw(im)
# font = ImageFont.truetype(os.path.join("fonts", "yuanshen"), 14)
# dr.text((10, 5), text, font=font, fill="#000000")
# im.show()
# im.save(r'D:/output.png')
from PIL import Image, ImageDraw, ImageFont
from configs.path_config import IMAGE_PATH, FONT_PATH
import os
def image_add_text(count ,txts:list,  text_color=(255, 0, 0), text_size=13):
    img_back = Image.new("RGB",(510, (len(txts) * 14)),(255,255,255))
    fight_dir = IMAGE_PATH / "fight"
    fight_dir.mkdir(exist_ok=True, parents=True)
    temp = fight_dir / "temp"
    temp.mkdir(exist_ok=True, parents=True)
    img_back.save(fight_dir / 'back.png')
    fight_ttf = str(FONT_PATH / "yuanshen.ttf")
    del img_back
    img_path = fight_dir / 'back.png'
    img = Image.open(img_path)
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    
    # 字体的格式 这里的SimHei.ttf需要有这个字体
    fontStyle = ImageFont.truetype(fight_ttf, text_size, encoding="utf-8")
    # 绘制文本
    j = -1
    for i in txts:
        j = j + 1
        draw.text((0, j * 14), i, text_color, font=fontStyle)
    img.save(temp / '{}.png'.format(count - 1))
    del img
    return count

def image_add_name(name:str, txts:dict,  type:int ,text_color=(0, 0, 0), text_size=12):
    img_back = Image.new("RGB",(320, (len(txts) * 14) + 1),(255,255,255))
    fight_dir = IMAGE_PATH / "fight"
    fight_dir.mkdir(exist_ok=True, parents=True)
    temp = fight_dir / "temp"
    temp.mkdir(exist_ok=True, parents=True)
    img_back.save(fight_dir / 'back1.png')
    fight_ttf = str(FONT_PATH / "yuanshen.ttf")
    del img_back
    img_path = fight_dir / 'back1.png'
    img = Image.open(img_path)
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)

    # 字体的格式 这里的SimHei.ttf需要有这个字体

        
    fontStyle = ImageFont.truetype(fight_ttf, text_size, encoding="utf-8")
    # 绘制文本
    j = -1
    for i in txts:
        j = j + 1
        if type == 3:
            draw.text((0, j * 14), txts[i]["name"], text_color, font=fontStyle)
            draw.text((160, j * 14), txts[i]["support"], (208, 122, 255), font=fontStyle)
            draw.text((274, j * 14), str(txts[i]["money"]), (255, 224, 0), font=fontStyle)
        if type == 2:
            draw.text((0, j * 14), txts[i]["name"], text_color, font=fontStyle)

            draw.text((274, j * 14), str(txts[i]["money"]), (255, 224, 0), font=fontStyle)            
    img.save(temp / '{}.png'.format(name))
    del img
    return 0
    





