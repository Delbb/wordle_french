#!/usr/bin/env python3

import sys
import os

def get_data():
    #Get input data as list of strings
    with open('data/data.txt') as f:
        lines = f.readlines()

    #clean the list : remove \n
    clean_list = []
    for line in lines:
        clean_list.append(line.lower().replace('\n',''))

    return clean_list

def give_word(words):
    for word in words:
        for i in range(0,len(word)):
            next = False
            for j in range(0,len(word)):
                if i != j and word[i] == word[j]:
                    next = True
                    break
            if next:
                break
        if not next:
            return word
    return words[0]

def process_word(letter, number, position, answer):
    #Create word variable containings all posibility for each postion 
    excluded = [""] * 5
    #Create word variable containings all posibility for each postion
    possibilities = [""] * 5
    for i in range(0,5):
        if number == 0 and not letter in answer:
            excluded[i] = letter
        elif number == 2:
            if answer[position] != "" and letter != answer[position]:
                print("Already found correct letter.")
            else:
                answer[position] = letter
                possibilities[position] = letter
            break
        elif number == 1 or letter in answer:
            if i == position:
                excluded[position] = letter
            else:
                possibilities[i] = letter
    return possibilities, excluded


def remove_words(possibilities, excluded, word_list):    
    new_list = word_list.copy()
    #parse word to see available letters, then use regexp to remove wrong entries from the list
    for word in word_list:
        valid_word = False
        allow_check = False
        #Check excluded letters list first
        for i in range(0, 5):
            if word[i] in excluded[i] and word in new_list:
                new_list.remove(word)
                break
            if word[i] in possibilities[i]:
                valid_word = True
            if len(possibilities[i]) != 0:
                allow_check = True
        if allow_check and not valid_word and word in new_list:
            new_list.remove(word)
            
    return new_list

def interpet_results(word_list, letter, attribute, position, answer):
    correct_guess = True

    possibilities, excluded = process_word(letter, attribute, position, answer)
    word_list = remove_words(possibilities, excluded, word_list)
    for i in answer:
        if i == "":
            correct_guess = False

    return word_list, correct_guess
    

def main():

    answer = [""] * 5

    word_list = get_data()
    correct_guess = False
    counter = 5
    while not correct_guess:
        print(answer)
        if counter == 5 or val == "next":
            print("Suggested word : " + str(give_word(word_list)))
            counter = 0
        val = input("Results ? O:inc 1:partial 2:correct | next for suggestion\n")
        if val != "next":
            word_list, correct_guess = interpet_results(word_list, val[0], int(val[2]), int(val[4]), answer)
            counter += 1    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nSIGINT received.')
        sys.exit(0)
