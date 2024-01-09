
import random

user_input_options = set()
inventory = set()
enemies_killed = set()

curr_room = "1"
health = 3
attack_mult = 1
defense_mult = 1

# {Rm number: (item in room, enemy in room, (room connections))}
rooms = { \
    "1":(None, None, ("2", "3")), \
    "2":("sword", None, ("1", "4", "3")), \
    "3":(None, "dragon", ("1", "2", "5")), \
    "4":(None, "skeleton", ("2", "5")), \
    "5":("shield", "ghoul", ("3", "4")) \
}

def get_user_input(message, list_of_possible_responses):
    user_input = str()
    while len(user_input) == 0 or user_input not in list_of_possible_responses:
        user_input = input(message).lower()
    print()
    
    return user_input

print()
print(f"Welcome to the CLI RPG game! You have {health} health.")
print()

while True:

    item_in_room, enemy, rm_connections_tuple = rooms[curr_room]

    print(f"You are in room {curr_room}.")

    if enemy is not None:
        
        equip = get_user_input(f"There is a {enemy}! Do you wish to equip your items? (y/n): ", ("y", "n"))

        if equip == "y":
            
            if len(inventory) == 0:
                print("You have no items.")
            else:
                if "sword" in inventory:
                    attack_mult = 2
                    print("Sword equipped.")
                if "shield" in inventory:
                    defense_mult = 2
                    print("Shield equipped.")

        fight = get_user_input(f"Do you wish to fight the {enemy}? (y/n): ", ("y", "n"))
        
        if fight == "n":
            print("You put your items back into your inventory.")
        else:

            hero_attack = random.randint(1, 5) * attack_mult
            hero_defense = random.randint(1, 5) * defense_mult

            enemy_attack = random.randint(1, 5)
            enemy_defense = random.randint(1, 5)

            print(f"The {enemy} attacks for {enemy_attack}!")
            print(f"You defend the attack with {hero_defense}!")
            print(f"You counterattack for {hero_attack} attack!")

            e_attack = enemy_attack - hero_defense
            if e_attack > 0:
                health -= e_attack
                print(f"You are wounded for {e_attack}!")
            else:
                print("You defend against the attack!")
            
            attack = hero_attack - enemy_defense
            if attack > 0:
                enemies_killed.add(enemy)
                print(f"You killed the {enemy}!")
            else:
                print(f"The {enemy} defends against the attack!")

            if health <= 0:
                print("You died! Game over...")
                break
            elif len(enemies_killed) == 3:
                print("You have killed all enemies. You win!")
                break
            else:
                print(f"You have {health} left.")
    
    explore = get_user_input(f"Would you like to explore the room? (y/n): ", ("y", "n"))

    if explore == "y" and (item_in_room is None or item_in_room in inventory):
        print("There are no items in this room.")
    elif explore == "y":
        inventory.add(item_in_room)
        print(f"You found a {item_in_room} and added it to your inventory.")

    curr_room = get_user_input(f"Please pick which room you would like to go to - {str(rm_connections_tuple)}", rm_connections_tuple)
