# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 15:25:13 2019

@author: kbowa
This will contain a basic text adventure game.
"""

def move(current_location, room):
    direction = input("In which direction (n,e,s,w) would you like to move?")
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
        return current_location
    
    proposed_location = current_location + dir_vector
    if proposed_location.real not in list(range(int(room.real))):
        print("You just walked into a wall. Ouch! You take 1 damage.")
        current_health -= 1
        return current_location
    elif int(proposed_location.imag) < 0 or int(abs(proposed_location.imag)) not in list(range(int(abs(room.imag)))):
        print("You just walked into a wall. Ouch! You take 1 damage.")
        current_health -= 1
        return current_location
    else:
        display_location(proposed_location)
        return proposed_location

def display_location(location):
    print("You are at co-ordinate (" + str(int(location.imag)) + ", " + str(int(location.real)) + ")." )


character = {"location":0+0j,"health":10,"room":1}
room1 = 4 + 5j
current_location = 0 + 0j
current_health = 10
current_room = room1

#print(current_location["x"] in list(range(room1["length"])))

intro_text = open("intro.txt","r")
for line in intro_text:
    print(line)
quest_complete = 0
while quest_complete == 0:
    requested_action = input("What would you like to do? \n")
    if requested_action == "move":
        character["location"] = move(character["location"],room1)
    if requested_action == "die":
        break
    
