from os import system
from sys import stdout
from json import load



def clamp(minCap, value, maxCap):
    return min(max(minCap, value), maxCap)


def clear_lines(linesToClear=int):
    for i in range(linesToClear): ## do the specified number of times:
        stdout.write("\033[F\033[2K") ## write an escape code to the standard output of the terminal that clears a line


def clear_terminal():
    system("cls")


#def randint():
#    pass


#def randchoice():
#    pass


def display_status():
    currentSave = load(open("temp.json", "r"))
    escRed = '\x1b[31m'     ## corresponds to 'STARTRED'
    escBRed = '\x1b[1;31m'  ## corresponds to 'STARTBRED'
#    escHLRed = '\x1b[41m'   ## corresponds to 'STARTHLRED'
#    escGreen = '\x1b[32m'   ## corresponds to 'STARTGREEN'
    escGold = '\x1b[33m'    ## corresponds to 'STARTGOLD'
#    escHLGold = '\x1b[43m'  ## corresponds to 'STARTHLGOLD'
#    escBlue = '\x1b[1;34m'  ## corresponds to 'STARTBLUE'
    escPurple = '\x1b[35m'  ## corresponds to 'STARTPURPLE'
#    escCyan = '\x1b[36m'    ## corresponds to 'STARTCYAN'
    escGrey = '\x1b[37m'    ## corresponds to 'STARTGREY'
    escEnd = '\x1b[m'       ## corresponds to 'ENDCOLOR'. stops current escape

    print(f"  ------------- Energy: {str(currentSave["energyCurrent"])}/{str(currentSave["energyGoal"])}u -------------\n")
    system("title Current specimens: " + str(len(currentSave["specimens"])))
    if len(currentSave["specimens"]) == 0:
        print(escGold + "           [No specimens connected.]")
        print(escGold + "[Take care not to allow unnecessary casualties.]\n\n")
        input(escGrey + "          [Press enter to go back...]" + escEnd)
        exit()
    else:
        for s in currentSave["specimens"]: ## 's' stands for specimen
#                ## the following comment dunes i could not figure out how to get work but am keeping it in case i wanna come back to it later
#                cmbt = 0 += s["combat"]
#                medi = 0 += s["medical"]
#                socl = 0 += s["social"]
#                mech = 0 += s["mechanical"]
#                psyc = 0 += s["psychic"]
#
#                stats = {
#                    "cmbt": s["combat"],
#                    "medi": s["medical"],
#                    "socl": s["social"],
#                    "mech": s["mechanical"],
#                    "psyc": s["psychic"]
#                }
#                newStats = {
#                    "cmbt": 0,
#                    "medi": 0,
#                    "socl": 0,
#                    "mech": 0,
#                    "psyc": 0
#                }
#                for stat in stats:
#                    newStats[stat] += stats[stat]
#                    match stat:
#                        case 0 | 1 | 2 | 3 | 4 | 5:
#                            newStats[stat] = str(escRed + str(s[stat]) + escEnd)
#                        case 6 | 7 | 8:
#                            newStats[stat] = str(escBRed + str(s[stat]) + escEnd)
#                        case 9:
#                            newStats[stat] = str(escGold + str(s[stat]) + escEnd)
#                    print(newStats[stat]) #remove before flight
#                print(newStats)
            ## i would love to have just for-looped this process but i could not for the life of me figure it out
            cmbt = "" ## combat skill
            if s["combat"] == 9: cmbt = escGold + str(s["combat"]) + escRed
            elif s["combat"] >= 6: cmbt = escBRed + str(s["combat"]) + escEnd + escRed
            elif s["combat"] == 0: cmbt = escPurple + str(s["combat"]) + escRed
            else: cmbt = escRed + str(s["combat"]) + escRed
            medi = "" ## medical skill
            if s["medical"] == 9: medi = escGold + str(s["medical"]) + escRed
            elif s["medical"] >= 6: medi = escBRed + str(s["medical"]) + escEnd + escRed
            elif s["medical"] == 0: medi = escPurple + str(s["medical"]) + escRed
            else: medi = escRed + str(s["medical"]) + escRed
            socl = "" ## social skill
            if s["social"] == 9: socl = escGold + str(s["social"]) + escRed
            elif s["social"] >= 6: socl = escBRed + str(s["social"]) + escEnd + escRed
            elif s["social"] == 0: socl = escPurple + str(s["social"]) + escRed
            else: socl = escRed + str(s["social"]) + escRed
            mech = "" ## mechanical skill
            if s["mechanical"] == 9: mech = escGold + str(s["mechanical"]) + escRed
            elif s["mechanical"] >= 6: mech = escBRed + str(s["mechanical"]) + escEnd + escRed
            elif s["mechanical"] == 0: mech = escPurple + str(s["mechanical"]) + escRed
            else: mech = escRed + str(s["mechanical"]) + escRed
            psyc = "" ## psychic skill
            if s["psychic"] == 9: psyc = escGold + str(s["psychic"]) + escRed
            elif s["psychic"] >= 6: psyc = escBRed + str(s["psychic"]) + escEnd + escRed
            elif s["psychic"] == 0: psyc = escPurple + str(s["psychic"]) + escRed
            else: psyc = escRed + str(s["psychic"]) + escRed
            work = "" ## works left
            if s["worksLeft"] <= 0: work = escRed + str(s["worksLeft"])
            else: work = escBRed + str(s["worksLeft"]) + escEnd + escRed
            maxHealth = "" ## maximum health
