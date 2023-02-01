# -*- coding: utf-8 -*-
import os
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
import requests
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from inline.logger import error_logger, logger
from inline.schema import OrderInfo, Gender, Meal

class inline:
    def __init__(self, use_remote: bool = False):
        self._url = "https://inline.app/booking/yinmi117/yinmi117"
        self._case_status = ""
        self._chrome = None
        
        if use_remote:
            self._chrome = webdriver.Remote(
                os.getenv("CHROME_REMOTE_URL"),
                desired_capabilities=DesiredCapabilities.CHROME)
        else:
            ## for screen display
            # _chrome_opt = Options()
            # _chrome_opt.add_argument("--disable-notifications")
            # _chrome_opt.add_argument('--headless')  # enable headless mode
            # _chrome_opt.add_argument('--disable-gpu') # disable GPU, avoid system error or web error
            # self._chrome = uc.Chrome(advanced_elements=True, chrome_options=_chrome_opt)
            self._chrome = uc.Chrome(advanced_elements=True)

    def wait_loading(self, wait_sec: float = 2.0):
        # Wait for the page to load
        time.sleep(wait_sec)
    
    def capture_screen(self, screen_path):
        if screen_path is not None:
            screen_path = Path(screen_path)

            if screen_path.is_dir():
                screen_path = screen_path / 'screen.png'
            
            screen_path = screen_path.with_suffix('.png')
            
            self._chrome.save_screenshot(f'{screen_path}')

    def _elem_scoll(self, locator, wait_sec=1, scroll=False):
        elem = WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located(locator))
        self._chrome.execute_script(f"arguments[0].scrollIntoView({'true' if scroll else 'false'});", elem)
        self.wait_loading(wait_sec=wait_sec)
        # elem.click()
        return elem
    
    # 進入訂餐網站
    def enter_reserve_website(self):    
        self._chrome.get(self._url)
        self.wait_loading()
    
    # 選擇人數
    def select_adult(self, adult_num):
        adult_picker = self._elem_scoll((By.ID, "adult-picker"))
        Select(adult_picker).select_by_visible_text(f"{adult_num}位大人")
    
    def select_datetime(self, order_datetime: datetime):
        # 選擇日期
            date_picker = self._elem_scoll((By.ID, "date-picker"), scroll=True)
            date_picker.click()
            
            # 調整要點擊的月份出現在最左邊 避免沒有顯示該月份導致無法點擊
            month_elem = self._elem_scoll((By.XPATH, "//*[@id='calendar-picker']/div[1]/div[1]/h4")) 
            while True:
                month_elem = WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='calendar-picker']/div[1]/div[1]/h4")))
                logger.info(f"month_elem.text: {month_elem.text}")
                format = "%Y年%m月"
                date = datetime.strptime(month_elem.text, format)
                if date.year == order_datetime.year and \
                    date.month == order_datetime.month:
                        break
                
                if date > order_datetime:
                    # 往上一個月份
                    WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='calendar-picker']/div[1]/div[1]/a[1]"))).click()
                else:
                    # 往下一個月份
                    WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='calendar-picker']/div[2]/div[1]/a[2]"))).click()
            
            # 找出要預訂的日期div位置
            date_l2_c1 = self._chrome.find_element(By.XPATH, '//*[@id="calendar-picker"]/div[1]/div[3]/div[2]/div[1]/div[2]/span')
            date_l2_c1 = int(date_l2_c1.text)
            order_day = order_datetime.day
            day_diff = order_day - date_l2_c1
            if day_diff < 0:
                day = order_day
                week = 1
            else:
                week = (day_diff//7)+2
                day = (day_diff%7)+1
            
            logger.info(f'week: {week}, day: {day}')
            
            try:
                date_elem = self._elem_scoll((By.XPATH, f'//*[@id="calendar-picker"]/div[1]/div[3]/div[{week}]/div[{day}]/div[2]/span'), scroll=True)
                date_elem.click()
            except Exception as e:
                logger.error(f"failed to click date element")
                raise Exception("failed to click date element")
            
            logger.info(f"date_elem.text: {date_elem.text}")
            
            try:
                date_all_booked = self._chrome.find_element(By.XPATH, '//*[@id="book-now-content"]/div/p')
                logger.info(f"date_all_booked message: {date_all_booked.text}")
            except Exception as e:
                logger.info("This date can be reserved")
            else:
                raise Exception("This date can not be reserved")
            
            if order_datetime.hour == 11 and order_datetime.minute == 30:
                time_xpath_val = '//*[@id="book-now-content"]/div[2]/button'
            elif order_datetime.hour == 17 and order_datetime.minute == 30:
                time_xpath_val = '//*[@id="book-now-content"]/div[4]/button[1]'
            else:
                time_xpath_val = "//div[@id='book-now-content']/div[4]/button[2]"
            
            # 查看是否有 提示 "登記候補" 的 span
            try:
                time_xpath_val_tip = f"{time_xpath_val}/span[3]"
                time_all_booked = self._chrome.find_element(By.XPATH, time_xpath_val_tip)
                logger.info(f"time_all_booked message: {time_all_booked.text}")
            except Exception as e:
                logger.info("This time can be reserved")
            else:
                raise Exception("This time can not be reserved")
            
            time_elem = self._elem_scoll((By.XPATH, time_xpath_val))
            time_elem.click()
        
    # 人數 日期 時間 姓名 性別 電話 套餐 備注
    def reserve_table(self, order_info: OrderInfo): # remove default value
        try:
            # 進入訂餐網站
            self.enter_reserve_website()
            # 選擇人數
            self.select_adult(adult_num=order_info.adult_num)
            # 選擇日期
            self.select_datetime(order_datetime=order_info.meal_datetime)
            # 下一步填寫資訊
            more_elem = self._elem_scoll((By.XPATH, "//div[@id='book-now-action-bar']/div[2]/button/span/span"))
            more_elem.click()
            logger.info("Next")
            
            # 輸入姓名
            name_elem = self._elem_scoll((By.ID, "name"))
            name_elem.click()
            name_elem.clear()
            name_elem.send_keys(f"{order_info.name}")
            
            # 選擇性別
            if order_info.gender == Gender.MALE:
                WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located((By.ID, "gender-male"))).click()
            else:
                WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located((By.ID, "gender-female"))).click()
            
            # 輸入電話
            phone_elem = WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located((By.ID, "phone")))
            phone_elem.click()
            phone_elem.clear()
            phone_elem.send_keys(f"{order_info.phone}")
            
            # 選擇套餐
            if Meal.MEAL1180 in order_info.meal:
                WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located((By.XPATH, u"//div[@value='套餐1180元\n']"))).click()
                # self._elem_scoll((By.XPATH, u"//div[@value='套餐1180元\n']")).click()
                
            if Meal.MEAL1580 in order_info.meal:
                WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='contact-form']/section/div[4]/div[1]/div[3]/span"))).click()
                # self._elem_scoll((By.XPATH, "//*[@id='contact-form']/section/div[4]/div[1]/div[3]/span")).click()
            
            # 加點龍蝦
            if Meal.Lobster in order_info.meal:
                WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//form[@id='contact-form']/section/div[4]/div/div[2]/span"))).click()
                # self._elem_scoll((By.XPATH, "//form[@id='contact-form']/section/div[4]/div/div[2]/span")).click()
            
            # 特殊需求
            # remark_elem = self._elem_scoll((By.XPATH, "//form[@id='contact-form']/section/div[5]/textarea"))
            remark_elem = WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//form[@id='contact-form']/section/div[5]/textarea")))
            remark_elem.click()
            remark_elem.clear()
            remark_elem.send_keys(f"{order_info.remark}")
            
            # 確認訂位
            self._elem_scoll((By.XPATH, "//form[@id='contact-form']/div/button/span")).click()
            
            # 不加入行事曆
            self._elem_scoll((By.NAME, "calendarModalRejectButton")).click()
        except Exception as e:
            err_msg = f"failed to query case status: {e}"
            error_logger.error(err_msg)
            return err_msg
    
    def run(self, order_info: OrderInfo, final_screen_path: str):
        self.reserve_table(order_info)
        self.capture_screen(final_screen_path)
        logger.info("Done !!")

    def notify_line(self, token: str):
        if not token: return
       
        # message you want to send
        tpe_date = datetime.now(tz=timezone(timedelta(hours=+8))).strftime("%Y/%m/%d")
        
        message = f'''
        inline {tpe_date}
        {self._case_status}
        '''

        # HTTP headers and message
        headers = {"Authorization": f"Bearer {token}"}
        data = { 'message': message }

        # Image want to sens
        # image = open('my_image.jpg', 'rb')
        # files = { 'imageFile': image }

        # send line notify by Line API
        requests.post(
            "https://notify-api.line.me/api/notify",
            headers = headers,
            data = data,
            # files = files
        )
        

    def teardown(self):
        if self._chrome is not None:
            self._chrome.quit()
