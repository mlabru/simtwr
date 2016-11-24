import Tkinter

root = Tkinter.Frame()
#root.title('Scrollbar')

list = Tkinter.Listbox(root, height=6, width=15)
scroll = Tkinter.Scrollbar(root, command=list.yview)

list.configure(yscrollcommand=scroll.set)
list.pack(side=Tkinter.LEFT, fill=Tkinter.Y)

scroll.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

for i in range(30): 
   list.insert(Tkinter.END, i)

root.pack(side=Tkinter.TOP)

F2 = Tkinter.Frame()
lab = Tkinter.Label(F2)

def poll():
    lab.after(200, poll)
    sel = list.curselection()
    lab.config(text=str(sel))

lab.pack()
F2.pack(side=Tkinter.TOP)

poll()
Tkinter.mainloop()
