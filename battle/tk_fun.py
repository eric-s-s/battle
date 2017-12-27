import tkinter as tk
import random
from itertools import cycle

main_tk = tk.Tk()
label_text = tk.StringVar()
label_text.set('not yet')
label = tk.Label(master=main_tk, textvariable=label_text)

texts = cycle(['a', 'b', 'c', '1', '2', '3', 'restart'])


def texter():
    new_text = random.choice(['hi', 'hello', 'go die', 'you suck', 'you are so awesome', 'i love you'])
    label_text.set(new_text)
    button.config(text=next(texts))

button = tk.Button(master=main_tk, text='try it', command=texter)

label.pack()
button.pack()

main_tk.mainloop()

