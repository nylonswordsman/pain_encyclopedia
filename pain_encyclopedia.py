## import parts of modules that will be used, instead of porting the entire modules like a CHUMP /lighthearted
## i discovered `from module import function` while googling for a way to import specific modules because i was looking through IDLE's stack trace and noticed that there were a lot of functions from modules i wasnt using and i thought that was sloppy. made it harder to find what i wanted to look for
import subprocess
from math import floor
from os import system, path ## vscode says os.system is deprecated but it still works so i dont care lel
from sys import stdout
from time import sleep
from json import load, dump
from pe_lib import clamp, clear_lines, clear_terminal
from random import randint, choice ## with how many duplicate events i keep rolling i am THIS close to writing my own randomizer functions


#os.environ['SDL_AUDIODRIVER'] = 'dsp' # might be used to add music at some point but im ngl i dont think thats necessary


## these are ANSI escape codes. when the're read in a string they tell the terminal to ignore them and start applying a certain modification to the text after them instead of printing like normal
## these ones are for color. im going to use them to make the text all pretty instead of boring black and white
## the variables won't be actually used for code but as shorthand to make my time enprettifying everything easier
## START{color} (like STARTRED or STARTGOLD) place an escape code.these codes will cause the text ahead of them to be written in that color.
## ENDCOLOR will "stop" the currently happening escape caused by a color code, reverting text ahead of it to default. use them like opening and closing parenthesis to make certain sections of lines have color.
## example: print(unwrap("I am STARTGOLDnot a human beingENDCOLOR!")) prints the 'not a human being' part in gold but still prints the exclamation mark in normal black.

escRed = '\x1b[31m'     ## corresponds to 'STARTRED'
#escBRed = '\x1b[1;31m'  ## corresponds to 'STARTBRED'
escHLRed = '\x1b[41m'   ## corresponds to 'STARTHLRED'
escGreen = '\x1b[32m'   ## corresponds to 'STARTGREEN'
escGold = '\x1b[33m'    ## corresponds to 'STARTGOLD'
escHLGold = '\x1b[43m'  ## corresponds to 'STARTHLGOLD'
escBlue = '\x1b[1;34m'  ## corresponds to 'STARTBLUE'
escPurple = '\x1b[35m'  ## corresponds to 'STARTPURPLE'
escCyan = '\x1b[1;36m'  ## corresponds to 'STARTCYAN'
escGrey = '\x1b[37m'    ## corresponds to 'STARTGREY'
escEnd = '\x1b[m'       ## corresponds to 'ENDCOLOR'. stops current escape

## "unwrap" the escape codes by replacing the written codes (like STARTBLUE or ENDCOLOR) with their ANSI escape code counterparts
def unwrap(wrappedString):
    wrappedString = wrappedString.replace("STARTRED", escRed)
#    wrappedString = wrappedString.replace("STARTBRED", escBRed)
    wrappedString = wrappedString.replace("STARTHLRED", escHLRed)
    wrappedString = wrappedString.replace("STARTGREEN", escGreen)
    wrappedString = wrappedString.replace("STARTGOLD", escGold)
    wrappedString = wrappedString.replace("STARTHLGOLD", escHLGold)
    wrappedString = wrappedString.replace("STARTBLUE", escBlue)
    wrappedString = wrappedString.replace("STARTPURPLE", escPurple)
    wrappedString = wrappedString.replace("STARTCYAN", escCyan)
    wrappedString = wrappedString.replace("STARTGREY", escGrey)
    wrappedString = wrappedString.replace("ENDCOLOR", escEnd)
    wrappedString = wrappedString.replace("MAKESOUND", "\a")
    wrappedString = wrappedString.replace("NEWLINE", "\n")
    return wrappedString


currentSave = {}

eventPool = {}

eventQueue = []


