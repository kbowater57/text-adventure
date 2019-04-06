# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 15:25:13 2019

@author: kbowa
This will contain a basic text adventure game.
"""

def move(direction,character,room_point_set):
    #direction = input("In which direction (n,e,s,w) would you like to move?\n")
    if direction == "n":
        dir_vector = 0+1j
    elif direction == "e":
        dir_vector = 1+0j
    elif direction == "s":
        dir_vector = 0-1j
    elif direction == "w":
        dir_vector = -1+0j
    else:
        print("That's not a valid direction. Try again.")
        return character
    
    proposed_location = character["location"] + dir_vector
    
    if proposed_location not in room_point_set:
        print("You just walked into a wall. Ouch! You take 1 damage.")
        character["health"] -= 1
        return character
    elif proposed_location == -10 + 7j:
        print("You approach the chest, and throw it open eagerly. A huge bounty of gold coins lies within the chest. Congratulations! You have won the game!")
        character["quest_complete"] = 1
        return character
    else:
        character["location"] = proposed_location
        return character
    """elif proposed_location == -2+2j and "torch" not in character["inv"]:
        print("You were eaten by a grue. Better bring a torch next time.")
        character["health"] = 0
        return character"""
    

def display_location(character):
    print(("You are at co-ordinate (" + str(int(character["location"].real)) + ", " + 
        str(int(character["location"].imag)) + "), in room " + 
    str(character["roomno"]) + "." ))
    
    """+ ". Room " +
        str(character["roomno"]) + " is " + str(int(character["roomsize"].real)) 
        + " wide by " + str(int(character["roomsize"].imag)) + " deep."))"""
    
def stat(character):
    display_location(character)
    print("You have " + str(character["health"]) + " hitpoints remaining.")
    
def help_text():
    help = open("help.txt","r")
    for line in help:
        print(line)
    help.close()
    
def room_desc(character):
    room_text = ("room" + str(character["roomno"]) + ".txt")
    text = open(room_text,"r")
    for line in text:
        print(line)
    text.close()
    
def check_room(character,location, room_points_dict):
    for number in range(len(room_points_dict)):
        if location in room_points_dict["room"+str(number)]:
            return number

def add_room(corner_dict,room_point_list):
        returned_list=list()
        for xcoord in range((int(corner_dict["corner_sw"].real)),
                             (int(corner_dict["corner_ne"].real+1))):
            for ycoord in range((int(corner_dict["corner_sw"].imag)),
                             (int(corner_dict["corner_ne"].imag+1))):
                returned_list.append(complex(xcoord,ycoord))
        room_point_list.extend(returned_list)
        return room_point_list
    

room0_dict = {"corner_ne": (4+5j),"corner_sw": (0+0j)}
room0_list = list()
room0_list=add_room(room0_dict,room0_list)
room1_dict = {"corner_ne": (-1+2j),"corner_sw": (-6+2j)}
room1_list = list()
room1_list=add_room(room1_dict,room1_list)
room2_dict = {"corner_ne": (-7+8j),"corner_sw": (-13+1j)}
room2_list = list()
room2_list=add_room(room2_dict,room2_list)


room_points_dict = {"room0":room0_list,"room1":room1_list,"room2":room2_list}
room_point_list=list()

    
room_point_list = add_room(room0_dict,room_point_list)
room_point_list = add_room(room1_dict,room_point_list)
room_point_list = add_room(room2_dict,room_point_list)

character = {"location":0+0j,"health":2,"roomno":0, "inv":{"sword":10}, "quest_complete":0}


room_desc(character)
help_text()

    
    

while character["quest_complete"] == 0:
    if character["health"] <=0:
        print("Oh no! You died. Better luck next time!")
        break
    old_room = character["roomno"]
    character["roomno"]= check_room(character,character["location"],room_points_dict)
    if old_room != character["roomno"]:
        room_desc(character)
    display_location(character)
    requested_action = input("What would you like to do? \n")
    if requested_action[0:5] == "move ":
        character = move(requested_action[5:],character,room_point_list)
    elif requested_action[0] == "n" and len(requested_action) == 1:
        character = move("n",character,room_point_list)
    elif requested_action[0] == "e" and len(requested_action) == 1:
        character = move("e",character,room_point_list)
    elif requested_action[0] == "s" and len(requested_action) == 1:
        character = move("s",character,room_point_list)    
    elif requested_action[0] == "w" and len(requested_action) == 1:
        character = move("w",character,room_point_list)
    elif requested_action == "die":
        print("Oh no! You died. Better luck next time!")
        break
    elif requested_action == "stat":
        stat(character)
    elif requested_action == "disp":
        display_location(character)
    elif requested_action == "help":
        help_text()
    elif requested_action == "look":
        room_desc(character)
    elif requested_action == "inv":
        print(character["inv"])
    else:
        print("I don't know how to " + requested_action + ".")
    
