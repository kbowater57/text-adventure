# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 15:25:13 2019

@author: kbowa
This will contain a basic text adventure game.
"""

def move(direction,character,room):
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
    
    if (proposed_location.real not in list(range(int(room.real))) or
        int(proposed_location.imag) < 0 or int(abs(proposed_location.imag)) 
        not in list(range(int(abs(room.imag))))):
        
        print("You just walked into a wall. Ouch! You take 1 damage.")
        character["health"] -= 1
        return character
    else:
        character["location"] = proposed_location
        display_location(character)
        return character

def display_location(character):
    print(("You are at co-ordinate (" + str(int(character["location"].imag)) + ", " + 
        str(int(character["location"].real)) + ") in room " + str(character["roomno"]) + ". Room " +
        str(character["roomno"]) + " is " + str(int(character["roomsize"].real)) 
        + " wide by " + str(int(character["roomsize"].imag)) + " deep."))
    
def stat(character):
    display_location(character)
    print("You have " + str(character["health"]) + " hitpoints remaining.")
    
def help_text():
    help = open("help.txt","r")
    for line in help:
        print(line)
    help.close()
    
def room_desc(character):
    room_text = "room" + str(character["roomno"]) + ".txt"
    text = open(room_text,"r")
    for line in text:
        print(line)
    text.close()
    


def add_room(corner_dict,room_point_set):
        for xcoord in range((int(corner_dict["corner_sw"].real)),
                             (int(corner_dict["corner_ne"].real+1))):
            for ycoord in range((int(corner_dict["corner_sw"].imag)),
                             (int(corner_dict["corner_ne"].imag+1))):
                room_point_set.add(complex(xcoord,ycoord))
        return room_point_set
    
room_point_set=set()
room1_dict = {"corner_ne": (4+5j),"corner_sw": (0+0j)}
room2_dict = {"corner_ne": (-1+2j),"corner_sw": (-6+2j)}

    
room_point_set = add_room(room1_dict,room_point_set)
room_point_set = add_room(room2_dict,room_point_set)

character = {"location":0+0j,"health":2, "inv":{"sword":10}}


room_desc(character)
help_text()

    
    
quest_complete = 0
while quest_complete == 0:
    if character["health"] <=0:
        print("Oh no! You died. Better luck next time!")
        break
    requested_action = input("What would you like to do? \n")
    if requested_action[0:5] == "move ":
        character = move(requested_action[5:],character,room1)
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
    
