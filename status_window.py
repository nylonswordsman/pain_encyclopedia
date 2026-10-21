## set up environment
import subprocess
from os import system
from sys import stdout
from json import load
from time import sleep
from pe_lib import clear_lines, clear_terminal, display_status


escRed = '\x1b[31m'     ## corresponds to 'STARTRED'
escBRed = '\x1b[1;31m'  ## corresponds to 'STARTBRED'
escHLRed = '\x1b[41m'   ## corresponds to 'STARTHLRED'
escGreen = '\x1b[32m'   ## corresponds to 'STARTGREEN'
escGold = '\x1b[33m'    ## corresponds to 'STARTGOLD'
escHLGold = '\x1b[43m'  ## corresponds to 'STARTHLGOLD'
#escBlue = '\x1b[1;34m'  ## corresponds to 'STARTBLUE'
escPurple = '\x1b[35m'  ## corresponds to 'STARTPURPLE'
escCyan = '\x1b[36m'    ## corresponds to 'STARTCYAN'
escGrey = '\x1b[37m'    ## corresponds to 'STARTGREY'
escEnd = '\x1b[m'       ## corresponds to 'ENDCOLOR'. stops current escape


currentSave = load(open("temp.json", "r"))


display_status()
input(escGrey + "     [Press enter to finish observation...]" + escEnd)
exit()