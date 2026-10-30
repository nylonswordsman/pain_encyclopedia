## set up environment
import subprocess
from os import system
from sys import stdout
from time import sleep
from json import load, dump
from random import randint
from pe_lib import clamp, clear_lines, clear_terminal, display_status
## i was today years old when i discovered you can import functions that are in files right next to other files. i knew you could do that with modules but the fact that you can do that with your own files is so cool.
## my dad told me that importing modules/functions thereof is kind of like statically linking in most other languages which is cool


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



def work_main():
    while True:
        clear_terminal()
        display_status()
        print("[0.] Back: Return to event phase.")
        print("[1.] Rest: Take time to regulate condition.")
        print("[2.] Doctor: Assist another medically.")
        print("[3.] Store Energy: Store psychic energy.")
        print("[4.] Train: Improve a skill. 2x work needed.")
        print("[5.] Refine: Improve another's maximum health.")
        print("  [Review status and assign work or cancel...]")
        choose_work()
        dump(currentSave, open("temp.json", "w"))


def choose_work():
    global currentSave
    try:
        choice = int(input(escRed + "> "))
        if choice == 0: dump(currentSave, open("memnode.json", "w")), exit()
        elif choice in [1, 2, 3, 4, 5]: display_workers(choice)
        else: raise ValueError
    ## graceful error handling; just pretend nothing happened basically
    except ValueError, TypeError, IndexError: clear_lines(1), choose_work()


def display_workers(workType):
    global currentSave
    i = 0
    workCost = 1
    match workType:
        case 1: skill = "social"
        case 2: skill = "medical"
        case 3: skill = "psychic"
        case 4:
            skill = "N/A" ## "N/A" instead of None because i dont want to deal with None
            workCost += 1
        case 5: skill = "mechanical"
    for s in currentSave["specimens"]:
        if s["worksLeft"] < workCost: print(escGrey + "[X]" + ". " + s["ID"] + "/" + s["name"] + "  (Invalid: Unable to work)" + escRed)
        else:
            if skill == "N/A": print(escRed + "[" + str(int(i+1)) + "]. " + s["ID"] + "/" + s["name"] + escRed)
            else:
                if s[skill] == 0 and skill != "social": print(escGrey + "[X]" + ". " + s["ID"] + "/" + s["name"] + "  (Invalid: Incapable of that)" + escRed)
                else: print(escRed + "[" + str(int(i+1)) + "]. " + s["ID"] + "/" + s["name"] + " (Relevant skill: " + str(s[skill]) + ")" + escRed)
        i += 1
    print("          [Choose a specimen to work...]")
    choose_worker(workType, workCost, skill)


def choose_worker(workType, workCost, skill):
    global currentSave
    try:
        choice = int(input(escRed + "> "))
        if choice <= 0: choose_worker(workType, workCost, skill)
        elif currentSave["specimens"][choice-1]["worksLeft"] < workCost:
            clear_lines(1)
            choose_worker(workType, workCost, skill)
#        elif skill != "N/A":
#            if currentSave["specimens"][choice-1][skill] <= 0:
#                clear_lines(1)
#                choose_worker(workType, workCost, skill)
        else:
            workerIndex = choice-1
            match workType:
                case 1: execute_rest(workerIndex)
                case 2: display_doctor_targets(), execute_doctor(workerIndex, choose_doctor_target())
                case 3: execute_store_energy(workerIndex)
                case 4: display_skills(workerIndex), execute_train(workerIndex, choose_skill(workerIndex))
                case 5: display_refine_targets(), execute_refine(workerIndex, choose_refine_target())
                case _:
                    clear_lines(1)
                    choose_worker(workType, workCost, skill)
    except ValueError, TypeError, IndexError:
        clear_lines(1)
        choose_worker(workType, workCost, skill)


def display_doctor_targets():
    global currentSave
    i = 0
    for s in currentSave["specimens"]:
        print(f"{escRed}[{str(int(i+1))}]. {s["ID"]}/{s["name"]} (HEA: {s["health"]}/{s["healthMax"]}){escRed}")
        i += 1
    print("     [Choose a specimen to be treated...]")


def choose_doctor_target():
    global currentSave
    try:
        choice = int(input(escRed + "> "))
        targetIndex = choice-1
        return targetIndex
    except ValueError, TypeError, IndexError: clear_lines(1), choose_refine_target()


def display_refine_targets():
    global currentSave
    i = 0
    for s in currentSave["specimens"]:
        print(f"{escRed}[{str(int(i+1))}]. {s["ID"]}/{s["name"]} (M.HEA: {s["healthMax"]}){escRed}")
        i += 1
    print("     [Choose a specimen to be refined...]")


