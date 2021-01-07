




import tkinter as tk
from tkinter import messagebox
from tkinter import font
import threading

import os
import sys

def importpackages():
    print("Importing packages")
    global paramiko, ScrolledText, pd, time, ttk, math
    global __varc__
    
    __varc__=['paramiko', 'tkinter.scrolledtext', 'pandas', 'time', 'tkinter', 'math']    

    import paramiko
    from tkinter.scrolledtext import ScrolledText
    import time
    import pandas as pd
    from tkinter import ttk
    import math
    
    print("Import complete")    

    pd.set_option('display.width', 2000000000)
    pd.set_option('display.max_columns', 10000)
    pd.set_option('display.max_rows', 5000000000)
    pd.set_option('precision',2)

class loginclass():
    formpadx=30
    formpady=30
    labelwidth=10
    labelheight=30
    entryheight=30
    entrywidth=60
    widthratio=7.6

    cmdheight=25
    cmdwidth=15
    
    entrytextlist=['Server', 'User ID', 'Password']
    labellist=[]
    entrylist=[]

    status=''
    
    
    def __init__(self):
        self.window=tk.Tk()
        self.login_font=font.Font(family='arial', size=12, weight=font.NORMAL)
        
        self.window.title('Login')
        self.window.resizable(0,0)
##        self.window.overrideredirect(1)

        self.formheight=200
        self.formwidth=int(  (self.formpadx*2) + (self.labelwidth * self.widthratio) + ((self.entrywidth-7.894) * self.widthratio) ) + 0
        xpos=int(  (self.window.winfo_screenwidth() - self.formwidth) / 2  )
        ypos=int(  (self.window.winfo_screenheight() - self.formheight) / 2    )
        
        self.window.wm_geometry(f"{self.formwidth}x{self.formheight}+{xpos}+{ypos}")   ##widthxheight+x wrt screen+y wrt screen
        self.window.update_idletasks()
        self.appwidth=self.window.winfo_width()
        self.appheight=self.window.winfo_height()

        self.window.update_idletasks()
        
        self.initwindow()
        self.entrylist[self.entrytextlist.index('Password')].configure(show='*')
        self.window.update_idletasks()
        
    def initwindow(self):
        self.frame=tk.Frame(self.window, bg=COLOR_FRAME_BG)
        self.frame.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        self.server=tk.StringVar(self.frame, "server")
        self.user=tk.StringVar(self.frame, "userid")
        self.pwd=tk.StringVar(self.frame)
        for text in self.entrytextlist:
            self.label=tk.Label(self.frame, width=self.labelwidth, text=text) #, font=self.login_font)  
            self.entry=tk.Entry(self.frame, width=self.entrywidth)      ##, font=self.login_font )

            self.label.place(x=self.formpadx, y=(self.formpady + self.entrytextlist.index(text) * self.labelheight) )
            self.entry.place(x=self.formpadx + (self.labelwidth * self.widthratio), y=self.formpady + (self.entrytextlist.index(text) * self.labelheight) )
            
            self.labellist.append(self.label)
            self.entrylist.append(self.entry)
        self.entrylist[0].configure(textvariable=self.server)
        self.entrylist[1].configure(textvariable=self.user)
        self.entrylist[2].configure(textvariable=self.pwd)
        
        self.cmdquit = tk.Button(self.window, width=self.cmdwidth, text='Quit', bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, bd=3, command=exit)
        self.cmdsubmit=tk.Button(self.window, width=self.cmdwidth, text='Submit', bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, bd=3, command=self.logintoserver)
        self.window.update_idletasks()
        xgap=int(    (self.appwidth-(self.cmdwidth*self.widthratio*2)) / 3    )
        y=self.entrylist[-1].winfo_y() + self.labelheight + 10
        self.cmdquit.place(  x=xgap, y=y  )
        self.cmdsubmit.place(  x=(xgap*2) + (self.cmdwidth*self.widthratio), y=y  )

        self.window.update_idletasks()
        self.connstatus=tk.StringVar()
        self.connstatus.set("Enter login credentials...")
        self.statusbar=tk.Label(self.frame, textvariable=self.connstatus, anchor='w')
        self.statusbar.place( x=0, y=self.cmdquit.winfo_y()+10 + self.labelheight, relwidth=1.0)
            
    def logintoserver(self):
        global connstatus
        self.window.update_idletasks()
        if self.server.get()=='' or self.user.get()=='' or  self.pwd.get()=='':
            self.connstatus.set("Please enter the server/ credentials...")
        else:
            self.connstatus.set("Connecting to Server ...  PLEASE WAIT ")
            self.window.update_idletasks()
            try:
                self.ssh = paramiko.SSHClient() 
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
                self.ssh.connect(self.server.get(), 22, self.user.get(), self.pwd.get())
                self.connstatus.set("Connected")
                self.status=1

                connstatus='connected'
                self.dq=dqclass()
                self.window.withdraw()
            except Exception as ex:
                self.status=str(ex)
                self.connstatus.set(str(ex))
            finally:
                self.window.update_idletasks()
        

