
import pprint
import curses
from curses import ascii
from curses.textpad import Textbox, rectangle
# content - array of lines (list)
mylines = ["Line {0} ".format(id)*3 for id in range(1, 11)]

pprint.pprint(mylines)


def main(stdscr):
    stdscr.clear()
    hlines = begin_y = begin_x = 5
    wcols = 10
    # calculate total content size
    padhlines = len(mylines)
    padwcols = 0
    for line in mylines:
        if len(line) > padwcols:
            padwcols = len(line)
    padhlines += 2
    padwcols += 2  # allow border

    for x in range(0, 10):
        for y in range(0, 10):
            stdscr.addstr(10+y, 10+x, f'{x*y}')
    # both newpad and subpad are <class '_curses.curses window'>:
    # mypadn = curses.newpad(padhlines, padwcols)
    mypads = stdscr.subpad(padhlines, padwcols, begin_y, begin_x+padwcols+4)
    # stdscr.addstr(str(type(mypads)) + "\n")
    # stdscr.addstr(str(type(mypadn))+" "+str(type(mypads)) + "\n")
    # mypadn.scrollok(1)
    # mypadn.idlok(1)
    mypads.scrollok(1)
    mypads.idlok(1)
    # mypadn.border(0)  # first ...
    # mypads.border(0)  # ... border
    for line in mylines:
        # mypadn.addstr(padhlines-1, 1, line)
        # mypadn.scroll(1)
        # mypads.addstr(0, 1, line)
        mypads.scroll(-1)
    # mypadn.border(0)  # second ...
    # mypads.border(0)  # ... border
    # refresh parent first, to render the texts on top
    #~ stdscr.refresh()
    # refresh the pads next
    # mypadn.refresh(0, 0, begin_y, begin_x, begin_y+hlines, begin_x+padwcols)
    mypads.refresh()
    mypads.touchwin()
    # mypadn.touchwin()
    stdscr.touchwin()  # no real effect here
    #stdscr.refresh() # not here! overwrites newpad!
    # mypadn.getch()
    # even THIS command erases newpad!
    # (unless stdscr.refresh() previously):
    # stdscr.getch()

    box = Textbox(stdscr)

    def ha(ch):
        if ch == curses.KEY_ENTER or ch == 10 or ch == 13:
            return ascii.ctrl(curses.KEY_EXIT)
        return ch
    # Let the user edit until Ctrl-G is struck.
    box.edit(ha)

    # Get resulting contents
    message = box.gather()
    print(message)

    tok =  message.strip().split(' ');
    print(tok)


curses.wrapper(main)
print('fish' + chr(13) + 'love')
