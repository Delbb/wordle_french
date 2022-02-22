#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

import time

answer = [""] * 5

key_index = {
    "a" : 0,
    "z" : 1,
    "e" : 2,
    "r" : 3,
    "t" : 4,
    "y" : 5,
    "u" : 6,
    "i" : 7,
    "o" : 8,
    "p" : 9,
    "q" : 10,
    "s" : 11,
    "d" : 12,
    "f" : 13,
    "g" : 14,
    "h" : 15,
    "j" : 16,
    "k" : 17,
    "l" : 18,
    "m" : 19,
    "enter" : 20,
    "w" : 21,
    "x" : 22,
    "c" : 23,
    "v" : 24,
    "b" : 25,
    "n" : 26,
    "delete" : 27
}

def init_navigator():
    # Créer une session Chrome
    ser = Service('/home/robotics/sandbox/python/word/chromedriver_linux64/chromedriver')
    driver = webdriver.Chrome(service=ser)
    driver.implicitly_wait(3000)
    
    driver.set_window_size(width=979, height=1053)
    #mx size is w:1848 h:1053
    # Appeler l’application web
    driver.get("https://wordle.louan.me/")
    time.sleep(1)
    return driver

def get_data():
    #Get input data as list of strings
    with open('data_french.txt') as f:
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

def process_word(letter, number, position):
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

def write_keyboard(driver, word):

    search = driver.find_elements(By.ID, "key")
    for letter in word:
        search[key_index[letter]].click()
    
    search[key_index["enter"]].click()

def interpet_results(driver, word_list, word):
    correct_guess = True
    status = {
        "incorrect" : 0,
        "partial" : 1,
        "correct" : 2
    }
    search = driver.find_elements(By.ID, "key")
    # read the five letters
    for index, letter in enumerate(word):
        attribute = search[key_index[letter]].get_attribute('class')

        possibilities, excluded = process_word(letter, status[attribute], index)
        word_list = remove_words(possibilities, excluded, word_list)

    for i in answer:
        if i == "":
            correct_guess = False

    return word_list, correct_guess
    

def main():

    driver = init_navigator()

    stop = False
    archives = True

    while not stop:
        correct_guess = False
        fail = False
        attempt = 0
        lines = get_data()
        #Play the game
        while not correct_guess and not fail:
            correct_guess = True
            suggested_word = give_word(lines)
            print("Suggested word is : " + str(suggested_word))
            attempt += 1
            if len(lines) > 1:
                write_keyboard(driver,suggested_word)
                lines, correct_guess = interpet_results(driver, lines, suggested_word)

            else:
                print("Answer is : " + str(suggested_word))
                write_keyboard(driver, suggested_word)

            if attempt == 6 and not correct_guess:
                print("LOSER")
                fail = True


            #reset variable
            if correct_guess or fail:
                if not fail:
                    print("CONGRATULATIONS")     

                for i in range(0, len(answer)):
                    answer[i] = ""  
        time.sleep(2)

        # Close ending window
        search = driver.find_element(By.CLASS_NAME, 'close-btn')
        print(search)
        search.click()

        print("Closed")
        time.sleep(0.1)
        # for element in search:
        #     attribute = element.get_attribute('alt')
        #     print(element)
        #     print(attribute)
        #     if attribute == "Fermer":
        #         print("Closing windows")
        #         element.click()
        #         time.sleep(1)
                
        # Start new game
        print("Select archives")
        search = driver.find_elements(By.TAG_NAME, 'img')
        for element in search:
            attribute = element.get_attribute('alt')
            if archives and attribute == 'Archives':
                element.click()
                archives = False
                break
            else:
                if attribute == 'Date précédente':
                    element.click()
                    break
        

        
        
    driver.quit()


if __name__ == "__main__":
    main()