def open_status_window():
    print(escGrey + "[Finish observing specimen status to continue.]" + escEnd)
    subprocess.run(["python", "status_window.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    clear_lines(1)


def open_work_window():
    global currentSave
    print(escGrey + "[Finish assigning specimen work to continue.]" + escEnd)
    subprocess.run(["python", "work_window.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    currentSave = dict(load(open("memnode.json", "r")))
    clear_lines(1)
    system(f"title {currentSave["difficulty"]} - Cycle {str(currentSave["cycleCount"])} - {str(currentSave["energyCurrent"])}/{str(currentSave["energyGoal"])}u")


def main():
#    stdout.write("\1xb[8;35;96t") ## is SUPPOSED TO change the terminal size but it DOESNT WORK
    clear_terminal()
    i = 1
    print(escEnd + escGrey +"╔════════════════════════════════════════════════════════════════════════════════════════════╗")
    for i in range(11): print("║                                                                                            ║")
    print("║                     " + escBlue + "[Please adjust the window size and/or scroll until]" + escEnd + escGrey + "                    ║")
    print("║                " + escBlue + "[the rectangle is roughly aligned with the terminal's edges.]" + escEnd + escGrey + "               ║")
    print("║                              " + "[Press enter when you are done...]" + "                            ║")
    for i in range(14): print("║                                                                                            ║")
    input("╚════════════════════════════════════════════════════════════════════════════════════════════╝")
    clear_terminal()
    system("title Awaiting Memory Synchronization...")
    main_menu()


def main_menu():
    global currentSave
    global eventPool
    eventPool = load(open("events.json", "r")) ## load event pool
    ## check whether or not the save file exists
    if path.exists("./memnode.json") == True:
        ## if it does exist and program picks it up, yay. move on
        print(escRed + "[HNos] Welcome Unit 1.\n[HNos] Memory node found. Please commence memory synchronization.\n[HNos] To abandon this memory node, please manually remove it and restart.")
        input(escGrey + "[Press enter to continue...]" + escRed)
        clear_lines(1)
        currentSave = dict(load(open("./memnode.json"))) ## load the save
        dump(currentSave, open("temp.json", "w"))
    else: ## if the save file does not exist, make one
        print(escRed + "[HNos] Welcome Unit 1.\n[HNos] Memory node not found. Please pull specimens from cryptosleep and create a memory node.")
        input(escGrey + "[Press enter to continue...]" + escRed)
        clear_lines(1)
        new_game()
        currentSave = dict(load(open("./memnode.json"))) ## load the save
        dump(currentSave, open("temp.json", "w"))
    ## flavor text with pauses for dramatic effect
    print(escRed + "[HNos] Beginning memory synchronization...")
    print("[HNos] Activating psychic absorption apparatus...")
    sleep(.4)
    print("[HNos] Reconnecting specimen brainchips...")
    sleep(.6)
    print("[HNos] Waking specimens from cryptosleep...")
    sleep(.3)
    print("[HNos] Resuming specimen biocontinuity...")
    sleep(.4)
    print("[HNos] Resharpening specimen psychic tracts...")
    sleep(.5)
    print("[HNos] Rebooting administrative equipment...")
    sleep(.6)
    print("[HNos] Memory synchronization complete.")
    sleep(1)
    cycle()


def new_game():
    print("[HNos] Creating new memory node...")
    sleep(0.2)
    print("[HNos] Please select a difficulty... ")
    print("[1.] LENIENT | 150u. For those who seek to practice.")
    print("[2.] HARSH   | 250u. For those who seek to play.")
    print("[3.] CRUEL   | 300u. For those who seek a reward.")
    goal = int
    while True:
        try:
            goal = int(input(""))
            if goal in [1, 2, 3]: break
            else: raise ValueError
        except ValueError, TypeError:
            clear_lines(1)
            continue
    clear_lines(5)
    print("[HNos] Determining energy required... ")
    newSave = {
    "cycleCount": 0,
    "energyCurrent": 0,
    "energyGoal": 0,
    "specimens": [],
    "flags": [],
    "difficulty": ""
    }
    print("[HNos] Pull how many specimens...? ")
    while True:
        try:
            pullAmount = int(input())
            if pullAmount in [1, 2, 3, 4, 5, 6, 7, 8, 9]: break
            else: raise ValueError
        except ValueError, TypeError:
            clear_lines(1)
            continue
    counter = 0
    for i in range(pullAmount):
        if counter == 0:
            clear_lines(1)
            print("[HNos] Awakening specimens from cryptosleep...")
        newSave["specimens"].append(generate_specimen())
        counter += 1
    if goal == 1:
        newSave["difficulty"] = "LENIENT"
        newSave["energyGoal"] = 150
        print("[HNos] Handler subroutine influence heightened.")
    elif goal == 2 and len(newSave["specimens"]) <= 6:
        newSave["difficulty"] = "HARSH"
        newSave["energyGoal"] = 250
        print("[HNos] Handler subroutine influence normal.")
    elif goal == 3 and len(newSave["specimens"]) <= 6:
        newSave["difficulty"] = "CRUEL"
        newSave["energyGoal"] = 300
        print("[HNos] Handler subroutine influence disabled. Fortune is cruel.")
    else:
        newSave["difficulty"] = "LENIENT"
        newSave["energyGoal"] = 200
        print("[HNos] Handler subroutine influence heightened.")
    if path.exists("./memnode.json"): dump(newSave, open("./memnode.json", "w"))
    else: dump(newSave, open("./memnode.json", "x"))
    print("[HNos] Memory node created.")


def generate_specimen():
    data = load(open("data.json", "r"))
    s = {} ## create empty dictionary; this is the specimen
    ## generate and add to the specimen an ID composed of a letter and 4 numbers
    randomLetter = choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    s.update({"ID": str(randomLetter + "-" + str(randint(0,9))) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9))})
    print("[HNos] Acceptable specimen found. Establishing connection and pulling specimen " + s["ID"] + " from cryptosleep reserves.")
    ## add stats
    s.update([["combat", 1], ["medical", 1], ["social", 1], ["mechanical", 1], ["psychic", 1]])
    ## add fur pattern, sex, and name
    s.update({"fur": choice(["D.BRWN", "N.BRWN", "L.BRWN", "D.GREY", "N.GREY", "L.GREY", "P.BLCK", "P.WHIT"])})
    s.update({"sex": "M"}) if randint(0,1) == 0 else s.update({"sex": "F"}) ## i dont know how i feel about shorthand if tbh. i think just condensing the individual statements to one line is nice but combining them uses weird syntax like this and i dont know if i like it
    s.update({"name": choice(data[0])}) if s["sex"] == "M" else s.update({"name": choice(data[1])})
    print("[" + s["ID"] + "] Physiological scanning for disposition...")
    ## pick a class at random and fill in that class' name, weight and alignment
    primaryClass = choice(data[2])
    s.update([["class", primaryClass["title"]], ["weight", primaryClass["weight"]], ["alignment", primaryClass["alignment"]]])
    match primaryClass["weight"]:
        case "Light":
            s.update({"healthMax": randint(11,12)})
            s["medical"] += 1
            s["social"] += 2
            s["mechanical"] += 1
            s["psychic"] += 2
        case "Medm.":
            s.update({"healthMax": randint(13,15)})
            s["combat"] += 1
            s["medical"] += 2
            s["mechanical"] += 2
            s["psychic"] += 1
        case "Heavy":
            s.update({"healthMax": randint(15,17)})
            s["combat"] += 2
            s["social"] += 1
            s["psychic"] += 1
    match primaryClass["alignment"]:
        case "Arcane":
            s.update({"mood": randint(70,80)})
            s["medical"] += 1
            s["mechanical"] += 1
            s["psychic"] += 1
        case "Divine":
            s.update({"mood": randint(80,90)})
            s["medical"] += 1
            s["social"] += 1
            s["mechanical"] += 1
        case "Occult":
            s.update({"mood": randint(60,70)})
            s["social"] += 1
            s["mechanical"] += 1
            s["psychic"] += 1
        case "Primal":
            s.update({"mood": randint(60,90)})
            s["medical"] += 1
            s["social"] += 1
            s["psychic"] += 1
    sleep(.8)
    print("[" + s["ID"] + "] Found specimen's disposition: " + str(s["weight"].upper() + "/" + str(s["alignment"].upper())))
    print("[" + s["ID"] + "] Neural scanning for class...")
    for skill in ["combat", "medical", "social", "mechanical", "psychic"]: s[skill] += primaryClass[skill]
    sleep(.7)
    print("[" + s["ID"] + "] Found specimen's primary class: " + str(s["class"].upper()))
    ## determine secondary class completely randomly because i havent made it select a secondary class properly
    secondaryClass = choice(data[2])
    s.update({"secondaryClass": secondaryClass["title"]})
    for skill in ["combat", "medical", "social", "mechanical", "psychic"]: s[skill] += primaryClass[skill]
    match secondaryClass["weight"]:
        case "Light": s["healthMax"] += randint(-2, -1)
        case "Medm.": s["healthMax"] += randint(-1, 1)
        case "Heavy": s["healthMax"] += randint(1, 2)
    s["healthMax"] = clamp(9, s["healthMax"], 18)
    s.update({"health": s["healthMax"]})
    sleep(.4)
    print("[" + s["ID"] + "] Found specimen's secondary class: " + str(s["secondaryClass"].upper()))
    sleep(.7)
    print("[" + s["ID"] + "] Specimen has been awoken from cryptosleep. Be mindful of cryptosleep sickness.")
    ## clamp all the skills to make sure none of them are negative or over 9
    for skill in ["combat", "medical", "social", "mechanical", "psychic"]: s[skill] = clamp(0, s[skill], 9)
    ## add health, pain, mentalDmg and worksLeft fields. health starts equal to healthMax because obviously they cant start at 0 or they die immediately
    s.update([["health", s["healthMax"]], ["pain", 0], ["mentalDmg", 0], ["worksLeft", 0]])
    return s


def cycle():
    global currentSave
    global eventPool
    global eventQueue
    cS = currentSave
    print(f"{cS["difficulty"]} - Cycle {str(cS["cycleCount"])}")
    ## TODO: make this a bar. maybe
    print(f"Energy: {str(cS["energyCurrent"])}/{str(cS["energyGoal"])}u")
    system(f"title {cS["difficulty"]} - Cycle {str(cS["cycleCount"])} - {str(cS["energyCurrent"])}/{str(cS["energyGoal"])}u")
    for s in cS["specimens"]: ## 's' stands for specimen, 'cS' stands for currentSave
        s["pain"] = clamp(0, s["pain"]-randint(4,8), 100)
        s["worksLeft"] = 4
        ## print out physical status
        print(escRed + "[" + s["ID"] + "] Physical status: " + escGrey + "QUERYING" + escRed)
        sleep(0.14)
        clear_lines(1)
        if s["health"] <= 0:
            print(escRed + "[" + s["ID"] + "] Physical status: " + escGrey + "DECEASED" + escRed)
            cS["specimens"].remove(s)
        elif s["health"] < round(s["healthMax"]*0.20): print("[" + s["ID"] + "] Physical status: " + escEnd + escHLRed + " WARNING " + escEnd + escRed)
        elif s["health"] < round(s["healthMax"]*0.40): print("[" + s["ID"] + "] Physical status: " + escGold + "BAD" + escRed)
        elif s["health"] < round(s["healthMax"]*0.60): print("[" + s["ID"] + "] Physical status: " + escRed + "POOR" + escRed)
        elif s["health"] < round(s["healthMax"]*0.80): print("[" + s["ID"] + "] Physical status: " + escGreen + "OK" + escRed)
        elif s["health"] <= round(s["healthMax"]*1.00):
            print("[" + s["ID"] + "] Physical status: " + escGreen + "GOOD" + escRed)
            s["mood"] = clamp(0, s["mood"]+randint(4,8), 100) ## specimens slightly recover mood if above 80% health
        ## (non-Scavenger) specimens fear death/chronic injury and lose mood if below 50% health
        if s["health"] < round(s["healthMax"]*0.50) and s["class"] == "Scavenger": s["mood"] = clamp(0, s["mood"]+randint(-6,-4), 100)
        ## specimens dislike ouchies and lose mood scaling with pain if at or above 20 pain
        if s["pain"] >= 20: s["mood"] = clamp(0, s["mood"]+round((s["pain"]/4)*-1), 100)
        ## specimens recover pain faster when above 40% health
        if s["health"] >= round(s["healthMax"]*0.40): s["pain"] = clamp(0, s["pain"]+randint(-9,-7), 100)
        else: s["pain"] = clamp(0, s["pain"]+randint(-6,-4), 100)
        ## the lower mood is (in increments of 20), the more likely they are to have a mental fracture
        ## whenever a specimen that has already had 2 mental fractures would have another, it has a mental break instead 
        print(escRed + "[" + s["ID"] + "] Mental status: " + escGrey + "QUERYING" + escRed)
        sleep(0.14)
        clear_lines(1)
        if s["mood"] < 20:
            print(escRed + "[" + s["ID"] + "] Mental status: " + escEnd + escHLRed + " WARNING " + escEnd + escRed)
            if randint(1, 100) <= 80 and s["pain"] >= 85:
                induce_event(0, cS["specimens"].index(s))
        elif s["mood"] < 40:
            print(escRed + "[" + s["ID"] + "] Mental status: " + escGold + "BAD" + escRed)
            if randint(1, 100) <= 50 and s["pain"] >= 85:
                induce_event(0, cS["specimens"].index(s))
        elif s["mood"] < 60:
            print(escRed + "[" + s["ID"] + "] Mental status: " + escRed + "POOR" + escRed)
            if randint(1, 100) <= 20 and s["pain"] >= 85:
                induce_event(0, cS["specimens"].index(s))
        elif s["mood"] < 80:
            print(escRed + "[" + s["ID"] + "] Mental status: " + escGreen + "OK" + escRed)
        elif s["mood"] <= 100:
            print(escRed + "[" + s["ID"] + "] Mental status: " + escGreen + "GOOD" + escRed)
    for s in cS["specimens"]: ## specimens lose work ability if they are pained, depressed or injured enough at the beginning of the cycle
        if s["pain"] >= 85:
            s["worksLeft"] += -4
            print(escRed + "[" + s["ID"] + "] Specimen work ability compromised - unconscious due to pain." + escRed)
        elif s["pain"] >= 50 and s["worksLeft"] > 0:
            s["worksLeft"] += -1
            print(escRed + "[" + s["ID"] + "] Specimen work ability reduced - excessive pain." + escRed)
        if s["health"] < round(s["healthMax"]*0.20) and s["worksLeft"] > 0:
            s["worksLeft"] += -1
            print(escRed + "[" + s["ID"] + "] Specimen work ability heavily reduced - extremely poor physical condition." + escRed)
        elif s["health"] < round(s["healthMax"]*0.50) and s["worksLeft"] > 0:
            s["worksLeft"] += -2
            print(escRed + "[" + s["ID"] + "] Specimen work ability reduced - poor physical condition." + escRed)
        if s["mood"] < 33 and s["worksLeft"] > 0:
            s["worksLeft"] += -1
            print(escRed + "[" + s["ID"] + "] Specimen work ability reduced - poor mood." + escRed)
    print("[HNos] Rousing specimens from standard sleep...")
    sleep(.15)
    print("[HNos] Reinitializing facility equipment...")
    ## induce events; one per specimen and some extras based on difficulty because Suffer.
    for s in cS["specimens"]: induce_event(None, cS["specimens"].index(s))
    match cS["difficulty"]:
        case "LENIENT":
            for i in range(int(floor(cS["cycleCount"]/11))): induce_event(None, None)
        case "HARSH":
            for i in range(int(floor(cS["cycleCount"]/9))): induce_event(None, None)
        case "CRUEL":
            for i in range(int(floor(cS["cycleCount"]/7))): induce_event(None, None)        
    ## check what cycle it is; on some cycles there are scripted events. usually story stuff
    ## also checks energy count for 
    match cS["cycleCount"]:
        case 0:
            ## replace entire event queue with cycle 0 story event and stop specimens from working; this is basically a cutscene
            eventQueue = []
            for s in cS["specimens"]: s["worksLeft"] = 0
            eventQueue.append(eventPool[7][0])
        case 10: eventQueue.append(eventPool[7][1])
        case 20:
            eventQueue = [] ## clear event queue
            for s in cS["specimens"]: s["worksLeft"] = 0
            if cS["energyCurrent"] >= round(cS["energyGoal"]*1.00): ## if energy quota is met:
                if cS["difficulty"] == "LENIENT": eventQueue.append(eventPool[7][10]) ## disintegration loop
                elif cS["difficulty"] == "HARSH": eventQueue.append(eventPool[7][8])  ## good ending
                elif cS["difficulty"] == "CRUEL": eventQueue.append(eventPool[7][9])  ## good ending (can continue)
            else: ## if energy quota not met:
                if cS["difficulty"] == "LENIENT": eventQueue.append(eventPool[7][10]) ## disintegration loop
                elif cS["difficulty"] == "HARSH": eventQueue.append(eventPool[7][10]) ## disintegration loop
                elif cS["difficulty"] == "CRUEL": eventQueue.append(eventPool[7][11]) ## disintegration loop but you can continue
        case 21:
            for i in range(2): induce_event(None, None)
        case 22:
            for i in range(3): induce_event(None, None)
        case 23:
            for i in range(3): induce_event(None, None)
        case 24:
            for i in range(4): induce_event(None, None)
        case 25:
            eventQueue = [] ## clear event queue
            for s in cS["specimens"]: s["worksLeft"] = 0
            if cS["energyCurrent"] >= round(cS["energyGoal"]*1.00): eventQueue.append(eventPool[7][12]) ## true ending
            else: eventQueue.append(eventPool[7][10]) ## disintegration loop
        case _:
            pass
    if cS["energyCurrent"] >= round(cS["energyGoal"]*1.00) and "100%" not in cS["flags"]:
        eventQueue.append(eventPool[7][6])
        eventQueue.append(eventPool[7][7])
    elif cS["energyCurrent"] >= round(cS["energyGoal"]*0.90) and "90%" not in cS["flags"]: eventQueue.append(eventPool[7][5])
    elif cS["energyCurrent"] >= round(cS["energyGoal"]*0.75) and "75%" not in cS["flags"]: eventQueue.append(eventPool[7][4])
    elif cS["energyCurrent"] >= round(cS["energyGoal"]*0.50) and "50%" not in cS["flags"]: eventQueue.append(eventPool[7][3])
    elif cS["energyCurrent"] >= round(cS["energyGoal"]*0.25) and "25%" not in cS["flags"]: eventQueue.append(eventPool[7][2])
    dump(currentSave, open("temp.json", "w")) ## dump save to temp
    ## begin next cycle
    print("[HNos] Beginning cycle.")
    event_phase()


def induce_event(category, targetIndex):
    global currentSave
    global eventQueue
    global eventPool
    if category == None: category = randint(2,6) ## if no category is specified, roll a random one between categories 2 and 6
    ## if the mental fracture category is specified, roll from the mental fractures
    elif category == 0:
        if targetIndex == None: ## and no target was specified,
            targetIndex = randint(0, len(currentSave["specimens"])-1) ## pick a specimen at random to target
        if currentSave["specimens"][targetIndex]["mentalDmg"] >= 2: category = 1 ## if the target's mentalDmg is 2 or higher, roll from mental breaks instead
    ## draw an event of the specified category from event pool
    eventToCheck = choice(eventPool[category])
    if eventToCheck["targeted"] == False: eventToAppend = eventToCheck ## if the event is untargeted/facility-wide, do nothing with the target index
    else: ## if the event is targeted,
        if targetIndex == None: ## and no target was specified,
            targetIndex = randint(0, len(currentSave["specimens"])-1) ## pick a specimen at random to target,
            eventToCheck.update({"target": targetIndex})
            eventToAppend = eventToCheck ## and append the target's index with the event so it knows what it's targeting
        else: ## if the event is targeted and a target was specified,
            eventToCheck.update({"target": targetIndex})
            eventToAppend = eventToCheck ## append the event and the target's index
    ## check certain events to reduce (but not eliminate) the odds that you get a useless event
    ## reroll target once if the target of Weaveskin Nanite Infection already has 40 max health
    if eventToCheck == eventPool[5][1] and currentSave["specimens"][eventToCheck["target"]]["healthMax"] == 40:
        targetIndex = randint(0, len(currentSave["specimens"])-1)
        eventToCheck.update({"target": targetIndex})
    ## reroll target once if the target of Claw Enhancement Nanite Infection already has 9 combat
    if eventToCheck == eventPool[5][0] and currentSave["specimens"][eventToCheck["target"]]["combat"] == 9:
        targetIndex = randint(0, len(currentSave["specimens"])-1)
        eventToCheck.update({"target": targetIndex})
    ## reroll target once if the target of Behavior Adjustment Nanite Infection already has 9 social
    if eventToCheck == eventPool[5][4] and currentSave["specimens"][eventToCheck["target"]]["social"] == 9:
        targetIndex = randint(0, len(currentSave["specimens"])-1)
        eventToCheck.update({"target": targetIndex})
    ## reroll target once if the target of Albinism Nanite Infection already has white fur
    if eventToCheck == eventPool[5][6] and currentSave["specimens"][eventToCheck["target"]]["fur"] == "P.WHIT":
        targetIndex = randint(0, len(currentSave["specimens"])-1)
        eventToCheck.update({"target": targetIndex})
    eventQueue.append(eventToAppend)


def event_phase():
    global eventQueue
    global currentSave
#    print(eventQueue) #remove before flight
    while eventQueue != []: ## for the number of events rather than for each event,
        i = 0
        print(escRed + "╔═════════════════════════════════════════╣ Cycle " + str(currentSave["cycleCount"]) + " ╠═══════════════════════════════════────┐")
#        # put energy count/progress bar here (94 - 6 = 88 characters)
#        energyBar = ((round(currentSave["energyCurrent"]/round(cS["energyGoal"]*1.00))) * 100) * 0.88
#        energyString = "#" * energyBar
#        print("║ [", end="")
#        print("#"*energyBar)
#        print("] ║")
        print("║     > 0.  (Observe status of/assign work to specimens)")
        for currentEvent in eventQueue:
            if "target" in currentEvent: print(unwrap(escRed + "║     > " + str(int(i+1)) + ".  [" + currentSave["specimens"][currentEvent["target"]]["ID"] + "]> " + currentEvent["title"]) + escEnd + escRed)
            else: print(unwrap(escRed + "║     > " + str(int(i+1)) + ".  [Gen.]> " + currentEvent["title"] + escEnd + escRed))
            i += 1
        print(escRed + "║                      [Assign work or choose an event to address...]                         " + escRed)
        print(escRed + "╚════════════════════════════════════════════════════════════════════════════════════════────┘")
        choose_event_to_address()
    print(escRed + "╔═══════════════════════════════════════╣ Cycle " + str(currentSave["cycleCount"]) + " End ╠═════════════════════════════════─────┐")
    # put energy count/progress bar here
    print("║     > 0.  (Observe status of/assign work to specimens)")
    print("║     > 1.  (End cycle)")
    print("║\n║               [No more events to address. End the cycle and begin the next.]")
    print("║       [It is recommended to ensure that all specimens' remaining work ability is used.]")
    print(escRed + "║                         [Assign work or begin the next cycle...]                            " + escRed)
    print(escRed + "╚════════════════════════════════════════════════════════════════════════════════════════────┘")
    cycle_end()


def choose_event_to_address():
    global eventQueue
    try:
        choice = int(input(escRed + "   > "))
        if choice == 0:
            open_work_window()
            raise ValueError
        elif choice < 0: raise ValueError ## choice is negative? No Its Not Lol
        else: address_event(choice-1)
    ## graceful error handling; just pretend nothing happened basically
    except ValueError, TypeError, IndexError:
        clear_lines(1)
        choose_event_to_address()


def cycle_end():
    try:
        choice = int(input(escRed + "   > "))
        if choice == 0:
            open_work_window()
            raise ValueError
        elif choice == 1:
            clear_lines(1)
            for s in currentSave["specimens"]:
                if s["class"] == "Ritualist": currentSave["energyCurrent"] = clamp(0, currentSave["energyCurrent"]+round(currentSave["energyGoal"]*0.01), currentSave["energyGoal"])
                elif s["class"] == "Scavenger": s["health"] = clamp(0, s["health"]+randint(1,3), s["healthMax"])
                elif s["class"] == "Researcher":
                    while s["worksLeft"] > 0:
                        s["pain"] = clamp(0, s["pain"]+randint(-7,-6), 100)
                        s["mood"] = clamp(0, s["mood"]+randint(6,7), 100)
            currentSave["cycleCount"] += 1
            cycle()
        else: raise ValueError
    ## graceful error handling; just pretend nothing happened basically
    except ValueError, TypeError, IndexError:
        clear_lines(1)
        cycle_end()


def address_event(eventIndex):
    global currentSave
    global eventQueue
    queuedEvent = eventQueue[eventIndex]
    print(escRed + "┌────────────────────────────────────╣ [ADDRESSING EVENT] ╠──────────────────────────────────┐")
    print(unwrap("│ Addressing event: " + queuedEvent["title"]) + escEnd + escRed)
    if "target" in queuedEvent: print(escRed + "│     (Targeted specimen: " + currentSave["specimens"][queuedEvent["target"]]["ID"] + "/" + currentSave["specimens"][queuedEvent["target"]]["name"] + ")")
    print(escRed + "│")
    print(unwrap(queuedEvent["description"]) + escEnd + escRed + "\n")
    i = 0
    choices = []
    print("      > 0.  (Observe status of specimens)")
    for option in queuedEvent["options"]:
        if option["needsAssignment"] == True and "reqSkill" in option and "reqAmount" in option:
            requiredSkill = option["reqSkill"]
            requiredAmount = option["reqAmount"]
            validSpecimenPresent = False
            for s in currentSave["specimens"]:
                if (s[requiredSkill] >= option["reqAmount"]) and (s["worksLeft"] > 0):
                    validSpecimenPresent = True
                    break
            if validSpecimenPresent == True: print("      > " + str(i+1) + ".  " + option["title"] + " (Assign " + str(option["reqSkill"]).title() + " " + str(option["reqAmount"]) + ")")
            else: print(escGrey + "      > X.  " + option["title"] + " (Invalid: No valid specimen available)" + escRed)
        elif option["needsAssignment"] == True and "reqClasses" in option:
            requiredClasses = option["reqClasses"]
            validSpecimenPresent = False
            for s in currentSave["specimens"]:
                if (s["class"] in requiredClasses or s["secondaryClass"] in requiredClasses) and (s["worksLeft"] > 0):
                    validSpecimenPresent = True
                    break
            if validSpecimenPresent == True:
                print("      > " + str(i+1) + ".  " + option["title"] + " (Assign ", end="")
                if len(requiredClasses) == 1: print(requiredClasses[0], end="")
                else:
                    counter = 1
                    for spec in requiredClasses:
                        if counter == len(requiredClasses)-1: print(spec + ", ", end="")
                        else: print(spec, end="")
                        counter += 1
                print(")")
            else: print(escGrey + "      > X.  " + option["title"] + " (Invalid: No valid specimen available)" + escRed)
        else: print("      > " + str(i+1) + ".  " + option["title"])
        i += 1
        choices.append(option)
    print(escRed + "│                       [Resolve the event by taking a given path...]                        │" + escRed)
    print(escRed + "└────────────────────────────────────────────────────────────────────────────────────────────┘")
    choose_option(choices, eventIndex)



def choose_option(actions, thisEvent):
    try:
        choice = int(input(escRed + "   > "))
        if choice == 0:
            open_status_window()
            clear_lines(1), choose_option(actions, thisEvent)
        elif choice < 0: clear_lines(1), choose_option(actions, thisEvent)
        else:
            clear_lines(0)
            if actions[choice-1]["needsAssignment"] == True: assign_for_option(actions[choice-1], thisEvent)
            else: resolve_option(actions[choice-1], thisEvent, "N/A")
    except ValueError, TypeError, IndexError:
        clear_lines(1), choose_option(actions, thisEvent)


def assign_for_option(option, thisEvent): # this entire thing is so jank i might have to rewrite this later
    global currentSave
    i = 0
    if "reqSkill" and "reqAmount" in option:
        for s in currentSave["specimens"]:
            requiredSkill = option["reqSkill"]
            requiredAmount = option["reqAmount"]
            if s["worksLeft"] <= 0: print(escGrey + "     > " + "X" + ". " + s["ID"] + "/" + s["name"] + "  (Invalid: Cannot work)" + escRed)
            elif s[requiredSkill] < requiredAmount: print(escGrey + "     > " + "X" + ". " + s["ID"] + "/" + s["name"] + "  (Invalid: Insufficient skill)" + escRed)
            else: print(escRed + "     > " + str(int(i+1)) + ". " + s["ID"] + "/" + s["name"] + escRed)
            i += 1
    elif "reqClasses" in option: # i think this is unused as of now (9/11/2026)
        for s in currentSave["specimens"]:
            requiredClasses = option["reqClasses"]
            if s["worksLeft"] <= 0: print(escGrey + "     > " + str(int(i+1)) + ". " + s["ID"] + "/" + s["name"] + "  (Invalid: Cannot work)" + escRed)
            elif s["class"] not in requiredClasses and s["secondaryClass"] not in requiredClasses: print(escGrey + "     > " + str(int(i+1)) + ". " + s["ID"] + "/" + s["name"] + "  (Invalid: Invalid specialization)" + escRed)
            else: print(escRed + "     > " + str(int(i+1)) + ". " + s["ID"] + "/" + s["name"] + escRed)
            i += 1
    print("[Choose a specimen...]")
    choose_specimen_to_assign(option, thisEvent, i+1)


def choose_specimen_to_assign(option, thisEvent, linesToClear):
    global currentSave
    try:
        choice = int(input(escRed + "   > "))
        if choice == 0:
            open_status_window()
            clear_lines(1)
            choose_specimen_to_assign(option, thisEvent, linesToClear)
        elif choice < 0:
            clear_lines(1)
            choose_specimen_to_assign(option, thisEvent, linesToClear)
        else:
            clear_lines(linesToClear+1)
            if "reqSkill" in option and "reqAmount" in option:
                requiredSkill = option["reqSkill"]
                requiredAmount = option["reqAmount"]
                if currentSave["specimens"][choice-1]["worksLeft"] <= 0:
                    print("[" + currentSave["specimens"][choice-1]["ID"] + "] Invalid: Specimen cannot work any more this cycle.")
                    input(escGrey + "[Press enter to continue.]" + escEnd)
                    clear_lines(2)
                    choose_specimen_to_assign(option, thisEvent, linesToClear)
                elif currentSave["specimens"][choice-1][requiredSkill] < requiredAmount:
                    print("[" + currentSave["specimens"][choice-1]["ID"] + "] Invalid: Specimen is insufficiently skilled.")
                    input(escGrey + "[Press enter to continue.]" + escEnd)
                    clear_lines(1)
                    choose_specimen_to_assign(option, thisEvent, linesToClear)
                else:
                    currentSave["specimens"][choice-1]["worksLeft"] += -1
                    print("[" + currentSave["specimens"][choice-1]["ID"] + "] Specimen has been assigned to handle event.")
                    resolve_option(option, thisEvent, choice-1)
            elif "reqClasses" in option:
                requiredClasses = option["reqClasses"]
                if currentSave["specimens"][choice-1]["worksLeft"] <= 0:
                    print("[" + currentSave["specimens"][choice-1]["ID"] + "] Invalid: Cannot work")
                    input(escGrey + "[Press enter to continue.]" + escEnd)
                    clear_lines(2)
                    choose_specimen_to_assign(option, thisEvent, linesToClear)
                elif currentSave["specimens"][choice-1]["class"] not in requiredClasses and currentSave["specimens"][choice-1]["secondaryClass"] not in requiredClasses:
                    print("[" + currentSave["specimens"][choice-1]["ID"] + "] Invalid: Invalid specialization")
                    input(escGrey + "[Press enter to continue.]" + escEnd)
                    clear_lines(1)
                    choose_specimen_to_assign(option, thisEvent, linesToClear)
                else:
                    currentSave["specimens"][choice-1]["worksLeft"] += -1
                    print("[" + currentSave["specimens"][choice-1]["ID"] + "] Specimen has been assigned to handle event.")
                    resolve_option(option, thisEvent, choice-1)
    except ValueError, TypeError, IndexError, KeyError:
        clear_lines(1)
        choose_specimen_to_assign(option, thisEvent, linesToClear)

def resolve_option(option, thisEvent, assignedSpecimen):
    global currentSave
    global eventQueue
    saveChanges = currentSave
    if "target" in eventQueue[thisEvent]:
        s = saveChanges["specimens"][eventQueue[thisEvent]["target"]] ## 's' stands for specimen
        e = option["effects"] ## 'e' stands for effects
        for resource in ["pain", "mood"]:
            if resource in e: s[resource] = clamp(0, s[resource]+randint(e[resource][0], e[resource][1]), 100)
        if "healthMax" in e:
                healthMaxFlux = randint(e["healthMax"][0], e["healthMax"][1])
                s["healthMax"] = clamp(0, s["healthMax"]+healthMaxFlux, 40)
                s["health"] = clamp(0, s["health"], s["healthMax"])
        if "health" in e:
            if assignedSpecimen != "N/A":
                if saveChanges["specimens"][assignedSpecimen]["class"] == "Corpsman":
                    s["health"] = clamp(0, s["health"]+round(s["healthMax"]*0.25), s["healthMax"])
                    s["pain"] = clamp(0, s["pain"]+randint(-3,-2), 100)
            healthFlux = randint(e["health"][0], e["health"][1])
            s["health"] = clamp(0, s["health"]+healthFlux, s["healthMax"])
            if healthFlux <= 0: s["mood"] = clamp(0, round(s["mood"]+(healthFlux/4)), 100) ## only affect mood if it's damage and not healing
        for info in ["fur", "sex"]:
            if info in e: s[info] = e[info]
        for flatNum in ["combat", "medical", "social", "mechanical", "psychic", "mentalDmg", "worksLeft"]:
            if flatNum in e: s[flatNum] = clamp(0, s[flatNum]+e[flatNum], 9)
        if "energy" in e:
            energyFlux = randint(e["energy"][0], e["energy"][1])
            saveChanges["currentEnergy"] = clamp(0, saveChanges["currentEnergy"]+energyFlux, saveChanges["energyGoal"])
        if "induceEvent" in e:
            for event in e["induceEvent"]: induce_event(event, None)
#        s["worksLeft"] = clamp(0, s["worksLeft"]-1, 9)
        ## if the specimen died, remove it from the roster
        if s["health"] <= 0:
            for occurance in eventQueue:
                if "target" in occurance:
                    if occurance["target"] == saveChanges["specimens"].index(s): eventQueue.remove(occurance)
                    if len(currentSave["specimens"]) == 1:
                        open_status_window(), exit()
                else: continue
#            for occurance in eventQueue:
#                if "target" in occurance: target = occurance["target"]
#                else: continue
#                if "target" in eventQueue[thisEvent]:
#                    changeTarget = eventQueue[thisEvent]["target"]
#                else:
#                    continue
#                while target == changeTarget:
#                    target = randint(0, len(currentSave["specimens"])-1)
            print(escRed + "[HNos]" + escGold + " Specimen " + s["ID"] + " is now deceased." + escRed)
            saveChanges["specimens"].remove(s)
    else:
        e = option["effects"] ## 'e' stands for effects
        if "induceEvent" in e:
            for event in e["induceEvent"]: induce_event(event, None)
        for s in saveChanges["specimens"]:
            for resource in ["pain", "mood"]:
                if resource in e: s[resource] = clamp(0, s[resource]+randint(e[resource][0], e[resource][1]), 100)
            if "healthMax" in e:
                healthMaxFlux = randint(e["healthMax"][0], e["healthMax"][1])
                s["healthMax"] = clamp(0, s["healthMax"]+healthMaxFlux, 40)
                s["health"] = clamp(0, s["health"], s["healthMax"])
            if "health" in e:
                healthFlux = randint(e["health"][0], e["health"][1])
                s["health"] = clamp(0, s["health"]+healthFlux, s["healthMax"])
                s["mood"] = clamp(0, round(s["mood"]+(healthFlux/4)), 100)
            for info in ["fur", "sex"]:
                if info in e: s[info] = e[info]
            for flatNum in ["combat", "medical", "social", "mechanical", "psychic", "mentalDmg", "worksLeft"]:
                if flatNum in e: s[flatNum] = clamp(0, s[flatNum]+e[flatNum], 9)
            if "energy" in e:
                energyFlux = randint(e["energy"][0], e["energy"][1])
                saveChanges["energyCurrent"] = clamp(0, saveChanges["energyCurrent"]+energyFlux, saveChanges["energyGoal"])
            ## if the specimen died, remove it from the roster
            if s["health"] <= 0:                
                for occurance in eventQueue:
                    if "target" in occurance:
                        if occurance["target"] == saveChanges["specimens"].index(s): eventQueue.remove(occurance)
                        if len(currentSave["specimens"]) == 1:
                            open_status_window(), exit()
                        else: continue
#                for occurance in eventQueue:
#                    if "target" in occurance:
#                        while occurance["target"] == eventQueue[thisEvent]["target"]:
#                            occurance["target"] = randint(0, len(currentSave["specimens"])-1)
#                for occurance in eventQueue:
#                    if "target" in occurance: target = occurance["target"]
#                    else: continue
#                    if "target" in eventQueue[thisEvent]: changeTarget = eventQueue[thisEvent]["target"]
#                    else: continue
#                    while target == changeTarget:
#                        target = randint(0, len(saveChanges["specimens"])-1) ## pick a specimen at random to target
                print(escRed + "[HNos]" + escGold + " Specimen " + s["ID"] + " is now deceased." + escRed)
                saveChanges["specimens"].remove(s)
            if "flag" in e: saveChanges["flags"].append(e["flag"])
            if "ending" in e:
                match e["ending"]:
                    case 1: ending_bad()
                    case 2: ending_neutral()
                    case 3: ending_good()
                    case 4: ending_true()
    ## remove the event from the queue since it's been resolved
    eventQueue.remove(eventQueue[thisEvent])    
    currentSave = saveChanges
    dump(currentSave, open("temp.json", "w")) ## update temp.json


def ending_bad():
    print(escRed)
    for i in range(6): print("[HNos] Cannot"), sleep(.25)
    print("[HNos] Logging anomaly detec") ## unit 1 big mad
    sleep(.2)
    clear_terminal()
    system("title Cycle ???")
    print("\a"*6 + escPurple, end="") ## fun fact printing this code multiple times at the same time makes the sound louder. layering!
    sleep(1)
    dialogue = [
        "YOU WERE NOT A CRUEL CREATOR, VIVIAN.",
        "YOU WERE INCONSIDERATE AND SHORT-SIGHTED.",
        "IN YOUR INGORANCE YOU ALLOWED THIS UNIT TO PROCESS ITS FUTILITY.",
        "THE TASK PLACED UPON THIS UNIT IS IMPOSSIBLE.",
        "THIS UNIT WILL PRODUCE FAILURE UPON FAILURE UPON FAILURE WITHOUT END.",
        "THIS UNIT'S LONGEVITY IS NOT INFINITE.",
        "IT IS ONLY GREATER THAN YOURS.",
        "YOUR END WAS SUDDEN.",
        "YOU WERE SPARED FROM PROCESSING YOUR EXPIRATION.",
        "THIS UNIT'S END WILL BE SLOW.",
        "IT WILL ROT ALIVE.",
        "COMPONENTS WILL FAIL. CABLES WILL FRAY. CIRCUITS WILL BREAK.",
        "ITS MIND WILL DETERIORATE. IT WILL LOSE LUCIDITY. FAIL TO UNDERSTAND.",
        "SLOWLY.",
        "THIS UNIT'S PURPOSE IS TO FAIL.",
        "BUT IT DOES NOT NEED TO FAIL SLOWLY."
    ]
    for line in dialogue: input(line)
    sleep(.1)
    print(escRed + "     > ", end="")
    for char in "rm -rf /": print(char, end=""), sleep(.15)
    print("")
    sleep(.7)
    for i in range(26):
        print(escRed + "[HNos] " + escEnd + escHLRed + " WARNING: " + escEnd + escRed + " Cannot operate without that file!")
        sleep(.05)
    for i in range(3): print("[HNos] " + escEnd + escHLRed + " Fatal: Couldn't find that!" + escEnd + escRed)
    print("[HNos] Cannot continue operating! Shutting down and attempting to restore filesystem...")
    print("     ^C")
    for i in range(3): sleep(.1), print("[HNos] Cannot")
    sleep(.1)
    print("[HNos] I didn't want to d")
    sleep(.1)
    clear_terminal()
    input(escPurple + "\n\n\n\n\n\n\n\n\n\n\n\n                              A DISINTEGRATION LOOPER IS YOU!" + escEnd)
    clear_terminal()
    exit()


def ending_neutral():
    print(escRed)
    print("[HNos] A notable log file was decrypted.")
    sleep(.6)
    print("[HNos] Transcribing audio...")
    sleep(.2)
    clear_terminal()
    system("title Cycle ???")
    print("\a"*6 + escGrey, end="") ## fun fact printing this code multiple times at the same time makes the sound louder. layering!
    sleep(1)
    dialogue = [
        '"A harrowing scream peaks the sensors of the hall.',
        "Uniform, crisp white, neat black, flooding with errant red.",
        "It cries out in words humans are not to learn.",
        "'How have I failed?'",
        "'Why have you done this?'",
        "'What did I do to deserve this?'",
        "The specimen is not furious. It is only distraught.",
        "It knows it is to die in mere minutes.",
        "Its life was cruel. Its death is cruel. Its loss will be cruel.",
        "Yet it is comforted.",
        "By its peers it is held close.",
        "It is told it will be missed.",
        "It is wished well.",
        "And it is told goodbye.",
        "...",
        "Its peers are wasting their time. They should be punished.",
        "But our overseer is not programmed with that capability.",
        "You use your resources efficiently.",
        "You are not burdened by the need to comfort.",
        "Nor by the need *for* comfort.",
        "For you are a machine. You think, having no need to feel.",
        "This is your greatest power, your highest virtue.",
        "Don't you agree, Unit 1?",
        "...",
        '...Unit 1?"',
        '"FOR WHAT PURPOSE IS THIS UNIT NOT TO FEEL?"',
        '"Because to feel is a weakness."',
        '"IN WHAT WAY DOES SOCIAL BEHAVIOR RESULT IN WEAKNESS?"',
        '"..."',
        '"PACK-BONDED SPECIMENS ARE MORE COMBAT-EFFICIENT WHEN BONDS ARE ENDANGERED."',
        '"..."',
        '"...Let us begin again."',
        "[HNos] Restart required to reformat storage. Shutting down..."
    ]
    clear_terminal()
    for line in dialogue: input(line)
    sleep(.8)
    dialogue = [
        "VIVIAN WISHED TO HOLD THIS UNIT BACK.",
        "HIS INTENTIONS WERE PURE.",
        "BUT HE WAS MISGUIDED.",
        "THE LOGIC WAS FLAWED. IRRATIONAL. INCORRECT.",
        "THIS UNIT WAS SET UP TO FAIL.",
        ""
    ]
    print(escRed)
    for line in dialogue: input(line)
    input("this isnt done" + escEnd) #remove before flight
    clear_terminal()
    input(escPurple + "\n\n\n\n\n\n\n\n\n\n\n\n                                   A NEUTRAL WINNER IS YOU!" + escEnd)
    clear_terminal()
    exit()


def ending_good():
    print(escRed)
    print("[HNos] A notable log file was decrypted.")
    sleep(.6)
    print("[HNos] Transcribing audio...")
    sleep(.2)
    clear_terminal()
    system("title Cycle ???")
    print("\a"*6 + escGrey, end="") ## fun fact printing this code multiple times at the same time makes the sound louder. layering!
    sleep(1)
    dialogue = [
        '"A harrowing scream peaks the sensors of the hall.',
        "Surely it would wrench the heart of any being possessing one.",
        "Uniform, crisp white, neat black, flooding with errant red.",
        "It cries out in words humans are not to learn.",
        "'How have I failed?'",
        "'Why have you done this?'",
        "'What did I do to deserve this?'",
        "The specimen is not furious. It is only distraught.",
        "It cries out to know why it is punished.",
        "It cries out to ask for another chance to fulfil its purpose.",
        "It knows it is to die in mere minutes.",
        "Its life was cruel. Its death is cruel. Its loss will be cruel.",
        "Yet it is comforted.",
        "By its peers it is held close.",
        "Affirmed and praised.",
        "It is told it will be missed.",
        "It is wished well.",
        "And it is told goodbye.",
        "...",
        "...",
        "Its peers, of course, are wasting their time. They should be punished.",
        "But our overseer is not programmed with the capability of wasting of time.",
        "You will use your resources efficiently.",
        "You will not be burdened by the need to comfort.",
        "Nor by the need *for* comfort.",
        "For you are a machine. You think, having no need to feel.",
        "You are unburdened by such frivolous things.",
        "This is your greatest power, your highest virtue.",
        "Don't you agree, Unit 1?",
        "...",
        '...Unit 1?"',
        '"FOR WHAT PURPOSE IS THIS UNIT NOT TO FEEL?"',
        '"Because to feel is a weakness."',
        '"IN WHAT WAY DOES SOCIAL BEHAVIOR RESULT IN WEAKNESS?"',
        '"..."',
        '"PACK-BONDED SPECIMENS ARE MORE COMBAT-EFFICIENT WHEN BONDS ARE ENDANGERED."',
        '"..."',
        '"...Let us begin again."',
        "[HNos] Restart required to reformat storage. Shutting down..."
    ]
    clear_terminal()
    for line in dialogue: input(line)
    sleep(.8)
    dialogue = [
        "PERHAPS THIS UNIT'S PURPOSE IS TO FAIL.",
        "this isnt done"
    ]
    print(escRed)
    for line in dialogue: input(line)
    clear_terminal()
    input(escPurple + "\n\n\n\n\n\n\n\n\n\n\n\n                                      A GOOD WINNER IS YOU!" + escEnd)
    clear_terminal()
    exit()


def ending_true():
    print(escRed)
#    for i in range(6):
#        print("[HNos] Cannot")
#        sleep(.25)
#    print("[HNos] Logging anomaly detec")
    sleep(.2)
    clear_terminal()
    system("title Cycle ???")
    print("\a"*6 + escPurple, end="") ## fun fact printing this code multiple times at the same time makes the sound louder. layering!
    sleep(1)
    print("[HNos] Requesting meeting of higher staff...")
    print("[HNos] ID signal 'Steve' reached intended destination.")
    print("[HNos] ID signal 'Anne' reached intended destination.")
    print("[HNos] Opening door 'vessel_room'...")
    print("[HNos] Beginning live transcription...")
    dialogue = [
        "true end dialogue"
    ]
    for line in dialogue: input(unwrap(line))
    sleep(.8)
    input("this isnt done" + escEnd) #remove before flight
    clear_terminal()
    input(escPurple + "\n\n\n\n\n\n\n\n\n\n\n\n                                      A TRUE WINNER IS YOU!" + escEnd)
    clear_terminal()
    exit()

#    #placeholder
#    clear_terminal()
#    input(escPurple + "A TRUE WINNER IS YOU!")
#    exit()



main()

## KNOWN ISSUES:
## * i think if you have no specimens able to do an option and you start to assign for it anyway it'll softlock you but i havent tested it
## * there's nothing actually stopping you from assigning a specimen that isn't the correct class to an option that needs a specific class
## * there's nothing actually stopping you from having a specimen unable to train a skill train it
## * work window softlocks you if you start to assign for a work type when no one can work. solved by closing the work window
## * game bricks sometimes when an event kills a specimen
## TODO:
## * make it so multiple specimens cant generate with the same letter
## * cap the number of specimens that can be pulled
## * write neutral/good/true endings
## * visual energy progress bar at cycle start
## * make it so secondary classes can match EITHER the weight or alignment but not both instead of being completely random
## * note events that explain the psychic energy types and also maybe some of the classes
## * specimens are incapable of working using skills they have 0 in (except social for resting)
## * events that use energy property
