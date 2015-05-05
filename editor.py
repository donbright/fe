# fe - file editor, a simple text editor
#
# copyright 2015 don bright, http://patreon.com/hugbright
#
# released under MIT license, open source
# 
# goals
# 0. no blinking cursor
# 1. completely blank screen other than text
# 2. only platform is textmode linux virtual console (ctrl-alt-f3) (or xterm)
#    with real local storage that can be mmaped (no network mounted stuff)
#    you must start from commandline. no provision for other startup modes
#    will not necessarily work under screen, ssh, etc. 
# 3. no "saving" of files, it auto-saves every character typed
#    there is no concept of 'saving over' a filename. u edit the file as is.
#    you can only open a filename by the command line on startup.
# 4. files can only be 1000 lines long
# 6. do not use any of the built in curses stuff, its confusing
# 7. keep this code very simple, so that if someone wants to add
#    a feature, or change something (how bkspc works) they can just fork this.
# 8. tell user how to exit on first run. allow to remove message easily.
# 9. store one backup copy of file on every open
# 10. not intended for coding. no syntax highlight, etc etc etc.
# 11. long lines dealt w like nano. but ideally screen s/b 80 columns
#
# bugs...
#
# currently conflated between screensize and file size
# what about long lines? line wrap? how to deal w variable screen size?
# 
# design...
# 
# big rectangle is the 'page' (or in curses world, the 'pad'), the whole file
# little dashed rectangle is 'screen', a 'window' that slides up and down 
# the 'pad'. the computer screen provides a sliding window view of the page.
# _________
# |       |
# |       |
# |_ _ _ _| 
# |       |
# |screen | 
# |- - - -| 
# |       |
# |_______|
#

import curses,sys,string,os,mmap,time

def clamp(clamprangelo,clamprangehi,inputvalue):
	if inputvalue<=clamprangelo: return clamprangelo
	if inputvalue>=clamprangehi: return clamprangehi
	return inputvalue

keycodes=[]
def mainwin(stdscr):
	global keycodes
	global mm
	stdscr.clear()
	h,w = stdscr.getmaxyx()
	#win = curses.newwin(25,80,0,0)
	psy,psx=1000,w # pad size
	pad = curses.newpad(psy,psx)
	done = False
	scy,scx=0,0  # position of physical cursor on physical screen
	pcy,pcx=0,0  # position of cursor within pad
	spy,spx=0,0  # position of screen within pad

	# create if non-existant
	if not os.path.isfile('delme'):
		f=open('delme','w+')
		f.write(' '*psy*psx)
		f.close()
	f = open('delme','r+b')
	f.flush()
	foriginalsize = os.stat('delme').st_size
	mm = mmap.mmap(f.fileno(), 0)
	mm.resize(psy*psx)

	# pad with ' ' if smaller than full size
	for i in range(foriginalsize,len(mm)): mm[i]=' '
	
	# load
	for i in range(0,psy-1):
		for j in range(0,psx):
			pad.addch(i,j,mm[psx*i+j])
	stdscr.refresh()
	pad.refresh(spy,spx,0,0,h-1,w-1)

	while not done:
		c = stdscr.getch()
		keycodes+=[c] # for finding integer codes for ctrl-a,enter,etc
		if c==24:
			done = True # ctrl - x
		elif c==10: # return aka enter aka linefeed
			pcy,pcx=pcy+1,0
			pcy=clamp(0,psy,pcy)
		elif c==14 or c==258: # ctrl-n, uparrow
			pcy,pcx=pcy+1,pcx
			pcy=clamp(0,psy,pcy)
		elif c==16 or c==259: # ctrl-p, dnarrow
			pcy,pcx=pcy-1,pcx
			pcy=clamp(0,psy,pcy)
		elif c==260: # lftarrow
			pcy,pcx=pcy,pcx-1
			pcx=clamp(0,psx,pcx)
		elif c==261: # rtarrow
			pcy,pcx=pcy,pcx+1
			pcx=clamp(0,psx,pcx)
		elif c==1 or c==curses.KEY_HOME: #ctrl-a
			pcx=0
		elif c==263: # bkspace
			pcx-=1
			pcx=clamp(0,psx-1,pcx)
			pad.addch(pcy,pcx,ord(' '))
			mm[pcy*psx+pcx]=' '
			pcx=clamp(0,psx,pcx)
		elif c==338: # pgdn
			spy,spx=spy+7,0
			spy=clamp(0,psy-h,spy)
		elif c==339: # pgup
			spy,spx=spy-7,0
			spy=clamp(0,psy-h,spy)
		else: # ordinary character
			if c<256:
				pcx=clamp(0,psx-1,pcx)
				pad.addch(pcy,pcx,c)
				mm[pcy*psx+pcx]=chr(c)
				pcx+=1
				pcx=clamp(0,psx,pcx)
		pad.refresh(spy,spx,0,0,h-1,w-1)
		scy,scx=pcy-spy,pcx-spx
		scy,scx=clamp(0,h-1,scy),clamp(0,w-1,scx)
		stdscr.move(scy,scx)
	mm.close()
	f.close()

#stdscr = setup()
errmsg = ''
try:
	curses.wrapper(mainwin)
finally:
	if '--debug' in string.join(sys.argv): print keycodes

#try:
#	mainwin()
#except Exception as e:
#	errmsg = str(e)
#finally: # reset terminal even if we crash, so keybd wont b messed up
#	quit( stdscr )
#	if errmsg: print 'error:',errmsg

#def quit(stdscr):
#	curses.noecho()
#	curses.nocbreak()
#	stdscr.keypad(0)
#	curses.echo()
#	curses.endwin()

#def setup():
#	stdscr = curses.initscr()
#	curses.cbreak()
#	stdscr.keypad(1)
#	return stdscr

