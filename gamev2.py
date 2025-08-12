import keyboard
import os
import time
import sys
import shutil
import random
import copy
def slowprint(s, t=10):
     for c in s + '\n':
          sys.stdout.write(c)
          sys.stdout.flush()
          time.sleep(1/t)

os.system('CLS')
# creating the field on which the game will be played
field = [[_ for _ in range(20 + 1)]  for _ in range(20 + 1)]
# getting the lowest and the highest numbers from list above, for simplicity reasons
def max_i_j_number_in_field(field):
    max_i = None
    max_j = None
    for i in range(len(field[0])):
        i_list = [i]
        
        for j in range(len(field)):
            j_list = [j]
            max_i = i_list[-1]
            max_j = j_list[-1]
    return max_i, max_j

max_i_number = max_i_j_number_in_field(field)
max_j_number = max_i_j_number_in_field(field)
for i in range(len(field[0])):
    for j in range(len(field)):
        if field[i][j] != range(1,max_i_number[0]):
            field[i][j] = " "
        if i == 0:
            field[0][j] = "#"
        elif j == 0:
            field[i][0] = '#'
        elif j == max_j_number[1]:
            field[i][max_j_number[1]] = '#'
        elif i == max_i_number[0]:
             field[max_i_number[0]][j] = "#"
        
print(field)
inventory = {
    'inventory_slots': {}
}

equipment_slots = {
    'equipment': {'helm_slot': None, 'chestpiece_slot': None, 'neck_slot': None, 'right_arm_slot':None, 'left_arm_slot': None, 'leg_slot': None, 'boot_slot': None, 'right_ring_slot': None, 'left_ring_slot': None}
}
characters_and_stats= {
    'warrior': {'strenght': 5, 'intelligence': 1, 'dexterity': 2, 'hp': 10, 'experience': 0,  'description': 'warrior: uses 2h weapons and has the highest health pool'},

    'mage': {'strenght': 1, 'intelligence': 5, 'dexterity': 3, 'hp': 5, 'experience': 0, 'description': 'mage: can cast powerfull spells, but has the lowest health pool'},

    'ranger': {'strenght': 2, 'intelligence': 2, 'dexterity': 5, 'hp': 8, 'experience': 0, 'description': 'ranger: uses bows and is a lot more survivable then a mage'}
}


enemys = {
     'goblin': {'strength': 1, 'intelligence': 1, 'dexterity': 1, 'hp': 5, 'description': 'most common of enemys that can be met.', 'monster_type': 'common', 'location': [], 'name_on_map': 'G', 'monster_id': 0},
     'goblin_boss': {'strength': 10, 'intelligence': 3, 'dexterity': 4, 'hp': 20, 'description': '', 'monster_type': 'boss', 'location': [], 'name_on_map': 'B', 'monster_id': 10}
}
general_items = {
    
    'apple': {'item_category': 'food', 'health_amount': 2, 'item_id': 1, 'chance_to_drop': range(4+1)},
    'coins': {'item_category': 'currency', 'amount': 0, 'item_id': 2}
    }
common_items = {
    'bronze_helm': {'strenght': 2, 'intelligence': 0, 'dexterity': 1, 'defence': 5, 'weight': 1, 'item_type': 'Heavy','item_category': 'helmet', 'common_item_id': 2, 'chance_to_drop': range(4+1)},
    'bronze_chestplate': {'strenght': 3, 'intelligence': 0, 'dexterity': 1, 'defence': 15, 'weight': 3, 'item_type': 'Heavy','item_category': 'chest_piece', 'common_item_id': 1, 'chance_to_drop': range(15+1)},
    'bronze_sword': {'strenght': 2, 'intelligence': 0, 'dexterity': 1, 'attack': 5, 'weight': 1, 'item_type': 'weapon','item_category': 'sword','if_equipable': True, 'common_item_id': 0, 'chance_to_drop': range(7+1)},
}

rare_items = {
    'mail_fullhelm': {'strenght': 4, 'intelligence': 0, 'dexterity': 1, 'defense': 10, 'weight': 2, 'item_category': 'chest_piece', 'item_type': 'heavy', 'item_id': 6}
}

