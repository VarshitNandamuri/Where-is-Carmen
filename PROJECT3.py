"""
File: carmen.py
Author: NANDAMURI SAI VARSHIT
Date:   14 may 2021
Section: 22 DIS
E-mail: s299@umbc.edu
Description:
this programm is a game to catch carmen by visiting different places and people and using their clues
to navigate carmen sandeigo.
"""
import json

def load_game(game_file_name):
    try:
        # Try to open and load the game file
        with open(game_file_name) as game_file:
            game = json.loads(game_file.read())
    except FileNotFoundError:
        print('That file does not exist. ')
        return None

    return game

def create_location(connections, starts_locked, carmen):
    """
    Create a location dictionary with the provided connections, start lock status, and Carmen's presence.

    Args:
    connections (list): List of connections to other locations.
    starts_locked (bool): Status of whether the location is locked at the beginning.
    carmen (bool): Status of Carmen's presence in the location.

    Returns:
    dict: A dictionary representing the location.
    """
    return {'connections': connections,
            'starts_locked': starts_locked,
            'carmen': carmen,
            'people': [],
            'clues': []}

def build_world(locations, people, clues, game_map):
    """
    Build the game world based on the provided data.

    Args:
    locations (dict): Dictionary containing location data.
    people (dict): Dictionary containing people data.
    clues (dict): Dictionary containing clues data.
    game_map (dict): Dictionary to store the built game world.
    """
    # Create locations
    for location_name, data in locations.items():
        connections = data['connections']
        starts_locked = data['starts-locked']
        carmen = data['carmen']
        game_map[location_name] = create_location(connections, starts_locked, carmen)

    # Add people to the locations
    for person, person_info in people.items():
        add_person(game_map, person, person_info)

    # Add clues to the locations
    for clue, clue_info in clues.items():
        add_clue(game_map, clue, clue_info)

def add_person(game_map, person, person_info):
    """
    Add a person to the game map.

    Args:
    game_map (dict): Dictionary representing the game world.
    person (str): Name of the person.
    person_info (dict): Information about the person.
    """
    person_data = {person: person_info}
    person_data[person]['talk_flag'] = False
    game_map[person_info['location']]['people'].append(person_data)

def add_clue(game_map, clue, clue_info):
    """
    Add a clue to the game map.

    Args:
    game_map (dict): Dictionary representing the game world.
    clue (str): Name of the clue.
    clue_info (dict): Information about the clue.
    """
    clue_data = {clue: clue_info.copy()}
    clue_data[clue]['invest_flag'] = False
    game_map[clue_info['location']]['clues'].append(clue_data)

def display_locations(locations):
    """
    Display all available locations.

    Args:
    locations (dict): Dictionary containing location data.
    """
    location_names = list(locations.keys())
    location_index = 0
    while location_index < len(location_names):
        print(location_names[location_index])
        location_index += 1

def display_people(starting_place, game_map):
    """
    Display people at a given location.

    Args:
    starting_place (str): Name of the location.
    game_map (dict): Dictionary representing the game world.
    """
    starting_place = starting_place.capitalize()
    people_info = game_map[starting_place]['people']
    person_index = 0

    while person_index < len(people_info):
        key, value = list(people_info[person_index].items())[0]
        if not value['starts-hidden']:
            if value['talk_flag']:
                print(f'{key}    {value["conversation"]}')
            else:
                print(f'{key}    Not Spoken To Yet')
        person_index += 1

def display_clues(starting_place, game_map):
    """
    Display clues at a given location.

    Args:
    starting_place (str): Name of the location.
    game_map (dict): Dictionary representing the game world.
    """
    starting_place = starting_place.capitalize()
    clue_info = game_map[starting_place]['clues']
    clue_index = 0
    while clue_index < len(clue_info):
        key, value = list(clue_info[clue_index].items())[0]
        if not value['starts-hidden']:
            if value['invest_flag']:
                print(f'{key}    {value["clue-text"]}')
            else:
                print(f'{key}    Hidden')
        clue_index += 1

def talk_to_person(starting_place, person_name, game_map):
    """
    Initiate a conversation with a person.

    Args:
    starting_place (str): Name of the current location.
    person_name (str): Name of the person to talk to.
    game_map (dict): Dictionary representing the game world.

    Returns:
    bool: True if the conversation was successful, False otherwise.
    """
    starting_place = starting_place.capitalize()
    loc_info = game_map[starting_place]
    people_info = loc_info['people']
    check_flag = True
    index = 0

    while index < len(people_info) and check_flag:
        person = people_info[index]
        key, value = list(person.items())[0]
        if key.lower() == person_name:
            value['talk_flag'] = True
            value['starts-hidden'] = False

            unlock_location(value['unlock-locations'], game_map)
            unlock_people(value['unlock-people'], game_map)
            unlock_clues(value['unlock-clues'], game_map)
            print(value['conversation'])
            check_flag = False
            return True
        index += 1

    if check_flag:
        print(f'You cannot talk to {person_name}')
        return False

def unlock_location(location_list, game_map):
    """
    Unlock a list of locations.

    Args:
    location_list (list): List of locations to unlock.
    game_map (dict): Dictionary representing the game world.
    """
    index = 0
    while index < len(location_list):
        game_map[location_list[index]]['starts_locked'] = False
        index += 1

