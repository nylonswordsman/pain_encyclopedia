## Requirements
* Python 3.14 or later
* Windows 11 (does not work on Linux unless run on a Windows VM. not tested for windows 10, but theres no reason it shouldnt work there)
* Powershell

## Instructions
* download and extract as .zip
* open powershell
* `cd` to the extracted folder
* ensure your python is installed and up to date (`py --version`)
* run `py pain_encyclopedia.py`
* enjoy


## Difficulties
Your difficulty is chosen for a memory node when it is created.
Note that if you have more than 6 specimens, HARSH and CRUEL are unavailable; if a HARSH or CRUEL amount of energy is selected but you have over 6 specimens, it will become LENIENT.
Difficulties don't affect anything other than the amount of extra events you get per cycle and the number of possible endings/cycles.
Don't kick yourself for losing; the game is somewhat random in nature, the same way Randy Random is if you've ever played Rimworld.
#### **LENIENT**
* For people who want a bit of practice without a whole ton of pressure.
* Less extra events.
#### **HARSH**
* For people who want to engage their brain cells a little more.
* Standard extra events.
* A new ending becomes possible...
#### **CRUEL**
* For those seeking a challenge.
* More extra events.
* With the overcoming of a great trial, yet another new ending is possible...
* Careful thought will get you far, but only good fortune will see you the rest of the way to the end.


## Classes
Specimens have classes and secondary classes, determined when they are pulled from cryptosleep at the start of the run. The primary class is determined by where their weight and alignment land them on the table below.

| Header |   Light   |  Medium   |   Heavy   |
| :----: | :-------: | :-------: | :-------: |
| Arcane |   Elite   | Machinist | Commander |
| Divine |  Paragon  |   Medic   | Corpsman  |
| Occult |Mindbreaker| Hemomancer| Researcher|
| Primal | Ritualist |  Biotech. | Scavenger |

Most classes have a fun little perk they grant the specimen when it is the primary class.
* Elite: Training skills is twice as effective. Relevant skill is treated as much less than it is for all work types. Great for skill checks!
* Machinist: Will increase specimens' max health more when refining.
* Commander: Resting slightly restores all specimens' mood.
* Paragon: Increases both doctor's and patient's mood when doctoring.
* Medic: Restores a bit more health when doctoring, and can't restore less than 4 health, even if their medical skill is low.
* Corpsman: Heals specimens targeted by damaging events if they are the one assigned. Heal takes place before damage is inflicted; less helpful when the target is near full health, but more likely to prevent a casualty when they're low.
* Mindbreaker: Stores much more psychic energy at once, but builds pain and damage to do it.
* Hemomancer: Working title. Injures themselves to doctor others more effectively.
* Researcher: Reduces own pain and increases own mood according to work left at the end of the cycle (LIE it does not do that, i didnt implement it yet)
* Ritualist: Stores a bit of energy at the end of each cycle.
* Biotechnician: Capable of increasing specimens' max health up to 40 rather than 30 when refining.
* Scavenger: Slightly restores own health at the end of each cycle.



## Tips
* h



# For devs

#### DO NOT touch the .json files without reading this!! it will break things!
* `temp.json` is the file that the game uses to store information when another window needs to access it since i couldnt figure out how to pass that information as a variable to the other window
* `data.json` is the file used to store potential names and information about the classes, and is used when generating new specimens
* `events.json` contains the entire event pool. it can be edited but be very careful about json formatting. the good part of this is that if python doesnt like the formatting, it'll tell you exactly where in the file it found something yucky
* if you delete any of these the program will crash because it does not validate that it exists before looking for it. i havent changed that because im lazy. fight me
* `memnode.json` must be deleted to make a new save. just don't delete it mid-game and you're good
#### event categories are indexed as follows:
0. mental fractures
1. mental breaks
2. injuries
3. psychic disturbances
4. raiders
5. nanite infections
6. social
7. story/fixed events
#### fixed events (in `events.json[7]`):
0. cycle 1 note
1. cycle 10 note
2. 25% note
3. 50% note
4. 75% note
5. 90% note
6. 100% note
7. neutral end
8. good end
9. good end (can continue)
10. bad end/disintegration loop
11. bad end/disintegration loop (can continue)
12. true end 
~~13. catharsis (from mental fractures)~~
#### how `data.json` is indexed
0. male names
1. female names
2. specimen class information
~~3. bad end dialogue~~
~~4. neutral end dialogue~~
~~5. good end dialogue~~
~~6. true end dialogue~~