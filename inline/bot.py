import os
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

from inline.logger import error_logger, logger
from inline.schema import OrderInfo, Gender, Meal

class inline:
    def __init__(self, use_remote: bool = False):
        self._url = "https://inline.app/booking/-M7q3CM0PAKAdJnHqyPe:inline-live-1/-M7q3CQ84DLcq93tijAx?language=zh-tw"
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

    def _elem_scoll(self, locator, wait_sec=1):
        elem = WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located(locator))
        self._chrome.execute_script("arguments[0].scrollIntoView(false);", elem)
        self.wait_loading(wait_sec=wait_sec)
        # elem.click()
        return elem
    
    # 人數 日期 時間 姓名 性別 電話 套餐 備注
    def query_case_status(self, order_info: OrderInfo): # remove default value
        try:
            # 進入訂餐網站
            self._chrome.get(self._url)
            self.wait_loading()
            
            # 選擇人數
            adult_picker = self._elem_scoll((By.ID, "adult-picker"))
            Select(adult_picker).select_by_visible_text(f"{order_info.adult_num}位大人")
            
            # 選擇日期
            date_picker = self._elem_scoll((By.ID, "date-picker"))
            date_picker.click()
            
            # 調整要點擊的月份出現在最左邊 避免沒有顯示該月份導致無法點擊
            month_elem = self._elem_scoll((By.XPATH, "//*[@id='calendar-picker']/div[1]/div[1]/h4")) 
            while True:
                month_elem = WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='calendar-picker']/div[1]/div[1]/h4")))
                logger.info(f"month_elem.text: {month_elem.text}")
                format = "%Y年%m月"
                date = datetime.strptime(month_elem.text, format)
                if date.year == order_info.meal_datetime.year and \
                    date.month == order_info.meal_datetime.month:
                        break
                
                if date > order_info.meal_datetime:
                    # 往上一個月份
                    WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='calendar-picker']/div[1]/div[1]/a[1]"))).click()
                else:
                    # 往下一個月份
                    WebDriverWait(self._chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='calendar-picker']/div[2]/div[1]/a[2]"))).click()
            
            # 3/13 =>  //*[@id="calendar-picker"]/div[2]/div[3]/div[3]/div[2]/div[2]/span
            date_elem = self._elem_scoll((By.XPATH, "//div[@id='calendar-picker']/div/div[3]/div[4]/div[4]/div[2]/span"))
            date_elem.click()
            
            logger.info(f"date_elem.text: {date_elem.text}")
            
            # # 選擇時間 17:30
            # time_elem = self._elem_scoll((By.XPATH, "//div[@id='book-now-content']/div[4]/button[1]"))
            # time_elem.click()
            
            # 選擇時間 19:30
            time_elem = self._elem_scoll((By.XPATH, "//div[@id='book-now-content']/div[4]/button[2]"))
            time_elem.click()
            
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
        logger.info("1. query_case_status")
        self.query_case_status(order_info)
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