def monster_type(enemy_killed):

    if enemys[enemy_killed]['monster_type'] == 'boss':
            return enemy_killed
    elif enemys[enemy_killed]['monster_type'] == 'common':
            return enemy_killed
    return False
# amount of gold drop
def random_amount_of_gold(enemy_name):
    
    if enemys[enemy_name]['monster_type'] == 'boss':
        
        return random.randint(10, 20)
    else:
        return random.randint(1, 5)
# drop system 
def drops(enemy_killed):
        enemy_location = enemy_killed[0]
        enemy_type = enemy_killed[1]
        if enemys[enemy_type]['monster_type'] == 'common':
            for key, value in general_items.items():
                if key == 'coins':
                    if 'coins' not in inventory['inventory_slots']:
                        amount = random_amount_of_gold(enemy_type)
                        print(f'You have found {amount} of coins!')
                        inventory['inventory_slots']['coins'] = amount
                    elif 'coins' in inventory['inventory_slots']:
                        amount = random_amount_of_gold(enemy_type)
                        print(f'The {enemy_type} has dropped {amount} of coins!')
                        inventory['inventory_slots']['coins'] += amount
                        check_amount = inventory['inventory_slots']['coins']
                        print(f'you now have {check_amount}')
                elif random.choice(value['chance_to_drop']) == random.randrange(5):
                    if 'apple' not in inventory['inventory_slots']:
                        amount = 2
                        print(f'The monster has dropped {amount} apple!')
                        inventory['inventory_slots']['apple'] = amount
                    elif 'apple' in inventory['inventory_slots'] and inventory['inventory_slots']['apple'] < 10:
                        amount = 2
                        print(f'The monster has dropped {amount} apple!')
                        inventory['inventory_slots']['apple'] += amount
                        check_amount = inventory['inventory_slots']['apple']
                        print(f'you now have {check_amount}')
                    else:
                        print('You cannot carry any more apples!')
            if random.randint(1,2) == 2:
                    for item_name, value in common_items.items():
                        if random.choice(value['chance_to_drop']) == random.randrange(20):
                            if item_name not in inventory['inventory_slots']:
                                amount = 1
                                print(f'You have found a {item_name}'.replace("_", " "))
                                inventory['inventory_slots'][item_name] = amount
                            elif key in inventory['inventory_slots']:
                                amount = 1
                                print(f'You have found another {item_name}'.replace("_", " "))
                                inventory['inventory_slots'][item_name] += amount

        if enemys[enemy_type]['monster_type'] == 'boss':
            for key, value in general_items.items():
                if key == 'coins':
                    if 'coins' not in inventory['inventory_slots']:
                        amount = random_amount_of_gold(enemy_type)
                        print(f'You have found {amount} of coins!')
                        inventory['inventory_slots']['coins'] = amount
                    elif 'coins' in inventory['inventory_slots']:
                        amount = random_amount_of_gold(enemy_type)
                        print(f'The {enemy_type} has dropped {amount} of coins!')
                        inventory['inventory_slots']['coins'] += amount
                        check_amount = inventory['inventory_slots']['coins']
                        print(f'you now have {check_amount}')
                elif random.choice(value['chance_to_drop']) == random.randrange(5):
                    if 'apple' not in inventory['inventory_slots']:
                        amount = 2
                        print(f'The monster has dropped {amount} apple!')
                        inventory['inventory_slots']['apple'] = amount
                    elif 'apple' in inventory['inventory_slots'] and inventory['inventory_slots']['apple'] < 10:
                        amount = 2
                        print(f'The monster has dropped {amount} apple!')
                        inventory['inventory_slots']['apple'] += amount
                        check_amount = inventory['inventory_slots']['apple']
                        print(f'you now have {check_amount}')
                    else:
                        print('You cannot carry any more apples!')
            if random.randint(1,2) == 2:
                    for item_name, value in common_items.items():
                        if random.choice(value['chance_to_drop']) == random.randrange(10):
                            if item_name not in inventory['inventory_slots']:
                                amount = 1
                                print(f'You have found a {item_name}'.replace("_", " "))
                                inventory['inventory_slots'][item_name] = amount
                            elif key in inventory['inventory_slots']:
                                amount = 1
                                print(f'You have found another {item_name}'.replace("_", " "))
                                inventory['inventory_slots'][item_name] += amount