class dqclass(threading.Thread):
    formpadx=30
    formpady=30
    labelwidth=10
    labelheight=30
    entryheight=30
    entrywidth=30
    widthratio=7.6

    cmdheight=25
    cmdwidth=15
    cmdtextlist=['New', 'Export', 'Exit']
    cmdlist=[]

    dslist=[]  ## list of list containing path, ds name with extension and ds name without extension eg[/anenv/prd, cnsp.sas7bdat, cnsp]    
    dsbtnwidth=20
    dsbtnlist=[]
    dflist=[]

    pagelist=[]
    profilelist=[]

    ask=0
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.window=tk.Tk()
        self.window.title('Python Data Quality')

        self.window.update_idletasks()
        self.appwidth=self.window.winfo_width()
        self.appheight=self.window.winfo_height()

        w=int(  self.window.winfo_screenwidth() * 0.7 )
        h=int(  self.window.winfo_screenheight() * 0.7 )
        xpos=int(  (self.window.winfo_screenwidth() - w) / 2  )
        ypos=int(  (self.window.winfo_screenheight() - h) / 4    )
        self.window.wm_geometry(f"{w}x{h}+{xpos}+{ypos}")
        self.window.minsize(int(w*0.5), int(h*0.5))

        self.colors=['gray','red','green','blue','yellow']
        self.ypos=0
        
        self.initwindow()
        self.window.bind('<Configure>', self.positionwindow)

        th=threading.Thread(target=self.ssh_live, args=())
        th.start()
        
        
    def initwindow(self):
        global connstatus
        self.cmdframe=tk.Frame(self.window, bg=COLOR_FRAME_BG, height=self.cmdheight )
        for text in self.cmdtextlist:
            self.cmd=tk.Button(self.cmdframe, width=self.cmdwidth, text=text, bg=COLOR_FRAME_BG, fg=COLOR_BTN_FG, bd=0)
            self.cmd.place(x=self.cmdwidth*self.widthratio*self.cmdtextlist.index(text), y=0, relheight=1.0)
            self.cmdlist.append(self.cmd)
        self.cmdlist[self.cmdtextlist.index('New')].configure(command=self.getinputs)
        self.cmdlist[self.cmdtextlist.index('Exit')].configure(command=self.exit_program)
        
        self.dsframe=tk.Frame(self.window, bg=COLOR_FORM_BG, height=self.cmdheight)
        
        self.pageframe=tk.Frame(self.window, bg=COLOR_FORM_BG )
        
        self.statusframe=tk.Frame(self.window, bg=COLOR_FRAME_BG,  height=self.cmdheight)
        self.connstatus=tk.StringVar()
        self.connstatus.set('CONNECTED')
        self.statusbar=tk.Label(self.statusframe, textvariable=self.connstatus, anchor='w', bg=COLOR_FRAME_BG, fg=COLOR_FRAME_FG, width=10)
        self.statusbar.place( x=0, y=0, relheight=1.0)
        self.window.update_idletasks()
        
