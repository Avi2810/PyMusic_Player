import os
import pickle
from tkinter import *
from tkinter import filedialog
from pygame import mixer


class Player:
    def __init__(self):
        mixer.init()
        if os.path.exists('songs.pickle'):
            with open('songs.pickle','rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist=[]

        self.current = 0
        self.paused = True
        self.played = False
        self.widgets()

    def widgets(self):

        self.canvas = Label(main, image=img,bg='#cccbbe')
        self.canvas.configure(width=120, height=120, bd = 0)
        self.canvas.place(x=5,y=5)

        self.songtrack = Label(main,bg='#cccbbe',fg="#52514e")
        self.songtrack['text'] = 'PyPlayer'
        self.songtrack.config(width=50, height=1)
        self.songtrack.place(x=15,y=130)

        self.loadSongs = Button(main, image=load,bd=0,bg='#cccbbe',activebackground='#cccbbe')
        self.loadSongs['text'] = 'Load Songs'
        self.loadSongs['command'] = self.retrieve_songs
        self.loadSongs.place(x=15,y=150)

        self.prev = Button(main, image=prev,bg='#cccbbe',bd=0,activebackground='#cccbbe')
        self.prev['command'] = self.prev_song
        self.prev.place(x=90,y=150)

        self.pause = Button(main, image=pause,bg='#cccbbe',bd=0,activebackground='#cccbbe')
        self.pause['command'] = self.pause_song
        self.pause.place(x=150,y=150)

        self.next = Button(main, image=next_,bg='#cccbbe',bd=0,activebackground='#cccbbe')
        self.next['command'] = self.next_song
        self.next.place(x=210,y=150)

        self.credit = Label(main,text='-by Abhishek',bg='#cccbbe')
        self.credit.place(x=330,y=195)

        self.volume = DoubleVar()
        self.slider = Scale(main, from_ = 0, to = 10, orient = HORIZONTAL,bg='#5ebfc4')
        self.slider['variable'] = self.volume
        self.slider.set(7)
        mixer.music.set_volume(0.7)
        self.slider['command'] = self.change_volume
        self.slider.place(x=295,y=155)


        self.tracklist = LabelFrame(main,bg='#cccbbe',bd=0,relief=GROOVE)
        self.tracklist.config(width=250,height=150)
        self.tracklist.place(x=150,y=5)

        self.scrollbar = Scrollbar(self.tracklist, orient=VERTICAL)
        self.scrollbar.grid(row=0,column=1,rowspan=2, sticky='ns')

        self.list = Listbox(self.tracklist,bg='#cccbbe', selectmode=SINGLE,yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
        self.enumerate_songs()
        self.list.config(height=7,width=38)
        self.list.bind('<Double-1>', self.play_song) 

        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0,column=0)



    def retrieve_songs(self):
        self.songlist = []
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
                for file in files:
                    if os.path.splitext(file)[1] == '.mp3':
                        path = (root_ + '/' + file).replace('\\','/')
                        self.songlist.append(path)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songlist, f)
        self.playlist = self.songlist
        self.list.delete(0, END)
        self.enumerate_songs()

    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))


    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg="#cccbbe")

        mixer.music.load(self.playlist[self.current])
        self.songtrack['anchor'] = 'w' 
        self.songtrack['text'] = os.path.basename(self.playlist[self.current])

        self.pause['image'] = play
        self.paused = False
        self.played = True
        self.list.activate(self.current) 
        self.list.itemconfigure(self.current, bg='sky blue')

        mixer.music.play()

    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause['image'] = pause
        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pause['image'] = play

    def prev_song(self):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current + 1, bg='#cccbbe')
        self.play_song()

    def next_song(self):
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current - 1, bg='#cccbbe')
        self.play_song()

    def change_volume(self, event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 10)








main = Tk()
main.title('PyPlayer')
main.geometry("410x213")
main.iconbitmap('images\\icon.ico')
main.resizable(0,0)
main.configure(bg='#cccbbe')

load = PhotoImage(file='images\\load.png')
img = PhotoImage(file='images\\music.png')
next_ = PhotoImage(file='images\\next.png')
prev = PhotoImage(file='images\\prev.png')
play = PhotoImage(file='images\\pause.png')
pause = PhotoImage(file='images\\play.png')

app = Player()

mainloop()