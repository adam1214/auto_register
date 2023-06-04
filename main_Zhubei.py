from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
import time
from selenium.webdriver import ActionChains
import asyncio
import pdb

async def write_id():
    driver.find_element(By.NAME, "Tel").send_keys(person_id)

async def write_name():
    driver.find_element(By.NAME, "sName").send_keys(person_name)
    
async def select_sex():
    driver.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[2]/td[2]/input[2]").click()
    
async def write_birth_year():
    driver.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[3]/td[2]/input[2]").send_keys(person_birth_year)
    
async def write_birth_month():
    driver.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[3]/td[2]/input[3]").send_keys(person_birth_month)
    
async def write_birth_day():
    driver.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[3]/td[2]/input[4]").send_keys(person_birth_day)
    
async def write_phone_num():
    driver.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[5]/td[2]/input").send_keys(person_phone_num)
    
async def write_address():
    driver.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[8]/td[2]/input").send_keys(person_address)

async def select_date():
    for i in range(0, 2, 1):
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[starts-with(@value, '1120302#3')]")))
        element.click()

async def main():
    # create task list
    tasks = []
    tasks.append(asyncio.create_task(write_id()))
    tasks.append(asyncio.create_task(write_name()))
    tasks.append(asyncio.create_task(select_sex()))
    tasks.append(asyncio.create_task(write_birth_year()))
    tasks.append(asyncio.create_task(write_birth_month()))
    tasks.append(asyncio.create_task(write_birth_day()))
    tasks.append(asyncio.create_task(write_phone_num()))
    tasks.append(asyncio.create_task(write_address()))
    tasks.append(asyncio.create_task(select_date()))
    # 執行所有 Tasks
    results = await asyncio.gather(*tasks)

if __name__ == '__main__':
    start_time = time.time()
    
    url = 'https://www.cmu-hch.cmu.edu.tw/OnlineAppointment/DoctorInfo?flag=first&DocNo=28629&Docname=%E9%99%B3%E4%BA%AD%E9%9C%93%28%E5%A5%B3%29'
    # person info
    person_id = 'A123456789'
    person_name = "XXX"
    person_birth_year = 'XX'
    person_birth_month = 'XX'
    person_birth_day = 'XX'
    person_phone_num = '0921XXXXXX'
    person_address = 'XXXXXXXXXXXXXXX'
    
    driver = webdriver.Chrome()
    driver.maximize_window() 
    driver.get(url)
    wait = ui.WebDriverWait(driver, 1000)
    wait.until(lambda driver: driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div/div/div/div[1]/div[3]/div[1]/div[5]/iframe"))
    iframe = driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div/div/div/div[1]/div[3]/div[1]/div[5]/iframe")
    driver.switch_to.frame(iframe)
    
    driver.find_element(By.NAME, "Tel").send_keys(person_id)
    
    driver.find_element(By.NAME, "sName").send_keys(person_name)

    driver.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[2]/td[2]/input[2]").click()
    
    driver.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[3]/td[2]/input[2]").send_keys(person_birth_year)
    driver.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[3]/td[2]/input[3]").send_keys(person_birth_month)
    driver.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[3]/td[2]/input[4]").send_keys(person_birth_day)
    
    driver.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[5]/td[2]/input").send_keys(person_phone_num)
    
    driver.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[8]/td[2]/input").send_keys(person_address)
    
    #asyncio.run(main()) # 執行協同程序
    
    for i in range(0, 2, 1):
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[starts-with(@value, '1120304#1')]")))
        element.click()
    
    end_time = time.time()
    print(round(end_time - start_time, 2), 'sec')

    #driver.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[9]/td/input[1]").click()