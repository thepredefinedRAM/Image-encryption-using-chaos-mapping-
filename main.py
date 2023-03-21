from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image as im

import frames


def resize_bg(event):
    root.update()
    print(event.width, ":", event.height)
    startframe.configure(width=event.width, height=event.height)

root = Tk()
root.title("Encrypt It")
root.geometry("700x750")
# root.wm_attributes("-transparentcolor", "#ceebd5")
# root.iconbitmap()

# mainframe = Frame(root)
# mainframe.pack(fill=BOTH, expand=1)
#
# canvas = Canvas(mainframe)
# canvas.pack(side=LEFT, fill=BOTH, expand=1)
#
# scrollbar = ttk.Scrollbar(mainframe, orient=VERTICAL, command=canvas.yview)
# scrollbar.pack(side=RIGHT, fill=Y)
#
# canvas.configure(yscrollcommand=scrollbar.set)
# canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
#
# bg = ImageTk.PhotoImage(file="orig.png")
# canvas.create_image(0, 0, image=bg, anchor='nw')
#
# innermainframe = Frame(canvas)
# canvas.create_window((0, 0), window=innermainframe, anchor="nw")
# bg = PhotoImage(file="D:\\EncryptIt\\orig.png")
# label1 = Label(root, image=bg)
# label1.place(x=0, y=0)
innermainframe = root
label = Label(innermainframe, text="Encrypt It", font=("COPPERPLATE GOTHIC BOLD", 56, "bold"))
label.pack()

startframe = Frame(innermainframe)

# Start Frame
startframe.pack(fill='both', expand=1)
# startframe.configure(width=750, height=700)
options = [
    "Logistic Chaos Map",
    "Arnold Cat Transform"
]
selected = StringVar()
selected.set("Logistic Chaos Map")
drop = OptionMenu(startframe, selected, *options)
drop.configure(font=("COPPERPLATE GOTHIC LIGHT", 30, "bold"))
drop.place(relx=0.5, rely=0.3, anchor=CENTER)
Button(startframe,
       text="Encrypt",
       font=("COPPERPLATE GOTHIC LIGHT", 20, "bold"),
       command=lambda: frames.CryptoFrame(innermainframe, startframe, selected.get(), "Encrypt")).place(relx=0.25,
                                                                                                        rely=0.5,
                                                                                                        anchor=CENTER)
Button(startframe,
       text="Decrypt",
       font=("COPPERPLATE GOTHIC LIGHT", 20, "bold"),
       command=lambda: frames.CryptoFrame(innermainframe, startframe, selected.get(), "Decrypt")).place(relx=0.5,
                                                                                                        rely=0.5,
                                                                                                        anchor=CENTER)
Button(startframe,
       text="Analysis",
       font=("COPPERPLATE GOTHIC LIGHT", 20, "bold"),
       command=lambda: frames.AnalysisFrame(innermainframe, startframe)).place(relx=0.75, rely=0.5, anchor=CENTER)

# root.bind("<Configure>", resize_bg)
root.mainloop()
