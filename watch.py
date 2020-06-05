import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

print('BLM "Watch" Script Starting...')

while True:
    broken = False
    browser = webdriver.Chrome("chromedriver")
    browser.get("https://www.youtube.com/watch?v=bCgLa25fDHM")
    actions = ActionChains(browser)
    time.sleep(5)

    # Get Title
    try:
        title = browser.find_element_by_xpath('//*[@id="movie_player"]/div[22]/div[2]/div[1]/button').get_attribute("title")
        playing = False
    except:
        print('Already Playing (failed to get title attribute)')
        playing = True

    # Press Space Again?
    if playing == False:
        if title == "Play (k)":
            print('Pressed Play')
            actions.send_keys(Keys.SPACE).perform()
        elif title == "Pause (k)":
            print('Already Playing (successfuly retrieved title attribute)')
        else:
            broken = True
            browser.quit()

    # Play Full Video and then Quit
    if broken == False:
        time.sleep(5)
        # Testing if the "Replay" button exists yet (it only does when the video is over)
        while True:
            try:
                replayButton = browser.find_element_by_xpath('//*[@id="movie_player"]/div[25]/div[2]/div[1]/button').get_attribute("title")
                if replayButton == 'Replay':
                    print('Video Played in Full, Restarting...')
                    browser.quit()
                    break
            except:
                pass
            time.sleep(1)