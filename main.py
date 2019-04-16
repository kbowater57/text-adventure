# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 15:25:13 2019

@author: kbowa
This will contain a basic text adventure game.
"""

###############################################################################
###########################FUNCTION DEFINITIONS################################
###############################################################################

def move(direction,character,room_point_set):
    # This function takes a character input by the user, transforms it to
    # a vector in complex notation (where north is 1j, east is 1), and then
    # performs checks against given points to ensure that the character 
    # remains within the confines of the dungeon (e.g. not going through
    # a wall). It returns the character object, either with an updated
    # location, or not, in the case of an invalid input
    if direction == "n" or direction == "north":
        dir_vector = 0+1j
        character["dir_word"] = "north"
    elif direction == "e" or direction == "east":
        dir_vector = 1+0j
        character["dir_word"] = "east"
    elif direction == "s" or direction == "south":
        dir_vector = 0-1j
        character["dir_word"] = "south"
    elif direction == "w" or direction == "west":
        dir_vector = -1+0j
        character["dir_word"] = "west"
    else:
        print("That's not a valid direction. Try again.")
    
    proposed_location = character["location"] + dir_vector
    character["direction"] = dir_vector
    
    if proposed_location not in room_point_set:
        print("You just walked into a wall. Ouch! You take 1 damage.")
        character["health"] -= 1
    elif proposed_location == -10 + 7j:
        print("You approach the chest, and throw it open eagerly. A huge "
              "bounty of gold coins lies within the chest. Congratulations! "
              "You have won the game!")
        character["quest_stage"] = "complete"
    else:
        character["location"] = proposed_location
        character["direction"] = dir_vector
    return character    

def display_location(character):
    string_inserted_1 = ""
    string_inserted_2 = ""
    print(("You are at co-ordinate (" + str(int(character["local_coord"].real)) + ", " + 
        str(int(character["local_coord"].imag)) + "), in room " + 
    str(character["roomno"]) + ". You are facing " ))
    if( 
    character["location"].real == character["room_dict"]["corner_sw"].real 
    and character["dir_word"] == "east" or 
    character["location"].real == character["room_dict"]["corner_ne"].real 
    and character["dir_word"] == "west" or
    character["location"].imag == character["room_dict"]["corner_sw"].imag 
    and character["dir_word"] == "south" or
    character["location"].imag == character["room_dict"]["corner_ne"].imag
    and character["dir_word"] == "north"):
        string_inserted_1 = "the "
        string_inserted_2 = " wall"
    print(string_inserted_1 + character["dir_word"] + string_inserted_2 + ".")
def stat(character):
    display_location(character)
    print("You have " + str(character["health"]) + " hitpoints remaining.")
    
def help_text():
    help = open("help.txt","r")
    for line in help:
        print(line)
    help.close()
    
def room_desc(character):
    # This function reads from text files in the current directory, which
    # give descriptions of each room within the dungeon
    room_text = ("room" + str(character["roomno"]) + ".txt")
    text = open(room_text,"r")
    for line in text:
        print(line)
    text.close()
    room_size = (character["room_dict"]["corner_ne"]
    - character["room_dict"]["corner_sw"]+1+1j)
    print("This room is " + str(int(room_size.real)) + " wide by " +
           str(int(room_size.imag)) + " deep.")
    
def check_room(character, room_points_dict):
    # This function determines which room the character is currently in, by
    # checking against a dictionary in which each room is a word whose
    # value is a list of all points (again in complex notation x+yj) in that 
    # room.
    for number in range(len(room_points_dict)):
        if character["location"] in room_points_dict["room"+str(number)]:
            character["roomno"] = number
            return character

def add_room(corner_dict,room_point_list):
    #This function takes a dictionary (room_dict) which has words corner_sw
    # and corner_ne, which describe the SW and NE corners of the room in 
    # complex notation (x+yj), and returns a list containing all points 
    # contained in that room, again in complex notation 
    returned_list=list()
    for xcoord in range((int(corner_dict["corner_sw"].real)),
                        (int(corner_dict["corner_ne"].real+1))):
        for ycoord in range((int(corner_dict["corner_sw"].imag)),
                            (int(corner_dict["corner_ne"].imag+1))):
            returned_list.append(complex(xcoord,ycoord))
    room_point_list.extend(returned_list)
    return room_point_list

def check_triggers(character,trigger_dict):
    character["trigger"] = ""
    trigger_dir_loc = ""
    for word in trigger_dict:
        if (character["location"] in trigger_dict[str(word)][0] and
            character["direction"] in trigger_dict[str(word)][1]):
                trigger_dir_loc = word
        
    if trigger_dir_loc == "torch" and "torch" not in character["inv"]:
        print("In front of you is a burning torch, resting in an iron"
              " bracket.")
        character["trigger"] = "torch"
        
    if trigger_dir_loc == "darkness_warning":
        character["trigger"] = "darkness_warning"
        if "torch" not in character["inv"]:
            print("Be careful! All kinds of nasty creatures live in the dark.")
        if "torch" in character["inv"]:
            print("Lifting your torch, you see an orc standing 3 paces in "
                  "front of you. It squints at the bright light of your torch"
                  ", and growls threateningly.")
        
    if trigger_dir_loc == "grue" and "torch" not in character["inv"]:
        print("You were eaten by a grue. Better bring a torch next time.")
        character["health"] = 0
        
    if (trigger_dir_loc == "orc_fight" and 
        character["quest_stage"] == "slay orc"):
        print("The orc is now directly in front of you. It hunkers down, "
              "with bared teeth, readying itself to leap onto you.")
        character["trigger"] = "orc fight"
        
    return character

###############################################################################
#########################DECLARATION OF VARIABLES##############################
###############################################################################
                
    
# Creating the room dictionaries for add_room, and creating a 
room0_dict = {"corner_ne": (4+4j),"corner_sw": (0+0j)}
room0_list = list()
room0_list=add_room(room0_dict,room0_list)
room1_dict = {"corner_ne": (-1+2j),"corner_sw": (-6+2j)}
room1_list = list()
room1_list=add_room(room1_dict,room1_list)
room2_dict = {"corner_ne": (-7+8j),"corner_sw": (-13+1j)}
room2_list = list()
room2_list=add_room(room2_dict,room2_list)

# A dictionary with each room as a word, with a list containing all points in
# the respective room as each word's value
room_points_dict = {"room0":room0_list,"room1":room1_list,"room2":room2_list}

# room_point_list is a list with all points in the dungeon, used to check that
# the character remains within the dungeon in function move()
room_point_list=list()    
room_point_list = add_room(room0_dict,room_point_list)
room_point_list = add_room(room1_dict,room_point_list)
room_point_list = add_room(room2_dict,room_point_list)

# List of special locations paired with directions, triggering events if
# satisfied
trigger_dict = ({"torch":[[(2+4j)],[(0+1j)]], "darkness_warning":
    [[(-1+2j)],[(-1+0j)]],"grue":[[-2+2j],[-1+0j]],
    "orc_fight":[[-4+2j],[-1+0j]],"chest":[[]]})

# character object. All directions and locations are described in complex
# notation x+yj. location is in global co-ords, where local-coord uses the 
# current room's SW corner as the origin.
character = ({"location":0+0j,"health":2,"roomno":0, "inv":{"sword":10}, 
              "quest_stage":"find torch", "room_dict":room0_dict, "local_coord": 0+0j,
              "trigger":"","dir_word":"north"})

# Prints at the beginning of the game
room_desc(character)
display_location(character)
print("Type help for available commands.")

###############################################################################
##################################GAME LOOP####################################
###############################################################################

# The quest is to move to the chest in the third room. This is updated in 
#function move()
while character["quest_stage"] != "complete":
    old_location = character["location"]
    old_room = character["roomno"]
    character = check_triggers(character, trigger_dict)
    
    # Checks if character is still alive before doing anything else
    if character["health"] <=0:
        print("Oh no! You died. Better luck next time!")
        break
    
    requested_action = input("What would you like to do? \n")
    
    if character["trigger"] == "orc fight":
        if requested_action[:4] == "use ":
            if requested_action[4:] == "sword":
                print("You raise your sword just in time for the orc's leap."
                      "It springs towards you, impaling itself on your sword"
                      " in the process. With a weak groan, it slides to the"
                      " ground, dead.")
                character["quest_stage"] = "find key"
            elif requested_action[4:] == "torch":
                print("You raise the torch, and swing it at the orc. It hisses"
                      ", leaps backwards, and runs further into the dungeon")
        else:
            print("The orc leaps onto you, and tears into your throat with"
                  " its vicious teeth. Your blood spatters across the "
                  "dungeon's wall. As your vision fades, you hear the orc"
                  " cackle evilly and mutter \"Meat's back on the menu,"
                  " boys! \n \n Oh no! You died. Better luck next time!")
            character["health"] = 0
            break
    
    # Either accept move [n,e,s,w] or just [n,e,s,w] as move command

    elif requested_action[0:5] == "move ":
        character = move(requested_action[5:],character,room_point_list)
    elif requested_action[0] == "n" and len(requested_action) == 1:
        character = move("n",character,room_point_list)
    elif requested_action[0] == "e" and len(requested_action) == 1:
        character = move("e",character,room_point_list)
    elif requested_action[0] == "s" and len(requested_action) == 1:
        character = move("s",character,room_point_list)    
    elif requested_action[0] == "w" and len(requested_action) == 1:
        character = move("w",character,room_point_list)
    
        
    elif requested_action[0:5] == "take ":
        if requested_action[5:] == "torch" and character["trigger"] == "torch":
            character["inv"]["torch"] = 1
            character["quest_stage"] = "slay orc"
            print("You take the torch. "
                  "The area around you is now brightly lit.")
        else:
            print("There's no " + requested_action[5:] + " to take here.")
        
    # Handy command to exit game
    elif requested_action == "die":
        print("Oh no! You died. Better luck next time!")
        break
    
    # Various commands to print information about the character and their
    # surroundings
    elif requested_action == "stat": #prints health
        stat(character)
    elif requested_action == "disp": #current room info text
        display_location(character)
    elif requested_action == "help": #display commands available to player
        help_text()
    elif requested_action == "look": #print local_coords
        room_desc(character)
    elif requested_action == "inv": #print inventory
        print(character["inv"])
    
    elif requested_action[:4] == "use ":
        if requested_action[4:] == "sword":
            print("There's nothing to stab here.")
        elif requested_action[4:] == "torch" and "torch" in character["inv"]:
            print("There's nothing to burn here.")
        else:
                print("You don't have a " + requested_action[4:] + ".")
    # If command not recognised, complain
    else:
        print("I don't know how to " + requested_action + ".")
        
    if character["location"] != old_location:
        # Determines which room the character is in
        character = check_room(character,room_points_dict)
        # Updates the character's room_dict to reflect new room
        character["room_dict"] = globals()["room"+str(character["roomno"])+"_dict"]
        # Obtains character's location in local (room-based) co-ords
        character["local_coord"] = (character["location"] -
        character["room_dict"]["corner_sw"])
        # Prints the new room description, if the room has changed
        if old_room != character["roomno"]:
            room_desc(character)
        # Prints the character's local co-ordinates
        display_location(character)
    
