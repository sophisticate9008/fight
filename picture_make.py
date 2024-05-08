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


import base64
from io import BytesIO
import random
from PIL import Image, ImageDraw, ImageFont
from configs.path_config import IMAGE_PATH, FONT_PATH
import os
from configs.config import Config


def image_add_text(txts:list,  text_color=(255, 0, 0), text_size=13):
    
    img_back = Image.new("RGB",(510, (len(txts) * 14)),(255,255,255))
    fight_dir = IMAGE_PATH / "fight"
    fight_dir.mkdir(exist_ok=True, parents=True)
    fight_ttf = str(FONT_PATH / "yuanshen.ttf")


    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img_back)
    # 字体的格式 这里的SimHei.ttf需要有这个字体
    fontStyle = ImageFont.truetype(fight_ttf, text_size, encoding="utf-8")
    # 绘制文本
    j = -1
    for i in txts:
        j = j + 1
        draw.text((0, j * 14), i, text_color, font=fontStyle)
        
    return img_back

def image_add_name(txts:dict, list_role: list, text_color=(0, 0, 0)):
    pic_arg = int(Config.get_config("fight", "FIGHT_PICTURE"))
    if pic_arg == 0:
        pic_style = '.png'
        
        img_length = 401
        img_width = 600  
        text_size = 26      
    if pic_arg == 1:
        pic_style = '.jpg'
        img_length = 900
        img_width = 1080
        text_size = 60
    path_fight = os.path.dirname(__file__)
    path_fight_res = str(path_fight) + "/resources/"    
    img_back = Image.new("RGB",(img_length * 2, (len(txts) * (text_size + 2)) + img_width),(255,255,255))
    left = path_fight_res + str(list_role[0] + 12) + pic_style
    right = path_fight_res + str(list_role[1] + 12) + pic_style
    left_f = Image.open(left)
    right_f = Image.open(right)
    fight_dir = IMAGE_PATH / "fight"
    fight_dir.mkdir(exist_ok=True, parents=True)
    temp = fight_dir / "temp"
    temp.mkdir(exist_ok=True, parents=True)
    img_back.paste(left_f, (0, 0))
    img_back.paste(right_f, (img_length, 0))
    fight_ttf = str(FONT_PATH / "yuanshen.ttf")

    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img_back)
    
    # 字体的格式 这里的SimHei.ttf需要有这个字体
    fontStyle = ImageFont.truetype(fight_ttf, text_size, encoding="utf-8")
    # 绘制文本
    j = -1
    for i in txts:
        j = j + 1
        draw.text((0, (text_size + 2) * j + img_width), txts[i]["name"], (0, 0, 0), font=fontStyle)
        draw.text((img_length * 2 - text_size * 12, (text_size + 2) * j + img_width), txts[i]["support"], (208, 122, 255), font=fontStyle)
        draw.text((img_length * 2 - text_size * 4, (text_size + 2) * j + img_width), str(txts[i]["money"]), (255, 187, 0), font=fontStyle)
    return img_back

def image_win(txts:dict, role_win:str):
    path_fight = os.path.dirname(__file__)
    path_fight_res = str(path_fight) + "/resources/"  
    fight_ttf = str(FONT_PATH / "yuanshen.ttf")   
    win_image = path_fight_res + role_win + '/'
    fight_dir = IMAGE_PATH / "fight"
    fight_dir.mkdir(exist_ok=True, parents=True)
    temp = fight_dir / "temp"
    temp.mkdir(exist_ok=True, parents=True)
     
    files= os.listdir(win_image)
    img_l = 802
    img_w = 1
    if len(files) - 1 >= 0 :
        index_rand = random.randint(0, len(files) - 1)
        img = Image.open(win_image + files[index_rand])
        img_l = img.size[0]
        img_w = img.size[1]
    text_size = int (img_l / 30)
    img_back = Image.new('RGB',(img_l, (len(txts) * (text_size + 2)) + img_w), (255,255,255))
    if len(files) - 1 >= 0 :
        img_back.paste(img, (0, 0))
    draw = ImageDraw.Draw(img_back)
    
    fontStyle = ImageFont.truetype(fight_ttf, text_size, encoding="utf-8")
    j = -1
    for i in txts:
        j = j + 1
        draw.text((0, (text_size + 2) * j + img_w), txts[i]["name"], (0, 0, 0), font=fontStyle)
        draw.text((img_l - text_size * 4, (text_size + 2) * j + img_w), str(txts[i]["money"]), (255, 187, 0), font=fontStyle)
    img_back.save(temp / '{}.jpg'.format("pool_divide"))
    return img_back
    

def image_compete(txts:dict, mode:int):
    pic_arg = int(Config.get_config("fight", "FIGHT_PICTURE"))
    if pic_arg == 0:
        pic_style = '.png'
        img_length = 401
        img_width = 600
        text_size = 31
    if pic_arg == 1:
        pic_style = '.jpg'    
        img_length = 900
        img_width = 1080
        text_size = 71    
    
    m = 0
    n = 0
    if mode == 2:
        m = 2
        n = 1
    if mode == 4:
        m = 2
        n = 2
    if mode == 8:
        m = 4
        n = 2
    if mode == 12:
        m = 4
        n = 3
    path_fight = os.path.dirname(__file__)
    path_fight_res = str(path_fight) + "/resources/"
    fight_dir = IMAGE_PATH / "fight"
    fight_dir.mkdir(exist_ok=True, parents=True)
    temp = fight_dir / "temp"
    temp.mkdir(exist_ok=True, parents=True)
    fight_ttf = str(FONT_PATH / "yuanshen.ttf")
    fontStyle = ImageFont.truetype(fight_ttf, text_size, encoding="utf-8")  
    img_back = Image.new('RGB',(m * (img_length), n * (img_width + text_size + 4)), (255,255,255))
    draw = ImageDraw.Draw(img_back) 
    rows = 0
    columns = 0
    for i in txts:
        print(i)
        if (columns) % m == 0 and columns != 0:
            rows += 1
            columns = 0
        support = txts[i]["support"]
        img_role = path_fight_res + str(support + 12) + pic_style
        img = Image.open(img_role)
        img_back.paste(img, (columns * img_length, rows * (img_width + text_size + 4)))
        del img
        draw.text((columns * img_length, (rows + 1) * img_width + 2 + rows * (text_size + 4)), txts[i]["name"], (0, 0, 0), font=fontStyle)
        columns += 1
        
    return img_back

def pic2b64(pic: Image) -> str:
    """
    说明:
        PIL图片转base64
    参数:
        :param pic: 通过PIL打开的图片文件
    """
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return "base64://" + base64_str