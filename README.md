# fe
file editor, a very, very simple text editor for linux text mode displays

Current Status:

alpha quality, not usable

Goals:

This program is an extremely simple, minimalistic text editor in the 
spirit of WordStar(TM), University of Washington's PICO, Free Software 
Foundation's Gnu Nano, JOE, as well as newer editors like Typewriter, 
DarkCopy, WriteMonkey, etc.

 The screen is completely, pure black. No filename, no border, nothing.
 And no blinking cursor.

 Each file can only be 1000 lines long, no more.

 There is no 'saving' of files - each character you type is instantly
 written to the file you are editing.

The program is completely focused on the Linux Text-Mode Virtual 
Terminal, available on most linux machines by typing ctrl-alt-f3 or 
ctrl-alt-f4. It is not easily portable, and not designed to be run 
inside of a GUI windowing environment. It is intended somewhat to 
replicate the old look and feel of a PC or word processor from the 
1980s.

The code is intentionally kept simple. It is probably easier to fork 
the code and rewrite it yourself than it is to request a feature.

It is not intended for editing of computer programs, just simple text.

QA

Q - But what about all those other programs?

A - they don't work. how do you get rid of the borders or help bar in nano?
 i dont know. google doesn't know. does anyone know? the web based ones are..
 dependent on your browsers ability to go full screen. they also dont look
 right. textmode is textmode. it looks a certain way. also a lot of them 
 are only for windows. 

Q - But what about Windows port of this?

A - 0. Textmode on Windows seems to be unavailable or weird/hard to get to. 
       Not sure if it is even available in Win 7 or Win 8 or Win 10. 
    1. Browser based or program based, too easy to hit 'alt-tab'. 
    2. No, emulating text mode is not going to be good enough. see 1.

Q - Mac OSX?

A - Don't have access to a Mac.

Q - iphone, android?

A - Kind of defeats the purpose (being not-distracted)
    Also a good reason not to do GUI mode version (again, prevent distraction)

Q - But in linux i can just alt-tab back to X and use twitter or whatever

A - In linux you can also de-install X and a bunch of other programs and
    still have a usable machine. In theory you could unplug from the net
    and have this editor running in pure textmode. In practice the
    act of going alt-left-left-left and waiting for X to come back up
    is a nice barrier, alot more than 'alt-tab'. 




