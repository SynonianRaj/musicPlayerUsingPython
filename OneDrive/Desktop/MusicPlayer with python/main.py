# Developed Buy Synonian (Ankit) Raj

"""
    music url sometimes not working because of bandwidth limit, in that case try another url.
    if You change something please mention, what have you done and what I did mistake..
    keep support

                    ....Synonian Raj....

"""

import json as js
import threading as thr
import vlc
import tkinter as tk
from tkinter.ttk import Progressbar

data = open('sanam.json')
json_data = js.load(data)
x = json_data['music']


class GUI(tk.Tk):

    def __init__(self):
        self.threading = thr
        self.player = vlc.MediaPlayer()
        self.temp = 0
        super().__init__()
        self.curr_time = 0
        self.dur = 0
        self.title('Music')
        self.iconbitmap('icon.ico')
        self.geometry('750x400')
        self.resizable(0, 0)
        self.frameMusic = tk.Frame(self, relief=tk.SUNKEN, background='red', height=400, width=500)
        self.frame = tk.Frame(self, relief=tk.SUNKEN, height=300, width=300)

        self.scroll = tk.Scrollbar(self.frame, relief=tk.SUNKEN)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self.frame, width=30, selectbackground='blue', font=("Helvetica", 10),
                                  yscrollcommand=self.scroll.set, relief=tk.SUNKEN,
                                  selectmode=tk.SINGLE, height=400)

        self.scroll['command'] = self.listbox.yview
        self.listbox.pack(side=tk.LEFT, padx=2, pady=5)

        self.frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.playingFrame = tk.LabelFrame(self.frameMusic, relief=tk.SUNKEN, labelanchor=tk.N, bd=1,
                                          width=480, height=230, text='Playing', font=("Helvetica", 15))

        self.playingFrame.grid(row=0, column=0, columnspan=2, sticky=tk.N, padx=5)
        self.playingFrame.grid_propagate(0)
        self.playingFrame.rowconfigure(0, weight=1)
        self.titleLabel = tk.Label(self.playingFrame, text='Title : ', font=("Helvetica", 10))
        self.artistLabel = tk.Label(self.playingFrame, text='Artist : ', font=("Helvetica", 10))
        self.statusLabel = tk.Label(self.playingFrame, text='Status : ', font=("Helvetica", 10))
        self.title = tk.Label(self.playingFrame, justify=tk.LEFT, text='Song title goes here ', font=("Helvetica", 10))
        self.artist = tk.Label(self.playingFrame, justify=tk.LEFT, text='artist name goes here ',
                               font=("Helvetica", 10))
        self.status = tk.Label(self.playingFrame, justify='left', text='Song is not loaded', font=("Helvetica", 10))

        self.ControlFrame = tk.Frame(self.frameMusic, relief=tk.SUNKEN, bd=1, width=480, height=160)
        self.ControlFrame.grid(row=1, column=0, columnspan=2, sticky=tk.S, pady=5)
        self.ControlFrame.grid_propagate(0)

        self.ControlFrame.rowconfigure(0, weight=1)

        self.ControlFrame.rowconfigure(2, weight=1)

        self.frameMusic.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        # Image initialization
        self.prevImg = tk.PhotoImage(file='previous.png')
        self.playImg = tk.PhotoImage(file='play.png')
        self.stopImg = tk.PhotoImage(file='stop.png')
        self.nextImg = tk.PhotoImage(file='next.png')
        self.pauseImg = tk.PhotoImage(file='pause.png')

        # ProgressBar Init

        self.progressBar = Progressbar(self.ControlFrame, orient=tk.HORIZONTAL, length=450, mode='determinate')
        self.curr_dur = tk.Label(self.ControlFrame, text="00:00", relief=tk.FLAT, font=("Helvetica", 10))
        self.total_dur = tk.Label(self.ControlFrame, text="00:00", relief=tk.FLAT, font=("Helvetica", 10))

        # Button initialization
        self.prevBtn = tk.Button(self.ControlFrame, relief=tk.FLAT, image=self.prevImg, state='disabled',
                                 command=self.seekPrev,
                                 text='Prev')
        self.playBtn = tk.Button(self.ControlFrame, relief=tk.FLAT, image=self.pauseImg, state='disabled',
                                 command=self.play_pause, text='Play')
        self.nextBtn = tk.Button(self.ControlFrame, relief=tk.FLAT, image=self.nextImg, state='disabled',
                                 command=self.seekNext, text='Next')
        self.stopBtn = tk.Button(self.ControlFrame, relief=tk.FLAT, image=self.stopImg, state='disabled',
                                 command=self.stop,
                                 text='Stop')
        self.curr_dur.grid(row=1, column=0, pady=0)
        self.total_dur.grid(row=1, column=4, pady=0)
        self.progressBar.grid(row=2, column=0, columnspan=5, padx=15)
        self.prevBtn.grid(row=3, column=1, pady=15)
        self.playBtn.grid(row=3, column=2, pady=15)
        self.nextBtn.grid(row=3, column=3, pady=15)
        self.stopBtn.grid(row=3, column=4, pady=15)

        self.titleLabel.grid(row=1, column=0, )
        self.title.grid(row=1, column=1, )

        self.artistLabel.grid(row=2, column=0)
        self.artist.grid(row=2, column=1)

        self.statusLabel.grid(row=3, column=0, rowspan=3)
        self.status.grid(row=3, column=1, rowspan=3)

    def play(self, url):
        self.status['text'] = 'Wait While Loading...'
        try:
            print('Wait While Loading')
            media = vlc.Media(url)
            self.player.set_media(media)
            self.player.play()
            print('playing')
            self.threading.Thread(target=self.duration).start()
        except Exception as e:
            self.status['text'] = "Error: " + str(e)
            print(e)

    def play_pause(self):
        if self.player.is_playing():
            self.player.pause()
            self.playBtn['image'] = self.playImg
            self.status['text'] = 'Paused...'
        else:
            self.player.play()
            self.playBtn['image'] = self.pauseImg
            self.status['text'] = 'Playing...'

    def stop(self):
        self.status['text'] = 'Stopped...'
        self.playBtn['image'] = self.playImg
        return self.player.stop()

    def duration(self):
        while True:
            if self.player.is_playing():
                self.status['text'] = 'Playing...'
                self.dur = self.player.get_length()
                print(self.dur)
                self.progressBar['maximum'] = self.dur
                break
        durInMin, durInSec = hrs(self.dur)
        self.total_dur['text'] = '%02i:%02i' % (durInMin, durInSec)
        print('%02i:%02i' % (durInMin, durInSec))
        while True:
            curr_state = self.player.get_state()
            if curr_state == vlc.State(3):
                print(curr_state)
                self.curr_time = self.player.get_time()
                Min, Sec = hrs(self.curr_time)
                self.curr_dur['text'] = '%02i:%02i' % (Min, Sec)
                self.progressBar['value'] = self.curr_time
                self.update_idletasks()
            elif curr_state == vlc.State(5):
                self.curr_dur['text'] = '00:00'
                self.total_dur['text'] = '00:00'
                self.progressBar['value'] = 0
                self.update_idletasks()
                print(curr_state)
                break
            elif curr_state == vlc.State(6):
                self.curr_dur['text'] = '00:00'
                self.total_dur['text'] = '00:00'
                self.progressBar['value'] = 0
                self.update_idletasks()
                self.status['text'] = " Music Completed"
                self.playBtn['image'] = self.playImg
                self.temp = self.temp + 1
                u = x[self.temp]['url']
                self.play(u)
                self.playBtn['image'] = self.pauseImg
                self.listbox.selection_clear(self.temp - 1)
                self.listbox.select_set(self.temp)
                self.listbox.activate(self.temp)
                self.title['text'] = x[self.temp]['title']
                self.artist['text'] = x[self.temp]['artist']

                break

    # seek 10sec forward
    def seekPrev(self):
        if self.curr_time > 11000:
            self.player.set_time(self.curr_time - 10000)

        else:
            print('duration is less!')

    # seek 10sec backward
    def seekNext(self):
        if self.curr_time < self.dur:
            self.player.set_time(self.curr_time + 10000)
        else:
            print('Music is completed')


app = GUI()

for i in range(len(x)):
    # print(i,x[i]['title'])
    app.listbox.insert(i, x[i]['title'])


def hrs(dur):
    durInSec = (dur / 1000) % 60
    durInMin = (dur / 1000) / 60
    return durInMin, durInSec


def listboxSelectCommand(event):
    j = app.listbox.curselection()[0]
    print(j)
    app.temp = j
    url = x[j]['url']
    app.play(url)
    app.title['text'] = x[j]['title']
    app.artist['text'] = x[j]['artist']
    app.playBtn['state'] = 'normal'
    app.playBtn['image'] = app.pauseImg
    app.stopBtn['state'] = 'normal'
    app.prevBtn['state'] = 'normal'
    app.nextBtn['state'] = 'normal'


app.listbox.bind('<<ListboxSelect>>', listboxSelectCommand)

app.mainloop()
app.player.stop()
