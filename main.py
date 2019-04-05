# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 15:25:13 2019

@author: kbowa
This will contain a basic text adventure game.
"""

def move(character,room):
    direction = input("In which direction (n,e,s,w) would you like to move?\n")
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
    if proposed_location.real not in list(range(int(room.real))):
        print("You just walked into a wall. Ouch! You take 1 damage.")
        character["health"] -= 1
        return character
    elif int(proposed_location.imag) < 0 or int(abs(proposed_location.imag)) not in list(range(int(abs(room.imag)))):
        print("You just walked into a wall. Ouch! You take 1 damage.")
        character["health"] -= 1
        return character
    else:
        display_location(proposed_location,character["roomno"])
        character["location"] = proposed_location
        return character

def display_location(location, roomno):
    print("You are at co-ordinate (" + str(int(location.imag)) + ", " + str(int(location.real)) + ") in room " + str(roomno) + "." )
    
def stat(character):
    display_location(character["location"])
    print("You have " + character["health"] + " hitpoints remaining.")
    
    
room1 = 4 + 5j
character = {"location":0+0j,"health":2,"roomno":1, "roomsize":room1}

#print(current_location["x"] in list(range(room1["length"])))

intro_text = open("intro.txt","r")
for line in intro_text:
    print(line)
quest_complete = 0
while quest_complete == 0:
    if character["health"] <=0:
        print("Oh no! You died. Better luck next time!")
        break
    requested_action = input("What would you like to do? \n")
    if requested_action == "move":
        character = move(character,room1)
    elif requested_action == "die":
        print("Oh no! You died. Better luck next time!")
        break
    elif requested_action == "stat":
        stat
    else:
        print("I don't know how to " + requested_action + ".")
    