def choose_refine_target():
    global currentSave
    try:
        choice = int(input(escRed + "> "))
        targetIndex = choice-1
        return targetIndex
    except ValueError, TypeError, IndexError: clear_lines(1), choose_refine_target()


def display_skills(workerIndex):
    global currentSave
    s = currentSave["specimens"][workerIndex]
    if s["combat"] in [0,9]: print(f"{escGrey}[X]. Combat     ({s["combat"]}){escRed}") ## if it's 0 or 9
    else: print(f"[1]. Combat     ({s["combat"]})")
    if s["medical"] in [0,9]: print(f"{escGrey}[X]. Medical    ({s["medical"]}){escRed}")
    else: print(f"[2]. Medical    ({s["medical"]})")
    if s["social"] in [0,9]: print(f"{escGrey}[X]. Social     ({s["social"]}){escRed}")
    else: print(f"[3]. Social     ({s["social"]})")
    if s["mechanical"] in [0,9]: print(f"{escGrey}[X]. Mechanical ({s["mechanical"]}){escRed}")
    else: print(f"[4]. Mechanical ({s["mechanical"]})")
    if s["psychic"] in [0,9]: print(f"{escGrey}[X]. Psychic    ({s["psychic"]}){escRed}")
    else: print(f"[5]. Psychic    ({s["psychic"]})")
    print("          [Choose a skill to train...]")


def choose_skill(workerIndex):
    global currentSave
    while True:
        try:
            choice = int(input(escRed + "> "))
            match choice:
                case 1:
                    if currentSave["specimens"][workerIndex]["combat"] not in [0,9]: return "combat"
                    elif currentSave["specimens"][workerIndex]["combat"] == 0:
                        input(f"{escGrey}[{currentSave["specimens"][workerIndex]["ID"]}] Invalid: Incapable of that.{escRed}")
                        clear_lines(2)
                        continue
                    elif currentSave["specimens"][workerIndex]["combat"] == 9:
                        input(f"{escGrey}[{currentSave["specimens"][workerIndex]["ID"]}] Invalid: Already mastered that.{escRed}")
                        clear_lines(2)
                        continue
                case 2:
                    if currentSave["specimens"][workerIndex]["medical"] not in [0,9]: return "medical"
                    elif currentSave["specimens"][workerIndex]["medical"] == 0:
                        input(f"{escGrey}[{currentSave["specimens"][workerIndex]["ID"]}] Invalid: Incapable of that.{escRed}")
                        clear_lines(2)
                        continue
                    elif currentSave["specimens"][workerIndex]["medical"] == 9:
                        input(f"{escGrey}[{currentSave["specimens"][workerIndex]["ID"]}] Invalid: Already mastered that.{escRed}")
                        clear_lines(2)
                        continue
                case 3:
                    if currentSave["specimens"][workerIndex]["social"] not in [0,9]: return "social"
                    elif currentSave["specimens"][workerIndex]["social"] == 0:
                        input(f"{escGrey}[{currentSave["specimens"][workerIndex]["ID"]}] Invalid: Incapable of that.{escRed}")
                        clear_lines(2)
                        continue
                    elif currentSave["specimens"][workerIndex]["social"] == 9:
                        input(f"{escGrey}[{currentSave["specimens"][workerIndex]["ID"]}] Invalid: Already mastered that.{escRed}")
                        clear_lines(2)
                        continue
                case 4:
                    if currentSave["specimens"][workerIndex]["mechanical"] not in [0,9]: return "mechanical"
                    elif currentSave["specimens"][workerIndex]["mechanical"] == 0:
                        input(f"{escGrey}[{currentSave["specimens"][workerIndex]["ID"]}] Invalid: Incapable of that.{escRed}")
                        clear_lines(2)
                        continue
                    elif currentSave["specimens"][workerIndex]["mechanical"] == 9:
                        input(f"{escGrey}[{currentSave["specimens"][workerIndex]["ID"]}] Invalid: Already mastered that.{escRed}")
                        clear_lines(2)
                        continue
                case 5:
                    if currentSave["specimens"][workerIndex]["psychic"] not in [0,9]: return "psychic"
                    elif currentSave["specimens"][workerIndex]["psychic"] == 0:
                        input(f"{escGrey}[{currentSave["specimens"][workerIndex]["ID"]}] Invalid: Incapable of that.{escRed}")
                        clear_lines(2)
                        continue
                    elif currentSave["specimens"][workerIndex]["psychic"] == 9:
                        input(f"{escGrey}[{currentSave["specimens"][workerIndex]["ID"]}] Invalid: Already mastered that.{escRed}")
                        clear_lines(2)
                        continue
                case _:
                    clear_lines(1)
                    continue
        except TypeError: clear_lines(1)


