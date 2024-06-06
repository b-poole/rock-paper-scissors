# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:06:34 2024

@author: barre

Rock, Paper, Scissors game, with JSON score recording
"""
import random
import json
import logging
import os.path

hand = ["Rock", "Paper", "Scissors"]
def rps_input():
    '''Returns player's choice of rock/paper/scissors'''
    print("Rock, paper, or scissors?")
    print("a: Rock")
    print("b: Paper")
    print("c: Scissors")
    player_choice = 0
    while True:
        #loops if valid input is not recieved
        player_input = input("Enter: ")
        match player_input:
            case "a":
                player_choice = 0
                break
            case "b":
                player_choice = 1
                break
            case "c":
                player_choice = 2
                break
            case _:
                print("Invalid Input, please enter a, b, or c.")
    logger.debug("Player chose " + str(player_choice))
    return player_choice

def computer_input():
    """Returns computer's choice of rock/paper/scissors"""
    print("Computer deciding on move...")
    com_input = random.randint(0, 2)
    logger.debug("Computer chose " + str(com_input))
    return com_input

def game_logic(player, com):
    """Determine player or computer win, or a tie"""
    logger.info("Player hand: " + hand[player] + ", Computer hand: " + hand[com])
    print("Player chose " + hand[player])
    print("Computer chose " + hand[com])
    #0 is rock, 1 is paper, 2 is scissors
    #return 0 is tie, 1 is user win, 2 is computer win
    if player == com:
        #Tie
        return 0
    if any([player == 0 and com == 2,
            player == 1 and com == 0,
            player == 2 and com == 1]):
        #Player win
        return 1
    #Computer win
    return 2

def y_n_input(prompt):
    """Asks User to type 'y' or 'n'"""
    ans = ''
    while len(ans) < 1:
        #Loops until input is not an empty string
        ans = input(prompt)
    if ans.lower() == "y":
        return True
    #Any input other than 'y' is assumed to be False
    return False

def score_str(scores_dict, keyword):
    """Returns score string, useful for logging or printing"""
    return (keyword + " scores - Player: " + str(scores_dict['player'])
            + " Computer: " + str(scores_dict['computer'])
            + " Ties: " + str(scores_dict['ties']))

def overwrite_json(filename, new_json_elements):
    """Overwrites anything in .json file"""
    if not os.path.isfile(filename):
        logger.info("Creating new " + filename)
    else:
        logger.info("Overwriting " + filename)
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(new_json_elements, file)
        

def parse_json(filename):
    """Returns JSON file contents, or None if file is empty/corrupt or nonexistant"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            try:
                json_elements = json.load(file)
                logger.info("Successfully parsed " + filename)
                return json_elements
            except json.decoder.JSONDecodeError as e:
                logger.warning(str(type(e)) + ": " + filename + " is empty or corrupt")
                return None
    except FileNotFoundError as e:
        logger.warning(str(type(e)) + ": " + filename + " not found")
        return None

def game_run(scores_dict=None):
    """Gameplay loops, gets hands from player and computer, then adds score"""
    if scores_dict is None:
        scores_dict={"player": 0,
                "computer": 0,
                "ties": 0}

    com_hand = computer_input()
    user_hand = rps_input()
    win = game_logic(user_hand, com_hand)

    match win:
        case 0:
            logger.info("Tie")
            print("Tie!")
            scores_dict['ties'] += 1
        case 1:
            logger.info("Player won")
            print("Player won!")
            scores_dict['player'] += 1
        case 2:
            logger.info("Computer won")
            print("Computer won!")
            scores_dict['computer'] += 1
    logger.info("Current scores: " + str(scores_dict))
    return scores_dict

if __name__ == "__main__":
    SCORE_FILE = 'scores.json'
    
    logging.basicConfig(filename='main.log',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='a',
                        force=True)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    #Start by running gameplay loop
    scores = game_run()
    while y_n_input("Another game? y/n: "):
        #Loops game as long as player wants
        scores = game_run(scores)

    #After game ends
    logger.info(score_str(scores, "Final"))
    print(score_str(scores, "Final"))
    if y_n_input("Record score? y/n: "):
        old_scores = parse_json(SCORE_FILE)
        if old_scores == None:
            logger.warning("JSON read and parse failure, unable to get old scores")
        else:
            for score in scores:
                scores[score] += old_scores[score]
        overwrite_json(SCORE_FILE, scores)
        logger.info(score_str(scores, "Overall"))
        print(score_str(scores, "Overall"))
    print("Thanks for playing!")
    logger.handlers[0].close()
