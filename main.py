import csv
import time
import random

import pyautogui
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

class My_scrapper:
    def __init__(self, path_csv_homes):
        """
        Contains the path of all the csv's
        the position of the needed text
        the browser/driver for fireofx
        :param path_csv_homes:
        """
        self.path_csv_homes=path_csv_homes

        # position of the adress
        self.xpos_top_adress = 1133
        self.ypos_top_adress = 270
        self.xpos_bot_adress = 1712
        self.ypos_bot_adress = 300
        # set up the firefox driver
        self.option = Options()
        self.option.add_argument('--no-sandbox')
        self.option.add_argument('--disable-dev-shm-usage')
        self.browser = Firefox(options=self.option)
        self.browser.maximize_window()


    def set_crops_from_csv(self):
        """
        TODO - use a proxy to not get blocked by the website        set all the crops from set_screenshot_crop for all the
        url in the csv file
        :return:
        """
        # with encoding because of the character when opening the csv
        with open(self.path_csv_homes, mode='r', encoding='utf-8-sig') as file:
            # reading the CSV file
            csvFile = csv.reader(file)

            # displaying the contents of the CSV file
            for lines in csvFile:
                # get the urls fro the csv
                scrap.browser.get(lines[0])
                scrap.set_screenshot_crop()
                #plt.imshow(scrap.crop)
                #plt.show()
                #time.sleep(random.uniform(0, 1))
    def set_screenshot_crop(self):
        """
        Gets coordinnates and "screenshot" accordingly
        return: the crop image
        """
        # screenshoot the full MAIN screen
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        #Crop the image to the needed size > the image is a 3 layers matrix (XGB)
        self.crop = image[self.ypos_top_adress:self.ypos_bot_adress,
                    self.xpos_top_adress:self.xpos_bot_adress,
                    :3]  # image[ymin:ymax,xmin:xmax,0:3]
if __name__ == '__main__':
    # path to the websraping urls
    db_path='./resources/scrapping_list.csv'
    scrap = My_scrapper(path_csv_homes=db_path)

    #scrap.set_crops_from_csv()
    # Take a single screenshot from the given url and print it
    scrap.browser.get("https://www.zillow.com/homedetails/1278-Pacific-Beach-Dr-UNIT-4-San-Diego-CA-92109/16920867_zpid/")
    scrap.set_screenshot_crop()
    plt.imshow(scrap.crop)
    plt.show()

    # get the text from the image
    txt = pytesseract.image_to_string(scrap.crop)
    print(type(txt))
    print(txt)

    # close all the opened browsers
    scrap.browser.close()