import pathlib, random

def get_user_input(message, list_of_possible_responses):
    """
    Validates user input.

    Args:
        message: The message to the user requesting input
        list_of_possibly_responses: iterable with possible responses
    
    Returns:
        The validated user input for further processing
    """
    while True:
        user_input = input(message).lower()
        if user_input in list_of_possible_responses:
            break
    
    print()
    
    return user_input

def equip_items(user_status):
    """
    Equips user items, if any in inventory, by increasing attack/defense multipliers as appropriate.

    Args:
        user_status: The full user status dictionary, which includes the inventory
    """
    if len(user_status["inv"]) == 0:
        print("You have no items.")
    else:
        if "sword" in user_status["inv"]:
            user_status["att_mult"] = 2
            print("Sword equipped.")
        if "shield" in user_status["inv"]:
            user_status["def_mult"] = 2
            print("Shield equipped.")


def fight_enemy(user_status: dict, enemy: dict):
    """
    Executes a fight with an enemy. Alters user_status to be processed afterward.

    Args:
        user_status: The full user status dictionary
        enemy: The dictionary of information regarding the enemy to be fought
    """
    hero_attack = random.randint(0, 5) * user_status["att_mult"]
    hero_defense = random.randint(0, 5) * user_status["def_mult"]

    enemy_attack = random.randint(0, enemy["att"])
    enemy_defense = random.randint(0, enemy["def"])

    print(f"The {enemy['name']} attacks for {enemy_attack}!")
    print(f"You defend the attack with {hero_defense}!")
    print(f"You counterattack for {hero_attack} attack!")

    e_attack = enemy_attack - hero_defense
    if e_attack > 0:
        user_status["health"] -= e_attack
        print(f"You are wounded for {e_attack}!")
    else:
        print("You defend against the attack!")
    
    attack = hero_attack - enemy_defense
    if attack > 0:
        enemies_killed.add(enemy['name'])
        print(f"You killed the {enemy['name']}!")
    else:
        print(f"The {enemy['name']} defends against the attack!")

user_status =  {"room": "1", "health": 3, "att_mult": 1, "def_mult": 1, "inv": set()}
enemies_killed = set()

save_file = pathlib.Path("./save.txt")

# {Rm number: (item in room, {enemy name, att, def}, (room connections))}
rooms = { \
    "1":(None, None, ("2", "3")), \
    "2":("sword", None, ("1", "4", "3")), \
    "3":(None, {"name": "dragon", "att": 5, "def": 3}, ("1", "2", "5")), \
    "4":(None, {"name": "skeleton", "att": 3, "def": 2}, ("2", "5")), \
    "5":("shield", {"name": "ghoul", "att": 2, "def": 1}, ("3", "4")) \
}

print()
user_input = get_user_input("Welcome to the CLI RPG game! Would you like to start a (n)ew game or (c)ontinue your last game?: ", "nc")
if user_input == "c":

    try:
        with open(save_file) as f:
            user_status = eval(f.readline())
            enemies_killed = eval(f.readline())
    except FileNotFoundError:
        print("File does not exist. Starting new game.")

while True:

    print(f"You are in room {user_status['room']}.")
    user_input = get_user_input("Would you like to quit? (y/n): ", "yn")
    if user_input == "y":
        with open(save_file, "w") as f:
            f.write(str(user_status))
            f.write('\n')
            f.write(str(enemies_killed))
        
        print("Thanks for playing!")
        break

    item_in_room, enemy, rm_connections_tuple = rooms[user_status["room"]]

    if enemy is not None:
        
        equip = get_user_input(f"There is a(n) {enemy['name']}! Do you wish to equip your items? (y/n): ", ("y", "n"))

        if equip == "y":
            equip_items(user_status)
            
        fight = get_user_input(f"Do you wish to fight the {enemy['name']}? (y/n): ", ("y", "n"))
        
        if fight == "n":
            print("You put your items back into your inventory.")
        else:

            fight_enemy(user_status, enemy)

            if user_status["health"] <= 0:
                print("You died! Game over...")
                break
            elif len(enemies_killed) == 3:
                print("You have killed all enemies. You win!")
                break
            else:
                print(f"You have {user_status['health']} health left.")
    
    explore = get_user_input(f"Would you like to explore the room? (y/n): ", ("y", "n"))

    if explore == "y" and (item_in_room is None or item_in_room in user_status["inv"]):
        print("There are no items in this room.")
    elif explore == "y":
        user_status["inv"].add(item_in_room)
        print(f"You found a {item_in_room} and added it to your inventory.")

    user_status["room"] = get_user_input(f"Please pick which room you would like to go to - {str(rm_connections_tuple)}: ", rm_connections_tuple)