##        print(connstatus)
##        print(self.connstatus.get())
##        print('aa')

##        self.statusbar=tk.Label(self.frame, textvariable=connstatus, anchor='w')
##        self.statusbar.place( x=0, y=self.cmdquit.winfo_y() + self.labelheight, relwidth=1.0)

    def positionwindow(self, event):
        self.window.update_idletasks()
        self.appwidth=self.window.winfo_width()
        self.appheight=self.window.winfo_height()
        
        self.cmdframe.place(x=0, y=0, relwidth=1.0)
        self.dsframe.place(x=0, y=self.cmdheight, relwidth=1.0)
        self.pageframe.place(x=0, y=self.cmdheight*2, relwidth=1, height=self.appheight-(self.cmdheight*3))
        self.statusframe.place(x=0, y=self.appheight-self.cmdheight, relwidth=1.0)
        self.window.update_idletasks()

##        messagebox.showinfo("DQ CLASS")
        
                
    def getinputs(self):
        global __varc__

        if self.ask==1:
            return
        if len(self.dslist) >=5:
            messagebox.showinfo("Information", "You can do the analysis for maximum 5 datasets.")
            return
        for v in __varc__:
            if v not in sys.modules:
                print(f'Module {v} not yet imported. Please try again.')
                return
                
        self.inpwindow=tk.Toplevel()
        self.inpwindow.resizable(0,0)

        entrytextlist=['Absolute Path']
        labellist=[]
        entrylist=[]
        
        labelwidth=int(len(max(entrytextlist, key=len)) * 0.9)
        entryheight=2
        entrywidth=60
        
        w=int(  (self.formpadx*2) + (labelwidth * self.widthratio) + ((entrywidth*1.1) * self.widthratio) )
        h=230  ##140
        xpos= int(  (self.window.winfo_x() + (self.window.winfo_width()-w)) / 2  )
        ypos= int(  (self.window.winfo_y() + (self.window.winfo_height()-h)) / 2  )
        self.inpwindow.wm_geometry(f"{w}x{h}+{xpos}+{ypos}")
        self.inpwindow.title('Data Source')
        
        for text in entrytextlist:
            label=tk.Label(self.inpwindow, width=labelwidth, text=text, anchor='w')  ##, bg='red')
            entry=ScrolledText(self.inpwindow, height=entryheight, width=entrywidth)

            label.place(x=self.formpadx, y=(self.formpady + entrytextlist.index(text) * self.labelheight) )
            entry.place(x=self.formpadx + (labelwidth * self.widthratio), y=self.formpady + (entrytextlist.index(text) * self.labelheight) )
            
            labellist.append(label)
            entrylist.append(entry)

        self.radiooption=tk.IntVar()
        radiolocal =tk.Radiobutton(self.inpwindow, width=10, text='Local file', variable=self.radiooption, value=1)
        radioremote=tk.Radiobutton(self.inpwindow, width=10, text='Remote file', variable=self.radiooption, value=2)
        xgap=int(    (w - (self.cmdwidth*self.widthratio*2)) / 3    )
        y=entrylist[-1].winfo_y() + (entryheight*1.3*self.labelheight) + 10
        radiolocal.place(  x=xgap, y=y  )
        radioremote.place(  x=(xgap*2) + (self.cmdwidth*self.widthratio), y=y  )
        
        
        cmdquit = tk.Button(self.inpwindow, width=self.cmdwidth, text='Cancel', bg=COLOR_BTN_BG, fg=COLOR_BTN_FG,
                            command=lambda: self.cancelinput(self.inpwindow) )
        cmdsubmit=tk.Button(self.inpwindow, width=self.cmdwidth, text='Submit', bg=COLOR_BTN_BG, fg=COLOR_BTN_FG,
                            command=lambda: self.submitinput(self.inpwindow, self.radiooption.get(), entrylist[0].get(1.0, tk.END)))
        self.inpwindow.update_idletasks()
        xgap=int(    (w - (self.cmdwidth*self.widthratio*2)) / 3    )
        y=radiolocal.winfo_y() + radiolocal.winfo_height() + 10
        cmdquit.place(  x=xgap, y=y  )
        cmdsubmit.place(  x=(xgap*2) + (self.cmdwidth*self.widthratio), y=y  )

        self.helptext=tk.StringVar()
        ht=(f"Please enter absolute path e.g. \n\n"
            f"For remote - sasdatasetpath\n"
            f"For local  - sasdatasetpath")

        self.helptext.set(ht)
        self.statusbar=tk.Message(self.inpwindow, anchor='nw', textvariable=self.helptext, width=700, bg=COLOR_HELPMSG_BG, fg=COLOR_HELPMSG_FG)
        self.statusbar.place(x=0, y=y + self.labelheight+10, relwidth=1.0)

        self.ask=1

    def cancelinput(self, iw):
        self.ask=0
        iw.destroy()
        
    def submitinput(self, iw, rem_loc, path):
        print(rem_loc)
        global pd
        while path[-1]=='\n':
            path=path[:-1]
        if ( os.path.splitext(path)[1][1:] == ''):
            messagebox.showerror(title="Error", message="Please enter a correct path with extension")
            return
        
        self.dslist.append( [path,
                         os.path.dirname(path),
                         os.path.basename(path).split(".")[0],
                         os.path.splitext(path)[1][1:] ] )
        try:
            self.helptext.set("Reading the file ...  PLEASE WAIT")
            self.inpwindow.update_idletasks()

            if rem_loc==2:
                sftp=login.ssh.open_sftp()
                rfile=sftp.open(self.dslist[-1][0], 'r') 
                reader=pd.read_sas(rfile, format='sas7bdat', chunksize=100)
                data=[d for d in reader]
                df=pd.concat(data)
                sftp.close()
            elif rem_loc==1:
                df=pd.read_sas(self.dslist[-1][0], 'sas7bdat')
                
            if not (df.empty):
                self.dflist.append(df)
                self.profilelist.append( profiling(df=df, ds=self.dslist[-1], app=self, ypos=self.ypos*50) )    ##color=self.colors[self.ypos],
                self.ypos+=1
        except Exception as ex:
            messagebox.showinfo(title="Reading error", message=str(ex))
            self.helptext.set(f"Reading error")
            self.inpwindow.update_idletasks()
        finally:
            iw.destroy()

        self.ask=0

    def ssh_live(self):
        global keep_conn_live
        while keep_conn_live:
            command='ls -l /home'
            stdin, stdout, stderr = login.ssh.exec_command(command=command)
            time.sleep(10)
            
        
    def exit_program(self):
        global keep_conn_live
        keep_conn_live=0
        print(f"val={keep_conn_live}")
        self.window.destroy()

