# https://blog.csdn.net/wangzhuanjia/article/details/124673223
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
import time
from selenium.webdriver import ActionChains
import asyncio
import pdb
from PIL import Image
import os
import tesserocr
import cv2
import numpy as np
import ddddocr

# 3處須改動
def main_fun():
    person_id = 'A123456789'
    person_phone_num = '09XXXXXXXX'
    Consultation_time = '上午' # 1: 上午, 下午, 夜間
    
    url = 'https://app.tzuchi.com.tw/tchw/opdreg/OpdTimeShow.aspx?Depart=%E9%97%9C%E7%AF%80%E4%B8%AD%E5%BF%83&HospLoc=1'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome()
    #driver.maximize_window() 
    driver.get(url)
    wait = ui.WebDriverWait(driver, 1000)
    
    # 2: index of tr: row數, 從1開始數, 開始列包含"看診日、上午、下午、夜間"
    hyper_root = '/html/body/form/table[2]/tbody/tr/td/center/table/tbody/tr[2]/td[2]/center/table/tbody/tr[7]' 
    
    if Consultation_time == '上午':
        hyper_root += '/td[2]/'
    elif Consultation_time == '下午':
        hyper_root += '/td[3]/'
    else:
        hyper_root += '/td[4]/'

    hyper_root += 'a[1]' # 3: 若有兩位醫師在同一時段, 由上而下依序為a[1], a[2]; 若只有一位醫師則為a
    
    wait.until(lambda driver: driver.find_element(By.XPATH, hyper_root))
    driver.find_element(By.XPATH, hyper_root).click()
    
    wait.until(lambda driver: driver.find_element(By.ID, 'rblRegFM_0')).click()
    driver.find_element(By.ID, 'rblRegFM_0').click()
    driver.find_element(By.NAME, "txtMRNo").send_keys(person_id)
    driver.find_element(By.NAME, "txtTel").send_keys(person_phone_num)

    while(1):
        try:
            confirm_btn = driver.find_element(By.NAME, "btnRegNo")
        except:
            break
        
        driver.save_screenshot('data/full_img.png')
        img = driver.find_element(By.ID, 'imgVI')
        #print(img.location)
        #print(img.size)
        img_height = img.size['height']
        img_width = img.size['width']
        
        left = img.location['x']
        top = img.location['y']
         
        right = img.location['x'] + img.size['width']
        bottom = img.location['y'] + img.size['height']
        
        img = Image.open('data/full_img.png')
        
        screensize = (driver.execute_script("return document.body.clientWidth"), #Get size of the part of the screen visible in the screenshot
                  driver.execute_script("return window.innerHeight"))
        img = img.resize(screensize) #resize so coordinates in png correspond to coordinates on webpage

        img = img.crop((left, top, right, bottom))
        
        img.save('data/crop_img.png')
        
        ocr = ddddocr.DdddOcr(use_gpu=True, device_id=0)
        img = cv2.imread('data/crop_img.png', cv2.IMREAD_GRAYSCALE)
        thres = 180
        img = cv2.threshold(img, thres, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite('data/crop_img_thres.png', img)
        with open('data/crop_img_thres.png', 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)
        driver.find_element(By.NAME, "txtVCode").send_keys(res.replace('I', '1').replace('o', '0').replace('B', '8'))
        confirm_btn.click()

if __name__ == '__main__':
    while(1):
        localtime = time.asctime(time.localtime (time.time()))
        if localtime == 'Mon Apr 17 07:59:58 2023':
            main_fun()
            break