import math
import time
from datetime import datetime as dt
from datetime import time as tim
from datetime import timedelta as td
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

print('\nBLM "Watch" Script Starting...\n')

def findReplayXPath():
    first = '//*[@id="movie_player"]/div['
    second = ']/div[2]/div[1]/button'
    for num in range(24, 26):
        try:
            replayButton = browser.find_element_by_xpath(first + str(num) + second).get_attribute("title")
            return replayButton
        except:
            pass
    return ''

def adTime(totalRunTime):
    videoLen = td(seconds = 3386)
    secDiff = totalRunTime.seconds - videoLen.seconds
    
    if secDiff > 0:
        return str(td(seconds = secDiff))
    else:
        return '(no ads were detected or the video was cut short)'

def end():
    print('\nVideo Played in Full')

    currentTime = dt.now().replace(microsecond = 0)
    totalRunTime = (currentTime - initialTime)

    print('It took {} to play the entire video with ads'.format(totalRunTime))
    print('Ad time totaled: {}'.format(adTime(totalRunTime)))
    print('Restarting...\n')
    browser.quit()

# Plays the whole video with ads over and over (restarts after end)
while True:
    go = True
    broken = False
    browser = webdriver.Chrome("Desktop/Programming/Scripts/BLM/BLM/chromedriver")
    browser.get("https://www.youtube.com/watch?v=bCgLa25fDHM")
    actions = ActionChains(browser)
    time.sleep(5)

    # Get Title
    try:
        title = browser.find_element_by_xpath('//*[@id="movie_player"]/div[22]/div[2]/div[1]/button').get_attribute("title")
    except:
        try:
            title = browser.find_element_by_xpath('//*[@id="movie_player"]/div[23]/div[2]/div[1]/button').get_attribute("title")        
        except:
            try:
                title = browser.find_element_by_xpath('//*[@id="movie_player"]/div[24]/div[2]/div[1]/button').get_attribute("title")        
            except:
                pass

    # Press Space Again?
    if 'title' in globals() or 'title' in locals():
        if title == "Play (k)":
            print('Pressed Play')
            actions.send_keys(Keys.SPACE).perform()
        elif title == "Pause (k)":
            pass
        else:
            broken = True
            browser.quit()

    # Play Full Video and then Quit
    if broken == False:

        initialTime = dt.now().replace(microsecond = 0)

        time.sleep(5)

        # Loop to test if the "Replay" button exists yet (it only does when the video is over)
        while go:

            if browser.current_url != 'https://www.youtube.com/watch?v=bCgLa25fDHM':
                print(browser.current_url)
                print('Went to the wrong video')
                end()

            # Get Title
            try:
                title = browser.find_element_by_xpath('//*[@id="movie_player"]/div[25]/div[2]/div[1]/button').get_attribute("title")
                if title == "Play (k)":
                    print('Pressed Play')
                    actions.send_keys(Keys.SPACE).perform()
            except:
                # Already Playing or Video Ended
                pass

            # Try to get 'Replay' element
            try:
                replayButton = findReplayXPath()
                if replayButton == 'Replay':   
                    end()
                    go = False
            except:
                pass

            time.sleep(0.5)