class profiling():
    dtypes=['number', 'object', 'datetime', 'category']
    
    def __init__(self, df, ds, app, ypos, *args, **kwargs):  ##color, 
        self.df=df
        self.ds=ds
        self.app=app
##        self.color=color
        self.ypos=ypos

        print('basic')
        self.basic()
        print('full')
        self.full()
        print('summframe')
        self.summframe()

        self.canvas.bind('<Configure>', self.positionwindow1)
        
    def positionwindow1(self, event):
        self.app.window.update_idletasks()
        self.frame.place(x=0,y=0, relheight=1.0, relwidth=1.0)
        self.app.window.update_idletasks()

        self.cframe.configure(height=self.app.pageframe.winfo_height()-8, width=self.app.pageframe.winfo_width())
        self.app.window.update_idletasks()
        
        self.cframe1.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        self.heading.place(x=0, y=0, relwidth=1.0)

        self.scrollbar.configure(command=self.canvas.yview)
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL), yscrollcommand=self.scrollbar.set)

        x=(self.cframe.winfo_height() - self.heading.winfo_height())/self.app.labelheight
##        self.treedescribe.configure(height=int(x/1))   ##hello
        
        self.app.dsframe.configure(bg=COLOR_FORM_BG)

##        messagebox.showinfo("",f"PROFILE CLASS   -  {self.treedescribe.cget('height')}")
        
    def summframe(self):
        ##len(self.app.dslist[len(self.app.dslist)-1][2])
        self.label=tk.Button(self.app.dsframe,
                             width=30,
                             bg='gray',
                             text=self.app.dslist[len(self.app.dslist)-1][2],
                             command=lambda:self.showframe(self.frame) )
        self.app.dsbtnlist.append(self.label)
        x=sum(btn.cget('width')+2 for btn in self.app.dsbtnlist) * self.app.widthratio
        self.label.place(x=(len(self.app.dsbtnlist)-1)*self.app.dsbtnwidth*self.app.widthratio, y=0)
        self.label.place(x=(len(self.app.dsbtnlist)-1)*30*self.app.widthratio, y=0)


        self.frame=tk.Frame(self.app.pageframe, width=50, height=50, bg='gray') ##self.color )
        self.app.pagelist.append(self.frame)
        self.frame.place(x=0,y=0, relheight=1.0, relwidth=1.0)  #y=self.ypos, x=self.ypos)

        self.canvas=tk.Canvas(self.frame, bd=2, relief=tk.RAISED, bg='blue')
        self.scrollbar=tk.Scrollbar(self.frame, orient='vertical', command=self.canvas.yview, width=20)
        self.canvas.place(x=20, y=0, relwidth=1.0, relheight=1.0)
        self.scrollbar.place(x=0, y=0, relheight=1.0)

        self.cframe=tk.Frame(self.canvas)
        self.canvas.create_window(0,0, anchor='nw', window=self.cframe),

        self.app.window.update_idletasks()
        self.cframe.configure(height=self.app.pageframe.winfo_height()-8, width=self.app.pageframe.winfo_width())
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL), yscrollcommand=self.scrollbar.set)
        self.app.window.update_idletasks()
        
        self.cframe1=tk.Frame(self.cframe, height=500, width=500)
        self.cframe1.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        self.app.window.update_idletasks()

        self.heading=tk.Label(self.cframe1, text=self.ds[2], font=('times new roman',25), anchor='center', height=1)
        self.heading.place(x=0, y=0, relwidth=1.0)
        self.app.window.update_idletasks()

        self.treebasic=ttk.Treeview(self.cframe1, columns=list('a'*len(self.basicsumm[0])), show='tree', height=len(self.basicsumm))
        for item in self.basicsumm:
            self.treebasic.insert("", "end", text="", values=item)
        self.treebasic.place(x=0, y=self.heading.winfo_height(), relwidth=1.0)
        self.app.window.update_idletasks()

        
        self.describe.rename(columns={'count':'completeness', 'unique':'uniqueness'}, inplace=True)
        cols=['VARIABLE', 'DATATYPE'] + list(self.describe.columns)
        self.tdf=pd.merge(self.df.head().dtypes.reset_index().rename(columns={0:'DATATYPE'}),
                     self.describe.reset_index(),
                     on='index', left_index=False, right_index=False, indicator=False)
        self.tdf.rename(columns={'index':'VARIABLE'}, inplace=True)
        self.tdf.columns=[c.upper() for c in self.tdf.columns]
        self.tdf.sort_values(['DATATYPE','UNIQUENESS','COMPLETENESS','VARIABLE'], inplace=True)
        roundcols=['MEAN','STD','MIN','MAX']
        for c in roundcols:
            self.tdf[c]=self.tdf[c].apply(lambda x: int(x) if not math.isnan(x) else None )

        
        self.treedescribe=ttk.Treeview(self.cframe1, columns=cols, show='headings', height=20)   ##, height=min(20, len(self.tdf)) )
        for i in range(len(cols)):
            self.treedescribe.column(i, anchor='c')
            self.treedescribe.heading(i, text=cols[i].upper())
        for row in self.tdf.iterrows():
            self.treedescribe.insert("", "end", text="", values=tuple(row[1]) )
        self.treedescribe.place(x=0, y=self.treebasic.winfo_y()+self.treebasic.winfo_height(), relwidth=1.0)
        
        self.app.window.update_idletasks()
        
        self.positionwindow1(None)
        
    def showframe(self, f1):
        for f in self.app.pagelist:
            f.place_forget()
        f1.place(x=0, y=0, relheight=1.0, relwidth=1.0)
        
    def basic(self):
        self.numvars =self.df.head(50).select_dtypes('number').columns
        self.charvars=self.df.head(50).select_dtypes('character').columns
        self.charvars=self.charvars.append(self.df.head(50).select_dtypes('object').columns)
        self.datevars=self.df.head(50).select_dtypes('datetime').columns
        self.basicsumm=[]
        self.basicsumm.append(['Number of variables',    len(self.df.columns) ])
        self.basicsumm.append(['Number of numeric variables', len(self.numvars)  ])
        self.basicsumm.append(['Number of character variables', len(self.charvars)  ])
        self.basicsumm.append(['Number of datetime variables', len(self.datevars)  ])
        
        self.basicsumm.append(['Number of observations',  len(self.df)         ])
        self.basicsumm.append(['Missing cells',          f"{sum(self.df.isnull().sum())} ({  round(  sum(self.df.isnull().sum())  /  self.df.size*100, 3  )}%)"  ])
        self.basicsumm.append(['Memory usage',  f"{int(self.df.memory_usage().sum()/1024)} KB"     ])

