from  tkinter import *
import subprocess
import sv_ttk
import os
import sys
import pathlib
import time
import queue
from threading import Thread
import keyboard



def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

class Ui(Tk):
    def stop(self):
        self.withdraw()
        self.T.delete(0,'end')
        self.T.update()
    def __init__(self):
        
        Tk.__init__(self)
        self.v1 , self.v2 = int(self.winfo_screenwidth()/5),int(self.winfo_screenmmheight()/6)
        self.loc = (self.winfo_pointerx()-self.v1/2, self.winfo_pointery()-self.v2/2)
        sv_ttk.set_theme("dark")
        self.epath ="/everything/es.exe"
        self.bind("<Escape>",lambda x: self.stop())
        self.T = Entry(self, font=("DejaVu Sans Mono", 12),width=int(self.v1),relief="flat",background="grey15")
        self.attributes('-topmost',True)
        self.geometry('%dx%d+%d+%d' % (self.v1, self.v2, self.winfo_pointerx()-self.v1/2, self.winfo_pointery()-self.v2/2))
        self.focus()
        self.process = None
       
        self.bb = Frame(self)
        self.sc = Scrollbar(self.bb,orient=HORIZONTAL)
        self.box = Listbox(self.bb,)
        self.box.config(xscrollcommand = self.sc.set) 
        self.sc.config(command = self.box.xview) 
        self.configure( highlightcolor="grey90",highlightthickness=1)
        self.overrideredirect(True)
        self.T.bind("<ButtonPress-1>", self.start_move)
        self.T.bind("<B1-Motion>", self.do_move)
        self.box.bind("<ButtonPress-1>", self.start_move)
        self.box.bind("<B1-Motion>", self.do_move)
        self.repack()
        self.flag = None
        self.proc = None
        self.run = True
        self.is_packed = False
        self.th = Thread(target=self.waitfinput)
        self.th.start()
        self.bind("<Key>",lambda x :self.showres())
        self.box.bind('<Double-Button-1>',self.clickbox)
        self.box.bind('<Double-Button-3>',self.clickbox)
        self.lf()
        keyboard.add_hotkey("ctrl+alt+s",lambda: self.show())
        self.stop()
        self.mainloop()
    def flager(self):
        self.flag = time.time()
    def show(self):
        if self.state()!="normal":
            self.loc = (self.winfo_pointerx()-self.v1/2, self.winfo_pointery()-self.v2/2)
            self.repack()
            if self.is_packed:
                self.geometry('%dx%d+%d+%d' % (self.v1,int(12*1.34*16),self.loc[0],self.loc[1]))
            else:
                self.geometry('%dx%d+%d+%d' % (self.v1, self.v2, self.winfo_pointerx()-self.v1/2, self.winfo_pointery()-self.v2/2))
            self.deiconify()
    def waitfinput(self):
        while self.run :
            time.sleep(0.001)
            if self.flag!=None and time.time()-self.flag >=0.8:
                v =self.T.get()
                if (v!=""):
                    self.exec(v)
                    self.flag = None
                else:
                    if (self.bb.winfo_viewable()):
                        self.is_packed = False
                        self.bb.pack_forget()
                        self.geometry('%dx%d+%d+%d' % (self.v1, self.v2, self.loc[0],self.loc[1]))
                       
    def lf(self):
        self.lift()
        self.after(10,self.lf)
    def repack(self):
        self.configure( highlightcolor="grey90",highlightthickness=1,highlightbackground="grey70")
        self.T.pack_forget()
        self.T.pack(side="top",expand=True,fill="both",padx=5,pady=4)
    
    def exec(self,comm):
        self.process = subprocess.Popen(self.epath+" "+comm, shell=True,cwd=os.path.dirname(os.path.realpath(__file__)), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        
        self.box.yview = (0,"units")
        self.geometry('%dx%d+%d+%d' % (self.v1,int(12*1.34*16),self.loc[0],self.loc[1]))
        if (self.proc != None):
            
            self.proc.stop()
            self.proc.join()
        self.box.delete(0,"end")
        self.proc = process(self.process,self.box)
        
        self.proc.start()   
        self.box.pack(expand=True, fill="both",side="top")
        self.sc.pack(side="bottom",fill="both")
        self.bb.pack(expand=True, fill="both",side="bottom",padx=2,pady=0)
        self.is_packed = True
        self.repack()
    def clickbox(self,event):
        self.box.selection_clear(0,END)
        self.box.selection_set(self.box.nearest(event.y))
        self.box.activate(self.box.nearest(event.y))
        index = int(self.box.curselection()[0])
        value = self.box.get(index)
       
        if (event.num == 1):           
            subprocess.Popen(r'explorer /select,"{0}"'.format(value))
        elif(event.num == 3):
            copy2clip(value)
            self.configure(highlightcolor="green",highlightthickness=4)
            

        # Note here that Tkinter passes an event object to onselect()

    
    def showres(self):
        self.flager()
        
       
    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = int(self.winfo_x() + deltax)
        y = int(self.winfo_y() + deltay)
        self.loc = (int(x),int(y))
        self.geometry(f"+{x}+{y}")
    def start_move(self, event):
        self.x ,self.y= (event.x,event.y)
        

class process(Thread):
    def __init__(self,proc,box, args=(), kwargs=None):
        Thread.__init__(self, args=(), kwargs=None)
        self.proc = proc
        
        self.box = box
        self._run = True
    def run(self):
        self.update()
    def stop(self):
        self._run = False
    def update(self):

        c = self.proc.stdout.readline().decode("ISO-8859-1")
        while c and self._run:
            self.box.insert("end",c)
            c = self.proc.stdout.readline().decode("ISO-8859-1")

u = Ui()
       