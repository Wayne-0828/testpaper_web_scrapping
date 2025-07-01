from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pathlib
from pathlib import Path
from time import sleep
import json
import os
import subprocess
import wget

my_options = webdriver.ChromeOptions()
my_options.add_argument("--start-maximized")         #最大化視窗
# my_options.add_argument("--incognito")               #開啟無痕模式
my_options.add_argument("--disable-popup-blocking") #禁用彈出攔截
my_options.add_argument("--disable-notifications")  #取消 chrome 推播通知
my_options.add_argument("--lang=zh-TW")  #設定為正體中文

base_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
download_dir = base_dir / "松山高中97後"
download_dir.mkdir(exist_ok=True)
prefs = {
    # 關鍵設定
    "download.default_directory": str(download_dir),   # 預設下載資料夾
    "download.prompt_for_download": False,            # 不跳另存視窗
    "download.directory_upgrade": True,               # 若資料夾已存在仍使用
    "profile.default_content_setting_values.automatic_downloads": 1,
    "safebrowsing.enabled": True,                     # 關閉「檔案可能危險」攔阻
    # 兼容某些 Chrome 版號：UI 顯示與實際下載路徑不同步的情況
    "savefile.default_directory": str(download_dir)   # CHROME 113+ 時偶爾需要:contentReference[oaicite:0]{index=0}
}
my_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=my_options
)
wait = WebDriverWait(driver, 10)

def visit(url):
    driver.get(url)

def close():
    driver.quit()

def get_a(css):
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css))
    )
    return [a.get_attribute("href")
            for a in driver.find_elements(By.CSS_SELECTOR, css)]

visit("https://www.sssh.tp.edu.tw/home?cid=899")
links = get_a("td.table-cells-border-zero a")
links2 = links[2:]

for url in links2:
    visit(url)
    for a in driver.find_elements(By.CSS_SELECTOR, "td a"):
        a.click()
        sleep(2)

close()