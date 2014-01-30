from tkinter import *
from tkinter import filedialog
import snapshot
import pickle

class SaveSyncGui():
    def __init__(self):
        root = self.root = Tk()
        Label(root, text="Save Game Synch").pack()
        self.frame = Frame(root)
        self.frame2 = Frame(root)
        self.listbox1 = Listbox(self.frame)
        self.listbox2 = Listbox(self.frame)
        self.addbutton = Button(self.frame2, text="Add folder pair", command=self.add_folder_pair)
        self.syncbutton = Button(self.frame2, text="Sync Folders", command=self.sync_folders)
        self.listbox1.pack(side=LEFT, fill=BOTH, expand=YES)
        self.listbox2.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.frame.pack(fill=BOTH, expand=YES)
        self.addbutton.pack(side=LEFT)
        self.syncbutton.pack(side=RIGHT)
        self.frame2.pack(side=BOTTOM)
        self.makemenu()
        self.root.config(menu=self.menubar)
        self.folders = []
    def add_folder_pair(self):
        folder1 = filedialog.askdirectory()
        folder2 = filedialog.askdirectory()
        self.listbox1.insert(END ,folder1)
        self.listbox2.insert(END, folder2)
        self.root.update()
        self.folders.append([folder1, folder2])
    def sync_folders(self):
        for pairs in self.folders:
            snap1 = snapshot.snapshot()
            snap1.add_dir(pairs[0])
            snap2 = snapshot.snapshot()
            snap2.add_dir(pairs[1])
            snapshot.sync(snap1, snap2)
    def makemenu(self):
        self.menubar = Menu(self.root)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Save pairs", command=self.save)
        filemenu.add_command(label="Load pairs", command=self.load)
        self.menubar.add_cascade(label="File", menu=filemenu)
    
    def save(self):
        file = filedialog.asksaveasfilename()
        if file:
            file=open(file, 'wb')
            pickle.dump(self.folders, file)
            file.close()
    def load(self):
        self.folders = []
        self.listbox1.delete(0, END)
        self.listbox2.delete(0, END)
        file = filedialog.askopenfile('rb')
        self.folders = pickle.load(file)
        file.close()
        if self.folders:
            for pair in self.folders:
                self.listbox1.insert(END ,pair[0])
                self.listbox2.insert(END, pair[1])
                
    def start_gui(self):
        self.root.mainloop()

if __name__=="__main__":
    window = SaveSyncGui()
    window.start_gui()