def unlock_people(people_list, game_map):
    """
    Unlock a list of people.

    Args:
    people_list (list): List of people to unlock.
    game_map (dict): Dictionary representing the game world.
    """
    for city, data in game_map.items():
        person_index = 0
        while person_index < len(data['people']):
            key, value = list(data['people'][person_index].items())[0]
            if key.capitalize() in people_list:
                value['starts-hidden'] = False
            person_index += 1

def unlock_clues(unlock_clue_list, game_map):
    """
    Unlock a list of clues.

    Args:
    unlock_clue_list (list): List of clues to unlock.
    game_map (dict): Dictionary representing the game world.
    """
    index = 0
    unlock_clue_list = [val.lower() for val in unlock_clue_list]
    while index < len(game_map):
        clue_info = list(game_map.values())[index]['clues']
        clue_index = 0
        while clue_index < len(clue_info):
            key, value = list(clue_info[clue_index].items())[0]
            if key.lower() in unlock_clue_list:
                value['starts-hidden'] = False
            clue_index += 1
        index += 1

def investigate_location(starting_place, dest_name, game_map):
    """
    Investigate if a location is reachable from the starting place.

    Args:
    starting_place (str): Name of the starting location.
    dest_name (str): Name of the destination location.
    game_map (dict): Dictionary representing the game world.

    Returns:
    bool: True if the location is reachable, False otherwise.
    """
    return can_go(starting_place.capitalize(), dest_name.capitalize(), game_map)

def can_go(start, end, game_map, visited=None):
    """
    Check if a location is reachable from another location.

    Args:
    start (str): Name of the starting location.
    end (str): Name of the destination location.
    game_map (dict): Dictionary representing the game world.
    visited (set, optional): Set of visited locations. Defaults to None.

    Returns:
    bool: True if the destination is reachable from the starting location, False otherwise.
    """
    if visited is None:
        visited = set()
    visited.add(start)
    if start == end:
        return True
    for neighbor in game_map[start]['connections']:
        if neighbor not in visited and not game_map[neighbor]['starts_locked']:
            if can_go(neighbor, end, game_map, visited):
                return True
    return False

def investigate_clue(clue_name, game_map):
    """
    Investigate a clue.

    Args:
    clue_name (str): Name of the clue.
    game_map (dict): Dictionary representing the game world.

    Returns:
    bool: True if the clue is successfully investigated, False otherwise.
    """
    for city, data in game_map.items():
        clue_info = data['clues']
        for clue_data in clue_info:
            key, value = list(clue_data.items())[0]
            if key.lower() == clue_name:
                if not value['starts-hidden']:
                    unlock_location(value['unlock-locations'], game_map)
                    unlock_people(value['unlock-people'], game_map)
                    unlock_clues(value['unlock-clues'], game_map)
                    value['invest_flag'] = True
                    print(value['clue-text'])
                    return True
                else:
                    print(f'You are unable to investigate the clue {key}')
                    return False
    print(f'Clue {clue_name} not found!')
    return False


def catch_check(starting_place, game_map):
    """
    Check if Carmen Sandiego is caught.

    Args:
    starting_place (str): Name of the current location.
    game_map (dict): Dictionary representing the game world.

    Returns:
    bool: True if Carmen Sandiego is caught, False otherwise.
    """
    if game_map[starting_place.capitalize()]['carmen']:
        print('You have caught Carmen Sandiego! You win the game!')
        return True
    else:
        print('You have not caught Carmen Sandiego!')
        return False

def carmen_sandiego(game_file_name):
    """
    Main function to run the Carmen Sandiego game.

    Args:
    game_file_name (str): Name of the game file.
    """
    game_map = {}
    if load_game(game_file_name):
        build_world(load_game(game_file_name)['locations'], load_game(game_file_name)['people'], load_game(game_file_name)['clues'], game_map)
        print('You are at: Rome')
        starting_place = load_game(game_file_name)['starting-location']
        while True:
            command = input('What would you like to do? ').lower()
            if command == 'quit' or command == 'exit':
                return

            if command == 'display locations':
                display_locations(load_game(game_file_name)['locations'])
            if command == 'display people':
                display_people(starting_place, game_map)
            if command == 'display clues':
                display_clues(starting_place, game_map)
            if command.startswith('talk to'):
                person_name = command.split(' ')[-1]
                talk_to_person(starting_place, person_name, game_map)
            if command.startswith('go to'):
                dest_name = command.split(' ')[-1]
                go_flag = investigate_location(starting_place, dest_name, game_map)
                if go_flag:
                    starting_place = dest_name
                    print('You have travelled to {}'.format(dest_name.capitalize()))
                else:
                    print('You are unable to travel to {}'.format(dest_name.capitalize()))
            if command.startswith('investigate the'):
                clue_name = command.split(' ')[-1]
                investigate_clue(clue_name, game_map)
            elif command.startswith('catch'):
                if catch_check(starting_place, game_map):
                    return

if __name__ == '__main__':
    game_file_name = input('Which game do you want to play? ')
    carmen_sandiego(game_file_name)
