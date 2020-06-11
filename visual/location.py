from selenium import webdriver
from time import sleep
import os


os.chdir(r"C:\Users\Kembabazi Barbara\Desktop\Cesium")
os.system('cmd /k "node server.cjs"')
browser = webdriver.Chrome('C:/webdrivers/chromedriver.exe')
browser.get('http://localhost:8080/Apps/Hello.html')
sleep(1)

browser.get_screenshot_as_file("screenshot.png")
browser.quit()
print("end...")