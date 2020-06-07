import math
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

print('\nBLM "Watch" Script Starting...\n')

# Converts Seconds to Time
def secToTime(sec):
    hr = sec / 60 / 60
    min = (hr % 1) * 60
    sec = (min % 1) * 60
    
    if hr == 0:
        hr = '00'
    else:
        hr = str(math.floor(hr))
    
    if min == 0:
        min = '00'
    elif min < 10:
        min = '0' + str(math.floor(min))
    else:
        min = str(math.floor(min))

    if sec == 0:
        sec = '00'
    elif sec < 10:
        sec = '0' + str(round(sec))
    else:
        sec = str(round(sec))

    return hr + ':' + min + ':' + sec

# Plays the whole video with ads over and over (restarts after end)
while True:
    broken = False
    browser = webdriver.Chrome("Desktop/Programming/Scripts/BLM/BLM/chromedriver")
    browser.get("https://www.youtube.com/watch?v=bCgLa25fDHM")
    actions = ActionChains(browser)
    time.sleep(5)
    seconds = 5

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

    # Play Full Video and then Quit
    if broken == False:
        time.sleep(5)

        # Loop to test if the "Replay" button exists yet (it only does when the video is over)
        while True:

            # Get Title
            try:
                title = browser.find_element_by_xpath('//*[@id="movie_player"]/div[22]/div[2]/div[1]/button').get_attribute("title")
                if title == "Play (k)":
                    print('Pressed Play')
                    actions.send_keys(Keys.SPACE).perform()
            except:
                # Already Playing or Video Ended
                pass

            # Try to get 'Replay' element
            try:
                replayButton = browser.find_element_by_xpath('//*[@id="movie_player"]/div[25]/div[2]/div[1]/button').get_attribute("title")
                if replayButton == 'Replay':
                    print('\nVideo Played in Full')
                    print('It took {} to play the entire video with ads'.format(secToTime(seconds)))
                    print('Ad time totaled {}'.format(secToTime(seconds - 3386)))
                    print('Restarting...\n')
                    browser.quit()
                    break
            except:
                pass

            time.sleep(1)
            seconds += 1