def item_equip():
    item_name = None
    for key, value in inventory['inventory_slots'].items():
        if key in common_items:
            equip = input('Item can be equipped! Would you like to equipt it now ? If yes press y, if no press n > ')
            if equip.lower() == 'y':
                for slot, value1 in equipment_slots['equipment'].items():  
                    if slot == 'helm_slot' and common_items[key]['item_category'] == 'helmet':
                        item_name = key
                        equipment_slots['equipment'][slot] = key
                        break
                    elif slot == 'chestpiece_slot' and common_items[key]['item_category'] == 'chestpiece':
                        item_name = key
                        equipment_slots['equipment'][slot] = key
                        break
                    elif slot == 'neck_slot':
                        item_name = key
                        equipment_slots['equipment'][slot] = key
                        break
                    elif slot == 'right_arm_slot':
                        item_name = key
                        equipment_slots['equipment'][slot] = key
                        break
                    elif slot == 'left_arm_slot':
                        item_name = key
                        equipment_slots['equipment'][slot] = key
                        break
                    elif slot == 'leg_slot':
                        item_name = key
                        equipment_slots['equipment'][slot] = key
                        break
                    elif slot == 'boot_slot':
                        item_name = key
                        equipment_slots['equipment'][slot] = key
                        break
                    elif slot == 'right_ring_slot':
                        item_name = key
                        equipment_slots['equipment'][slot] = key
                        break
                    elif slot == 'left_ring_slot':
                        item_name = key
                        equipment_slots['equipment'][slot] = key
                        break
                    elif slot == 'cape_slot':
                        item_name = key
                        equipment_slots['equipment'][slot] = key
                        break
                    elif equip.lower() == 'n':
                        break
   
    del inventory['inventory_slots'][item_name]
            
#item unequip
def item_unequip():
    
    for key, value in equipment_slots['equipment'].items():
        if value != None:
            ask = input('Would you like to unequip one of your items ? For yes press y, for no press n > ')
            if ask.lower() == 'y':
                piece = input('What piece you would like to unequip ? For helmet, press 1, for chestpiece, press 2 > ')
                if int(piece) == 2:
                    item = equipment_slots['equipment'][key]
                    inventory['inventory_slots'][item] = 1 
    
                    equipment_slots['equipment'][key] = None
                    break
            elif ask.lower() == 'n':
                break
# character choice
def character_choice():
    warrior_description = []
    mage_description = []
    ranger_description = []
    for key, value in characters_and_stats.items():
        if key == 'warrior':
            warrior_description.append(value['description'])
        elif key == 'mage':
            mage_description.append(value['description'])
        elif key == 'ranger':
            ranger_description.append(value['description'])
    preview_classes = input("If you would like to preview characters, please type P if no press enter: > ")
    if preview_classes.lower() == 'p':
        print(f'{warrior_description}'.replace("[", "").replace("]", "").replace("'", ""))
        print(f'{mage_description}'.replace("[", "").replace("]", "").replace("'", ""))
        print(f'{ranger_description}'.replace("[", "").replace("]", "").replace("'", ""))
    choice = input("choose by typing W, M or R: > ")
    if choice.lower() == 'w':
        print("You have choosen warrior")
        #print(f'{warrior_description}'.replace("[", "").replace("]", "").replace("'", ""))
        return choice
    elif choice.lower() == "m":
        print("You have choosen mage!")
        #print(f'{mage_description}'.replace("[", "").replace("]", "").replace("'", ""))
        return choice
    elif choice.lower() == "r":
        print("You have choosen ranger!")
        #print(f'{ranger_description}'.replace("[", "").replace("]", "").replace("'", ""))
        return choice
    else:
        print("Please choose a character")
        return character_choice()
