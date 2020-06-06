import math
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

print('\nBLM "Watch" Script Starting...\n')

# Find XPath For 'Skip Ad' Element
def skipAdXPath(browser):

    first = '//*[@id="player-overlay:'
    second = '"]/div[2]'

    for num in range(10, 50):
        num = str(num)
        try:
            browser.find_element_by_xpath(first + num + second)
            return True
        except:
            pass

    # Letters (j)
    for letter in alphabet:        
        try:
            browser.find_element_by_xpath(first + letter + second)
            return True
        except:
            pass

    # Combination (1j)
    for letter in alphabet:
        for num in range(10):
            middle = str(num) + letter
            try:
                browser.find_element_by_xpath(first + middle + second)
                return True
            except:
                pass

    return False

# Find XPath of Duration Element
def durationXPath(browser):

    first = '//*[@id="ad-text:'
    second = '"]'
    # Numbers
    for num in range(100):
        num = str(num)
        try:
            dur = browser.find_element_by_xpath(first + num + second).text
            if ':' in dur:
                return dur, 0
        except:
            pass

    # Letters
    for letter in alphabet:
        try:
            dur = browser.find_element_by_xpath(first + letter + second).text
            if ':' in dur:
                return dur, 0
        except:
            pass

    # Combination (1j)
    for letter in alphabet:
        for num in range(50):
            middle = str(num) + letter
            try:
                dur = browser.find_element_by_xpath(first + middle + second).text
                if ':' in dur:
                    return dur, 10
            except:
                pass
    
    # Combination (j1)
    for letter in alphabet:
        for num in range(50):
            middle = letter + str(num)
            try:
                dur = browser.find_element_by_xpath(first + middle + second).text
                if ':' in dur:
                    return dur, 15
            except:
                pass

    # Combination (1j)
    for l1 in alphabet:
        for l2 in alphabet:
            middle = l1 + l2
            try:
                dur = browser.find_element_by_xpath(first + middle + second).text
                if ':' in dur:
                    return dur, 20
            except:
                pass

    print('ERROR: AD PRESENT BUT NO DURATION ELEMENT ABLE TO BE DETECTED')
    return 0

# Test is there's an ad. If there is, add 1 to the "Ad Counter" and wait until the ad ends then continue on
def numAds(browser, ads):
    
    adNum = 1
    ad = skipAdXPath(browser)

    # If an ad played, add 1 to the counter and wait until the ad finishes
    if ad == True:
        t, d = durationXPath(browser)
        if t != 0:
            duration = timeToSeconds(t) + d
            min = math.floor(duration / 60)
            sec = duration - (min * 60)

            if sec < 10:
                sec = '0' + str(sec)

            print('Ad detected...Duration:', str(min) + ":" + str(sec))
            adTimes.append(duration)
            time.sleep(duration)
        return 1
    return 0

def timeToSeconds(t):
    for i, el in enumerate(t):
        if el == ":":
            index = i
            break

    # t = '3:46'
    min = int(t[0 : index])
    sec = int(t[index + 1:])
    
    totalSec = (60 * min) + sec
    return totalSec + 10
    
def sum(lst):
    s = 0
    for e in lst:
        s += e
    return s

ads = 0
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
adTimes = []

# Plays the whole video with ads over and over (restarts after end)
while True:
    broken = False
    browser = webdriver.Chrome("Desktop/Programming/Scripts/BLM/BLM/chromedriver")
    browser.get("https://www.youtube.com/watch?v=bCgLa25fDHM")
    actions = ActionChains(browser)
    time.sleep(5)

    # Get Title
    try:
        title = browser.find_element_by_xpath('//*[@id="movie_player"]/div[22]/div[2]/div[1]/button').get_attribute("title")
        playing = False
    except:
        playing = True

    # Press Space Again?
    if playing == False:
        if title == "Play (k)":
            print('Pressed Play')
            actions.send_keys(Keys.SPACE).perform()
        elif title == "Pause (k)":
            pass
        else:
            broken = True
            browser.quit()

    # Mute Audio
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--mute-audio")

    # Play Full Video and then Quit
    if broken == False:
        seconds = 0
        time.sleep(5)

        # Loop to test if the "Replay" button exists yet (it only does when the video is over)
        while True:

            # Test is there's an ad. If there is, add 1 to the "Ad Counter" and wait until the ad ends then continue on
            ads += numAds(browser, ads)

            # Try to get 'Replay' element
            try:
                replayButton = browser.find_element_by_xpath('//*[@id="movie_player"]/div[25]/div[2]/div[1]/button').get_attribute("title")
                s = sum(adTimes)

                totalAdTime = round(s / 60, 2)
                if replayButton == 'Replay':
                    print('\nVideo Played in Full')
                    print('There were {} ads, totaling {} minutes'.format(ads, totalAdTime))
                    print('Restarting...\n')
                    browser.quit()
                    break
            except:
                pass

            seconds += 1

