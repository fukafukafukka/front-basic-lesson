import tkinter as tk
import time

#ウインドを作成
root=tk.Tk()
root.geometry('400x400')
root.title('canvasの使い方')

#図形を壁画するキャンバスをウインド上に作成
canvas=tk.Canvas(root,width=300,height=300,bg="white")
canvas.pack()

#図形の壁画
dx=20
dy=20
square=canvas.create_rectangle(5,5,5+dx,5+dy,fill='red')#四角

#動かすためのパラメータ
x=150#四角の初期x座標
y=150#四角の初期y座標
Vy=2#どのくらいの速度で動かすか
Y_current=300-dy#どこまで動かすか（基本はcanvasの端から端）

start=time.time() #開始時間
stop_time=10 #目標終了時間

#無限ループ
while True:
    canvas.coords(square,x,y,x+dx,y+dy) #squareを指定の座標に移動させる
    y+=Vy #縦方向に少しづつ動かす
    if y<=0: #上端に到達したら
        Vy=abs(Vy) #下向きに動かす
    elif y>=Y_current: #下端に到達したら
        Vy=-abs(Vy) #上向きに動かす
    time.sleep(0.02) #0.02秒ずつ更新
    root.update() #ウインド画面を更新
    
    #目標終了時間に達したらループから抜ける
    if time.time()-start>stop_time:
        print('処理時間は',time.time()-start,'秒です')
        break

root.mainloop()
