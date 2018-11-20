import curses
import curses.textpad
import CLI_Audio_Exception
import os

import sys

class FrontEnd:
    # the front end of the application that the user interacts with.
    # it allows for a menu and interacting with songs.
    
    # Attributes:
    # player - a player object that gets used to control where the song is playing, paused, etc

    def __init__(self, player):
        self.player = player
        #self.player.play(sys.argv[1])
        curses.wrapper(self.menu)

    def menu(self, args):
        """creates a menu for the player to interact with"""
        self.stdscr = curses.initscr()
        try:
            height, width = self.stdscr.getmaxyx()
            if (height < 20 or width < 100):
                raise CLI_Audio_Exception.CLI_Screen_Size_Exception
        except CLI_Audio_Exception.CLI_Screen_Size_Exception:
            sys.exit("Screen size too small")
            
        self.stdscr.border()
        self.stdscr.addstr(0,0, "cli-audio",curses.A_REVERSE)
        self.stdscr.addstr(5,10, "c - Change current song")
        self.stdscr.addstr(6,10, "p - Play/Pause")
        self.stdscr.addstr(7,10, "l - Library")
        self.stdscr.addstr(9,10, "ESC - Quit")
        self.updateSong()
        self.stdscr.refresh()
        
        # while the true boolean is true, the menu allows for
        # certain actions to be taken when the corresponding key is pressed. the first line in
        # the while loop pulls the value associated with ESC key: 27 is ESC in ascii
                
        while True:
            c = self.stdscr.getch()
            if c == 27:
                self.quit()
            elif c == ord('p'):
                self.player.pause()
            elif c == ord('c'):
                self.changeSong()
                self.updateSong()
                self.stdscr.touchwin()
                self.stdscr.refresh()
            elif c == ord('l'):
                songlist = self.player.list()
                x = 0
                for s in songlist:
                    self.stdscr.addstr(17 + x, 13, s)
                    x = x + 1
                    self.stdscr.refresh()
    
    def updateSong(self):
        # displays the new song on the menu
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())

    def changeSong(self):
        # asks for the user to input the file path and plays the song
        changeWindow = curses.newwin(5, 40, 5, 50)
        changeWindow.border()
        changeWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = changeWindow.getstr(1,1, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        self.player.stop()
        try:
            self.player.play(path.decode(encoding="utf-8"))
        except:
            self.stdscr.clrtoeol()
            print("File path does not exist.")
            self.stdscr.refresh()
        

    def quit(self):
        try:
            self.player.stop()
        except:
            sys.exit("No song was playing.")
        exit()
