from tkinter import *
from tkinter.ttk import *
from PIL import Image,ImageTk,ImageDraw
from tkinter import messagebox as msgbox
from tkinter.filedialog import askdirectory
import os
import code_writ
def strroot():
    global top, logo
    top=Tk()
    top.title("ATC")
    top.resizable(0,0)
    logo=Image.open("images/AWG_middle-1.png")
    logo=ImageTk.PhotoImage(logo)
    top.iconphoto(False, logo)
def destroy():
    top.destroy()
def enter():
    frame1.destroy()
    frame2=Frame(top,height=500,width=500)
    frame2.grid(column=0,row=0)
    def run():
        frame2.destroy()
        strpg()
    canvas1=Canvas(frame2,width=500,height=500,bg="#3c1d3f",highlightthickness=0)
    canvas1.place(x=0,y=0)
    img2=ImageTk.PhotoImage(file="images/project_bg3.jpg")
    frame2.img2=img2
    canvas1.create_image(200,200,anchor=CENTER,image=img2)
    canvas1.place(x=0,y=0)
    ent1=Entry(frame2,font=("calibri",20))
    ent1.place(x=20,y=50)
    ent1.insert(END,os.getcwd())
    def save():
        nonlocal folder_path
        folder_loc=askdirectory()
        if folder_loc:
            ent1.delete(0,END)
            ent1.insert(END,folder_loc)
            folderPath.set(folder_loc)
            folder_path=folderPath.get()
        if folder_loc is None:
            return
    def runit(a):
        folder_path=ent1.get()
        if folder_path=="" and a!=2:
            msgbox.showinfo(title = 'Alert!' , message = 'Choose a folder location to save files before continuing.')
        else:
            msgbox.showinfo(title = 'Alert!' , message = 'Loading..')
            code_writ.main(a,folder_path)
    folderPath=StringVar()
    folder_path=os.getcwd()
    style=Style()
    style.configure("TButton",font=("calibri",20,"bold","underline"),borderwidth="4")
    style.map("TButton",foreground=[("active","!disabled","green")],background=[("active","black")])
    label0=Label(frame2,text="Enter location to save images",font=("Courier",16,"italic"))
    label0.place(x=20,y=17)
    btn101 = Button(frame2, text = 'Browse', command = lambda:save())
    btn101.place(x=330,y=50)
    label2=Label(frame2,text="Instructions:\n1. Press q to stop the program\n2. Press c to clear the screen\n3. Press s to save the file",font=("Courier",16,"italic"))
    label2.place(x=50,y=110)
    btn102=Button(frame2,text="Back",command=run)
    btn102.place(x=330,y=440)
    btn103=Button(frame2,text="Select for camera feed",command= lambda:runit(1))
    btn103.place(x=20,y=235)
    btn104=Button(frame2,text="Select for plain image feed",command=lambda:runit(0))
    btn104.place(x=20,y=300)
    btn105=Button(frame2,text="Select to check if green object is detected",command=lambda:runit(2))
    btn105.place(x=20,y=365)
def strpg():
    global frame1    
    frame1=Frame(top,height=500,width=500)
    frame1.grid(column=0,row=0)
    canvas1=Canvas(frame1,width=500,height=500,bg="#3c1d3f",highlightthickness=0)
    canvas1.grid(columnspan=3)
    img1=ImageTk.PhotoImage(file="images/project_bg3.jpg")
    canvas1.create_image(200,200,anchor=CENTER,image=img1)
    canvas1.grid(columnspan=3)
    logo_test=Label(image=logo)
    logo_test.grid(column=0,row=0,sticky='n')
    style=Style()
    style.configure("TButton",font=("calibri",20,"bold","underline"),borderwidth="4")
    style.map("TButton",foreground=[("active","!disabled","blueviolet")],background=[("active","black")])
    B1=Button(frame1,text="Enter",command=enter)
    B1.place(x=165,y=408)
    B2=Button(frame1,text="Exit",command=destroy)
    B2.place(x=165,y=455)
    top.mainloop()
def main():
    strroot()
    strpg()
if __name__ == '__main__':
    main()