def execute_rest(workerIndex):
    global currentSave
    s = currentSave["specimens"][workerIndex]
    if s["class"] == "Elite":
        moodFlux = randint(4, 5)+(round((s["social"]*0.6)*0.7))
        painFlux = randint(-5, -4)+(round(s["social"]*0.7)*-1)
    elif s["class"] == "Commander":
        moodFlux = randint(3, 4)+(round(s["social"]*0.7))
        painFlux = randint(-5, -3)+(round(s["social"]*0.7)*-1)
        for specimen in currentSave["specimens"]:
            s["mood"] = clamp(0, s["mood"]+randint(2,4), 100)
    else:
        moodFlux = randint(4, 5)+(round(s["social"]*0.7))
        painFlux = randint(-5, -4)+(round(s["social"]*0.7)*-1)
    s["mood"] = clamp(0, s["mood"]+moodFlux, 100)
    s["pain"] = clamp(0, s["pain"]+painFlux, 100)
    s["worksLeft"] += -1


def execute_doctor(workerIndex, targetIndex):
    d = currentSave["specimens"][workerIndex] ## 'd' stands for doctor
    p = currentSave["specimens"][targetIndex] ## 'p' stands for patient
    ## assigning heal formula according to class; some classes are better or worse at doctoring than others
    if d["class"] == "Medic": healthFlux = max(round((d["medical"]+randint(-1, 1))*1.2), 2)
    elif d["class"] == "Hemomancer": healthFlux = max(round((d["medical"]+2)*1.4), 5)
    elif d["class"] == "Elite": healthFlux = round(((d["medical"]*0.6)+randint(-2, -1))*1.2)
    else: healthFlux = round((d["medical"]+randint(-2, -1))*1.2)
    ## the actual heal
    p["health"] = clamp(0, p["health"]+healthFlux, p["healthMax"])
    ## assigning an additional effect according to class, if the specimen is one of the classes that has those
    if d["class"] == "Hemomancer": d["health"] = clamp(0, d["health"]+min(round(d["healthMax"]*-0.25), -4), d["healthMax"])
    elif d["class"] == "Paragon":
        d["mood"] = clamp(0, d["mood"]+randint(2, 3), 100)
        p["mood"] = clamp(0, p["mood"]+randint(3, 4), 100)
    d["worksLeft"] += -1


def execute_store_energy(workerIndex):
    global currentSave
    s = currentSave["specimens"][workerIndex] ## 's' stands for specimen
    if s["class"] == "Mindbreaker": energyFlux = max((randint(1,2)+round(s["psychic"]*0.8)), randint(4,5))
    elif s["class"] == "Elite": energyFlux = max((randint(1,2)+round((s["psychic"]*0.6)*0.5)), randint(3,5))
    else: energyFlux = max((randint(1,2)+round(s["psychic"]*0.5)), randint(3,5))
    if s["class"] == "Mindbreaker":
        healthFlux = min(round(s["healthMax"]*-0.1), randint(-3, -2))
        if s["health"] + healthFlux <= 0: s["mentalDmg"] = clamp(0, s["mentalDmg"]+1, 3)
        else: s["health"] = clamp(0, s["health"]+healthFlux, s["healthMax"])
        s["pain"] = clamp(0, s["pain"]+round(s["psychic"]*0.4), 100)
    currentSave["energyCurrent"] = clamp(0, currentSave["energyCurrent"]+energyFlux, currentSave["energyGoal"])
    s["worksLeft"] += -1


def execute_train(workerIndex, skill):
    global currentSave
    s = currentSave["specimens"][workerIndex] ## 's' stands for specimen
    s[skill] = clamp(0, s[skill]+1, 9)
    if s["class"] == "Elite": s[skill] = clamp(0, s[skill]+1, 9)
    s["worksLeft"] += -2


def execute_refine(workerIndex, targetIndex):
    d = currentSave["specimens"][workerIndex] ## 'd' stands for doctor
    p = currentSave["specimens"][targetIndex] ## 'p' stands for patient
    if d["class"] == "Elite": healthMaxFlux = round(((d["mechanical"]*0.6)+randint(-5,-4)*0.6))
    elif d["class"] == "Machinist": healthMaxFlux = round((d["mechanical"]+randint(-2, -1)*0.6))
    else: healthMaxFlux = round((d["mechanical"]+randint(-5,-4)*0.6))
    if d["class"] == "Biotech.": p["healthMax"] = clamp(0, p["healthMax"]+healthMaxFlux, 40)
    else: p["healthMax"] = clamp(0, p["healthMax"]+healthMaxFlux, 30)
    d["worksLeft"] += -1



work_main()