# printing visible board
def print_field(field, player_name):
    
    
    for i in range(len(field)):
        
        if i == 0:
            print("#" * len(field * 2) + '#')
        elif i == max_i_number[0]:
            print("#" * len(field * 2 ) + '#')
        elif i != 0 and i != max_i_number[0]:
            print("#" + str(field[i]).replace("[","").replace("'","").replace("]","").replace(",","") + "#")
# enemy stats for combat purposes, one lane implementation
def enemy_stats(enemy_name=None):
    for key, value in enemys.items():
        if enemy_name.lower() == 'g' and key == 'goblin':
            enemy_name = 'goblin'
    enemy_strength = [value for key, value in enemys[enemy_name].items() if key == 'strength']
    enemy_intelligence = [value for key, value in enemys[enemy_name].items() if key == 'intelligence']
    enemy_dexterity = [value for key, value in enemys[enemy_name].items() if key == 'dexterity']
    enemy_hp = [value for key, value in enemys[enemy_name].items() if key == 'hp']

    return enemy_strength, enemy_intelligence, enemy_dexterity, enemy_hp
#Player stats for future implementations for combat purposes
def player_stats(character_class):
    player_strength = 0
    player_intelligence = 0
    player_dexterity = 0
    player_hp = 0
    if character_class == 'w': 
        for key, value in characters_and_stats['warrior'].items():
            
            if key == 'strenght':
                player_strength = value
            elif key == 'intelligence':
                player_intelligence = value
            elif key == 'dexterity':
                player_dexterity = value
            elif key == 'hp':
                player_hp = value
    
    elif character_class == 'm':
        for key, value in characters_and_stats['mage'].items():
            if key == 'strenght':
                player_strength = value
            elif key == 'intelligence':
                player_intelligence = value
            elif key == 'dexterity':
                player_dexterity = value
            elif key == 'hp':
                player_hp = value

    elif character_class == 'r':
        for key, value in characters_and_stats['ranger'].items():
            if key == 'strenght':
                player_strength = value
            elif key == 'intelligence':
                player_intelligence = value
            elif key == 'dexterity':
                player_dexterity = value
            elif key == 'hp':
                player_hp = value
    
    return player_strength, player_intelligence, player_dexterity, player_hp
#checking player location
def check_location_of_Player(field, player_name):
    location = []
    for i in range(len(field[0])):
        for j in range(len(field)):
            if field[j][i] == 'P':
                location = (j, i)
                print('Found player!')
    
    return location
#checking for enemy locations for combat moves
def check_enemy_location(field):
    locations = []
    for i in range(len(field[0])):
        for j in range(len(field)):
            if field[j][i] == "G" or field[j][i] == "B":
                location = (j, i)
                locations.append(location)
                print('Found enemy!')
                for key, value in enemys.items():
                    
                    if  enemys[key]['name_on_map'] == 'g' and field[j][i] == "G" and enemys[key]['location'] == None:
                        enemys[key]['location'] = (j, i)
                        break
                    elif enemys[key]['name_on_map'] == 'b' and field[j][i] == "B":
                        enemys[key]['location'] = (j,i)
                        

    return locations
#checking for empty location for possible moves for player
def check_empty_locations(field):
    empty_locations = []
    for i in range(len(field[0])):
        for j in range(len(field)):
            if field[j][i] == " ":
                location = j, i
                empty_locations.append(location)

    return empty_locations
#combat function, not fully implemented yet
def combat(enemy, player, loc):
    

    for key in enemys.keys():
        for name_on_map in enemys[key]['name_on_map']:
            if name_on_map.lower() == 'b' and enemy.lower() == 'b':
                defeated_enemy_location = loc
                enemy_name = key
                return defeated_enemy_location, enemy_name 
            
            elif name_on_map.lower() == 'g' and enemy.lower() == 'g':
                defeated_enemy_location = loc
                enemy_name = key
                return defeated_enemy_location, enemy_name 
        

    return False
