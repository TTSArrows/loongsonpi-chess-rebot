# Author : WuYizhi
# CreatDate : 11.3
# ******************************************************************************************************************
# chesses = [ ['rju',0,0] , ...]        坐标以左下角为原点，横坐标为第一坐标，纵坐标为第二坐标
# img0 = GetChessBoard()                获取空棋盘
# img = PutChess(img0, chesses)         将chesses放到空棋盘上
# chesses = LoadSituation(situation)    加载预设棋局，situation = 'init','xxx' , ...
# bool Move(chesses, now, next)         将坐标为now的棋子移动到坐标next，支持移动和吃子，当原棋子不存在或试图吃友方棋子时返回False
#******************************************************************************************************************
# LastUpdate : 11.15

import cv2
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

grid_width=80
grid_height=80

def cv2ImgAddText(img, text, left, top, textColor=(0, 0, 0), textSize=20):
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype("simsun.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

def GetChessBoard():
    img=np.ones((grid_height*11,grid_width*10,3)).astype('uint8')
    img*=255

    img[grid_height*1-1,grid_width:9*grid_width,:]=0
    img[grid_height*1-0,grid_width:9*grid_width,:]=0
    img[grid_height*1+1,grid_width:9*grid_width,:]=0

    for i in range(2,5):
        img[grid_height*i,grid_width:9*grid_width,:]=0

    for i in range(5,7):
        img[grid_height*i-1,grid_width:9*grid_width,:]=0
        img[grid_height*i-0,grid_width:9*grid_width,:]=0
        img[grid_height*i+1,grid_width:9*grid_width,:]=0

    for i in range(7,10):
        img[grid_height*i,grid_width:9*grid_width,:]=0

    img[grid_height*10-1,grid_width:9*grid_width,:]=0
    img[grid_height*10-0,grid_width:9*grid_width,:]=0
    img[grid_height*10+1,grid_width:9*grid_width,:]=0

    img[grid_height:10*grid_height,grid_width*1-1,:]=0
    img[grid_height:10*grid_height,grid_width*1-0,:]=0
    img[grid_height:10*grid_height,grid_width*1+1,:]=0

    for i in range(2,9):
        img[grid_height:5*grid_height,grid_width*i,:]=0
        img[grid_height*6:10*grid_height,grid_width*i,:]=0

    img[grid_height:10*grid_height,grid_width*9-1,:]=0
    img[grid_height:10*grid_height,grid_width*9-0,:]=0
    img[grid_height:10*grid_height,grid_width*9+1,:]=0

    cv2.line(img, (4*grid_width, 1*grid_height), (6*grid_width, 3*grid_height), (0,0,0), 1)
    cv2.line(img, (6*grid_width, 1*grid_height), (4*grid_width, 3*grid_height), (0,0,0), 1)

    cv2.line(img, (4*grid_width, 8*grid_height), (6*grid_width, 10*grid_height), (0,0,0), 1)
    cv2.line(img, (6*grid_width, 8*grid_height), (4*grid_width, 10*grid_height), (0,0,0), 1)



    img=cv2ImgAddText(img,'楚河',grid_width*2+20,5*grid_height+10,(0,0,0),grid_width-20)
    img=cv2ImgAddText(img,'汉界',grid_width*6+20,5*grid_height+10,(0,0,0),grid_width-20)

    return img

def PutChess(img0,chesses):
    name_dict={'rbing':'兵','rpao':'炮','rju':'车','rma':'马','rxiang':'相','rshi':'士','rshuai':'帅',
                 'bzu':'卒','bpao':'炮','bju':'车','bma':'马','bxiang':'象','bshi':'士','bjiang':'将'}
    imgr=img0.copy()
    imgb=img0.copy()
    imgb[:,:,:]=255
    x=img0.shape[1]
    y=img0.shape[0]
    for chess in chesses:
        name=chess[0]
        xi=(chess[1]+1)*grid_width
        yi=(10-chess[2])*grid_height
        len=min(grid_width, grid_height)

        if name[0] == 'r':
            cv2.circle(imgr,(xi,yi),len//2-5,(0,0,255),2)
            cv2.circle(imgr,(xi,yi),len//2-6,(255,255,255),-1)
            imgr=cv2ImgAddText(imgr,name_dict[name],xi-(len-10)//4,yi-(len-10)//4,(255,0,0),(len-10)//2)
        elif name[0] == 'b':
            cv2.circle(imgb,(x-xi,y-yi),len//2-5,(0,0,0),2)
            cv2.circle(imgb,(x-xi,y-yi),len//2-6,(255,255,255),-1)
            cv2.circle(imgr,(xi,yi),len//2-6,(255,255,255),-1)
            imgb=cv2ImgAddText(imgb,name_dict[name],x-xi-(len-10)//4,y-yi-(len-10)//4,(0,0,0),(len-10)//2)
    matRotate=cv2.getRotationMatrix2D((x*0.5,y*0.5),180,1.0)
    imgb=cv2.warpAffine(imgb,matRotate,(x,y))
    img=imgr&imgb
    return img

def LoadSituation(situation):
    chesses=[]
    if situation=='init':
        chesses.append(['rbing',0,3])
        chesses.append(['rbing',2,3])
        chesses.append(['rbing',4,3])
        chesses.append(['rbing',6,3])
        chesses.append(['rbing',8,3])
        chesses.append(['rpao',1,2])
        chesses.append(['rpao',7,2])
        chesses.append(['rju',0,0])
        chesses.append(['rju',8,0])
        chesses.append(['rma',1,0])
        chesses.append(['rma',7,0])
        chesses.append(['rxiang',2,0])
        chesses.append(['rxiang',6,0])
        chesses.append(['rshi',3,0])
        chesses.append(['rshi',5,0])
        chesses.append(['rshuai',4,0])
        chesses.append(['bzu',0,6])
        chesses.append(['bzu',2,6])
        chesses.append(['bzu',4,6])
        chesses.append(['bzu',6,6])
        chesses.append(['bzu',8,6])
        chesses.append(['bpao',1,7])
        chesses.append(['bpao',7,7])
        chesses.append(['bju',0,9])
        chesses.append(['bju',8,9])
        chesses.append(['bma',1,9])
        chesses.append(['bma',7,9])
        chesses.append(['bxiang',2,9])
        chesses.append(['bxiang',6,9])
        chesses.append(['bshi',3,9])
        chesses.append(['bshi',5,9])
        chesses.append(['bjiang',4,9])

    return chesses

def Move(chesses,now,next):
   for chess in chesses:
       if chess[1]==now[0] and chess[2]==now[1]:
           for chess2 in chesses:
               if chess2[1]==next[0] and chess2[2]==next[1]:
                   if  chess[0][0]==chess2[0][0]:
                       return False
                   else:
                       chesses.remove(chess2)
                       break
           chesses.append([chess[0],next[0],next[1]])
           chesses.remove(chess)
           return True
   return False

if __name__ == "__main__":
    img0=GetChessBoard()
    chesses=LoadSituation('init')
    img=PutChess(img0,chesses)
    cv2.imshow('ChessBoard',img)
    cv2.waitKey(0)
    while 1:
        flag=0
        i=random.randint(0,len(chesses)-1)
        while Move(chesses,(chesses[i][1],chesses[i][2]),(random.randint(0,8),random.randint(0,9)))==0:
            pass
        img=PutChess(img0,chesses)
        cv2.imshow('ChessBoard',img)
        cv2.waitKey(1)
        color=chesses[0][0][0]
        for chess in chesses:
            if color!= chess[0][0]:
                flag=1
                break
        if flag== 0:
            break
    cv2.waitKey(0)