##        self.varlist=list(self.df.columns)
        print(self.basicsumm)
        
    def full(self):
        maxth=30
        thcnt=[0]
        thlist=[]
        dfs=[]
##        stat=pd.concat( [self.df.select_dtypes(dt).describe().T for dt in self.dtypes if not self.df.head(5).select_dtypes(dt).empty], sort=None)
        for c in self.df.columns:
            th=threading.Thread(target=self.getdescribe, args=(dfs, self.df[[c]], thcnt) )
            if thcnt[0] > maxth:
                time.sleep(3)
            th.start()
            thlist.append(th)
        for th in thlist:
            th.join()

        cols=['count', 'unique', 'mean', 'std', 'min', 'max']
        describe=pd.concat(dfs, sort=False)

        _len=len(self.df)
        describe['count1']=describe['count'].apply(lambda x: None if math.isnan(x) else f"{round(x/_len*100, 2)}%" )
        describe['unique1']=describe['unique'].apply(lambda x: None if math.isnan(x) else f"{round(x/_len*100, 2)}%" )
        describe.drop(columns=['count','unique'], axis=1, inplace=True)
        describe.rename(columns={'count1':'count', 'unique1':'unique'}, inplace=True)
        
        self.describe=describe[cols].reindex(cols, axis=1)
        
    def getdescribe(self, dfs, df, thcnt):
        thcnt[0]+=1
        try:
            dfs.append(df.describe().T)
        except:
            pass
        thcnt[0]-=1
        
    

def hex_color(*colors):
    return f"#{''.join([ hex(c).split('x')[-1].zfill(2)  for c in colors ])}"

if __name__=='__main__':
    file=r"sasdatasetpath"
    print(file)

    keep_conn_live=1
    print(f"val={keep_conn_live}")

    COLOR_FORM_BG=hex_color(255,255,255)
    COLOR_FORM_FG=hex_color(0,0,0)
    COLOR_FRAME_BG=hex_color(242,242,242)
    COLOR_FRAME_FG=hex_color(0,0,0)
    COLOR_BTN_BG=hex_color(210,210,210)
    COLOR_BTN_FG=hex_color(0,0,0)
    COLOR_HELPMSG_BG=hex_color(220,220,220)
    COLOR_HELPMSG_FG=hex_color(20,20,20)

    th1=threading.Thread(target=importpackages, args=())
    th1.start()

##    dq=dqclass()
    login=loginclass() 
        