# player movement function
def player_movement(field, player_location, empty_locations, enemy_locations, player_name):
    player = player_location
    if_empty = player_location
    empty_location = empty_locations
    
    while True:
        try:
            # check if key has been pressed up
            if keyboard.is_pressed('up') and player[0] >= 1:
                    time.sleep(0.1)
                    #Convert tuple to list to check if possible to move up
                    player = list(player)
                    player[0] = player[0] - 1
                    player = tuple(player)
                    # if not possible, return a message and remain in the location 
                    if player[0] == 0:
                        print("You have hit a rock! Cannot move up!")
                        player = player_location
                    elif player in empty_location:

                            print('Location is empty!')
                            field[player[0]][player[1]] = player_name
                            field[if_empty[0]][if_empty[1]] = ' '
                            break
                    

                    elif player in enemy_locations:

                        
                        print("Prepare to fight!")
                        for key, value in enemys.items():
                            locations = value['location']
                            
                            for loc in locations:
                                if loc == player:
                                    print(f'player is in: {player}')
                                    location = loc
                                    
                                            
                                    enemy = enemys[key]['name_on_map']
                            break
                        enemy_killed = combat(enemy, player, location)
                        # To be implemented combat system, only basic drop system working
                        if enemy_killed:
                            
                            field[enemy_killed[0][0]][enemy_killed[0][1]] = ' '
                            field[player[0]][player[1]] = player_name
                            field[if_empty[0]][if_empty[1]] = ' '
                            drop = drops(enemy_killed)
                        return drop
                        
            # check if key has been pressed down
            elif keyboard.is_pressed('down') and player[0] <= max_i_number[0]:
                    time.sleep(0.1)
                    #Convert tuple to list to check if possible to move down
                    player = list(player)
                    player[0] = player[0] + 1
                    player = tuple(player)
                    # if not possible, return a message and remain in the location 
                    if player[0] > max_i_number[0]:
                        print("You have hit a rock! Cannot move down!")
                        player = player_location
                    elif player in empty_location:
                        
                        print('Location is empty!')
                        field[player[0]][player[1]] = player_name
                        field[if_empty[0]][if_empty[1]] = ' '
                        break
                        
                    elif player in enemy_locations:
                        for key, value in enemys.items():
                            locations = value['location']
                            
                            for loc in locations:
                                if loc == player:
                                    print(f'player is in: {player}')
                                    location = loc
                                    
                                            
                                    enemy = enemys[key]['name_on_map']
                            break
                        enemy_killed = combat(enemy, player, location)
                        # To be implemented combat system, only basic drop system working
                        if enemy_killed:
                            
                            field[enemy_killed[0][0]][enemy_killed[0][1]] = ' '
                            field[player[0]][player[1]] = player_name
                            field[if_empty[0]][if_empty[1]] = ' '
                            drop = drops(enemy_killed)
                        return drop
            # check if key has been pressed left
            elif keyboard.is_pressed('left') and player[1] >= 0:
                    time.sleep(0.1)
                    #Convert tuple to list to check if possible to move left
                    player = list(player)
                    player[1] = player[1] - 1
                    player = tuple(player)
                    # if not possible, return a message and remain in the location 
                    if player[1] < 0:
                        print("You have hit a rock! Cannot move left!")
                        player = player_location
                    # if location empty, move to location
                    elif player in empty_location:

                            print('Location is empty!')
                            field[player[0]][player[1]] = player_name
                            field[if_empty[0]][if_empty[1]] = ' '
                            break
                    # if player in enemy location
                    elif player in enemy_locations:
                        for key, value in enemys.items():
                            locations = value['location']
                            
                            for loc in locations:
                                if loc == player:
                                    print(f'player is in: {player}')
                                    location = loc
                                    
                                            
                                    enemy = enemys[key]['name_on_map']
                            break
                        # To be implemented combat system, only basic drop system working
                        enemy_killed = combat(enemy, player, location)
                        if enemy_killed:
                            
                            field[enemy_killed[0][0]][enemy_killed[0][1]] = ' '
                            field[player[0]][player[1]] = player_name
                            field[if_empty[0]][if_empty[1]] = ' '
                            drop = drops(enemy_killed)
                        return drop
            # check if key has been pressed right
            elif keyboard.is_pressed('right') and player[1] <= max_i_number[0]:
                    time.sleep(0.1)
                    #Convert tuple to list to check if possible to move right
                    player = list(player)
                    player[1] = player[1] + 1
                    player = tuple(player)
                    if player[1] > max_i_number[0]:
                        print("You have hit a rock! Cannot move right!")
                        player = player_location

                    elif player in empty_location:

                            print('Location is empty!')
                            field[player[0]][player[1]] = player_name
                            field[if_empty[0]][if_empty[1]] = ' '
                            break
                    
                    elif player in enemy_locations:
                        for key, value in enemys.items():
                            locations = value['location']
                            
                            for loc in locations:
                                if loc == player:
                                    print(f'player is in: {player}')
                                    location = loc
                                    
                                            
                                    enemy = enemys[key]['name_on_map']
                            break
                        # To be implemented combat system, only basic drop system working                 
                        enemy_killed = combat(enemy, player, location)
                        
                        if enemy_killed:
                            
                            field[enemy_killed[0][0]][enemy_killed[0][1]] = ' '
                            field[player[0]][player[1]] = player_name
                            field[if_empty[0]][if_empty[1]] = ' '
                            drop = drops(enemy_killed)
                        return drop
        except: 
            break
