# Build a CLI RPG game following the instructions from the course.

# Ask the player for their name.

# Display a message that greets them and introduces them to the game world.

# Present them with a choice between two doors.

# If they choose the left door, they'll see an empty room.

# If they choose the right door, then they encounter a dragon.
 
# In both cases, they have the option to return to the previous room or interact further.

# When in the seemingly empty room, they can choose to look around. If they do so, they will find a sword. They can choose to take it or leave it.

# When encountering the dragon, they have the choice to fight it.

# If they have the sword from the other room, then they will be able to defeat it and win the game.

# If they don't have the sword, then they will be eaten by the dragon and lose the game.

name = input("Please enter your name: ")
print(f"Hello, {name}! Welcome to our Dungeons and Dragons game!")

next_room = 1
sword_acquired = False
look_around = False
fight = False
ret = False
cont = False

def get_user_input(message, str_of_posible_responses):
    user_input = str()
    while len(user_input) == 0 or user_input not in str_of_posible_responses:
        user_input = input(message).lower()
    print()
    
    return user_input

while True:
    
    if fight and sword_acquired:

        print("You vanquished the dragon with your sword! You have won the game!")
        break
        
    elif fight:

        print("The dragon has eaten you. You lose...")
        break
    
    elif look_around:

        sword_acquired = (get_user_input("You have found a sword! Do you (t)ake it or (l)eave it?: ", "tl") == "t")
        look_around = False
    
    elif ret:
            
        next_room = 1
        ret = False

    elif cont and next_room == 2:
                
        look_around = (get_user_input("Would you like to look around? y/n): ", "yn") == "y")
        cont = False
                           
    elif cont and next_room == 3:
        
        fight = (get_user_input("Do you wish to fight the dragon? y/n: ", "yn") == "y")
        cont = False

    elif next_room == 1:
        
        door = get_user_input("Please pick a door to walk through - (L)eft or (R)ight: ", "lr")
        
        if door == "l":
            next_room = 2
        else:
            next_room = 3
        
    else:

        if next_room == 2:
            print("You walk into an empty room.")        
        elif next_room == 3:
            print("You walk into a room guarded by a fearsome dragon!")
        
        return_continue = get_user_input("Would you like to (R)eturn to the previous room or (C)ontinue further? ", "rc")

        ret = (return_continue == "r")
        cont = not ret