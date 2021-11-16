import tkinter as tk

root = tk.Tk()

root.geometry('300x200')
root.title('サンプルプログラム')

buffer = tk.StringVar() # ①
buffer.set('')

# キーの表示
def print_key(event): # ③
    key = event.keysym
    buffer.set('入力された値: %s' % key)

# ラベルの設定
tk.Label(root, text='何か入力してください。').pack()
a = tk.Label(root, textvariable=buffer) # ②
a.pack()
a.bind('<Key>', print_key) # ④
a.focus_set() # ⑤

root.mainloop()
 