#            if s["healthMax"] == 40: maxHealth = escGold + str(s["healthMax"]) + escRed
            if s["healthMax"] >= 30: maxHealth = escBRed + str(s["healthMax"]) + escEnd + escRed
            else: maxHealth = escRed + str(s["healthMax"]) + escRed
            currentHealth = "" ## current health, colored based on how full it is
            if s["health"] < round(s["healthMax"]*0.50) and s["class"] != "Scavenger": currentHealth = escBRed + str(s["health"]) + escEnd + escRed
            else: currentHealth = escRed + str(s["health"]) + escRed
            pain = "" ## current pain
            if s["pain"] >= 85: pain = escGold + str(s["pain"]) + escRed
            elif s["pain"] >= 20: pain = escBRed + str(s["pain"]) + escEnd + escRed
            else: pain = escRed + str(s["pain"]) + escRed
            mood = "" ## current mood
            if s["mood"] < 20: mood = escGold + str(s["mood"]) + escRed
            elif s["mood"] < 40: mood = escBRed + str(s["mood"]) + escEnd + escRed
            else: mood = escRed + str(s["mood"]) + escRed
            mentaldmg = ""
            if s["mentalDmg"] <= 0: mentaldmg = escRed + str(s["mentalDmg"]) + escRed
            elif s["mentalDmg"] == 1: mentaldmg = escBRed + str(s["mentalDmg"]) + escEnd + escRed
            elif s["mentalDmg"] >= 2: mentaldmg = escGold + str(s["mentalDmg"]) + escRed
            ## printing phase
#                print(cmbt + " " + medi + " " + socl + " " + mech + " " + psych)
#                print(f"{cmbt} {medi} {socl} {mech} {psyc}")
            print(escRed + f"╔═════════════════╣ {s["ID"]} ╠══════════════─────┐")
            print(f"║ CMBT: {cmbt}  MEDI: {medi}  SOCL: {socl}  MECH: {mech}  PSYC: {psyc}")
            print(f"║ WEIGHT/ALIGN.: {s["weight"]}/{s["alignment"]}    WORK LEFT: {work}")
            print(f"║ CLASS/SEC.CLS: {escBRed + s["class"] + escEnd + escRed}/{s["secondaryClass"]}")
            print(f"║ SEX: {s["sex"]}  FUR: {s["fur"]}  INF.NAME: {s["name"]}")
            print("╟──────────────────────────────────────────────┤")
            print(f"║ HEA.: {currentHealth}/{maxHealth}  PAIN: {pain}  MOOD: {mood}  MNTL.DMG: {mentaldmg}")
            print("╚═════════════════════════════════════════─────┘\n")