# taking player name, no purpose yet
def player_greeting():
    
    name = input('Please input your name: ')
    
    if not name:
        print("You have not entered your name, please enter your name")
        return player_greeting()

    return name
# adding the amount of enemys to the field
def adding_new_enemy(*enemys_to_create, enemy_count=None):
    
     enemy_amount = enemys_to_create[0]
     enemy_count = 0
     while enemy_count < enemy_amount:
          x = random.randrange(1, 19)
          y = random.randrange(1, 5)
          #checking if location is not taken
          if field[y][x] != 'G' and field[x][y] != 'B' and field[x][y] != '#':
               location = y, x
               enemys['goblin']['location'].append(location)
               field[y][x] = enemys['goblin']['name_on_map']
               enemy_count += 1
            #if taken printing that location is taken for now
          else:
               print(f'Trying new x,y location for enemy spawn! current enemy count: {enemy_count}. Location {y}{x} taken!')
               #adding_new_enemy(*enemys_to_create, enemy_count)

def run():
    print("Welcome!")
    print(f'Hi {player_greeting()}!')
    print('You can choose from 3 characters, warrior, mage, ranger. They will be represented as W, M or R on the map respectively.\nRegular enemys will be represtented as E and boss enemys with B.')
    character_class = character_choice()
    
    if character_class == 'w':
        characters_and_stats['warrior']
    elif character_class == 'r':
         characters_and_stats['ranger']
    elif character_class == 'm':
         characters_and_stats['mage']
    
    field[7][6] = 'P'
    field[5][6] = enemys['goblin_boss']['name_on_map']
    enemys['goblin_boss']['location'] = (5,6)
    stats_of_player = player_stats(character_class)
    # printing stats of player, level up system to be implemented in later date
    print(f"These are your main stats: strenght: {stats_of_player[0]}, intelligence: {stats_of_player[1]}, dexterity: {stats_of_player[2]}, hp: {stats_of_player[3]}. \nThey can be modified with equipment and experience. You only get one point per level up.")
    moves = 0
    player_location = check_location_of_Player(field, player_name='P')

    new_field2 = (print_field(field, player_name='P'))
    while True:
        adding_new_enemy(5)
        break
    while moves < 40:   
            
            time.sleep(0.5) 
            
            print(enemys)
            #print(stats_of_player)
            enemy_locations = check_enemy_location(field)
            
            #print(enemy_locations)
            player_location = check_location_of_Player(field, player_name='P')
            #print(player_location)
            empty_locations = check_empty_locations(field)
            #print(enemys)
            player_movements = player_movement(field, player_location, empty_locations, enemy_locations, player_name='P')
            print(f"{inventory['inventory_slots']}".replace("_", " "))
            time.sleep(0.5)
            os.system('CLS')
            moves += 1
            
            new_field2 = (print_field(field, player_name='P'))
            
            
            
            continue
            
    
run()