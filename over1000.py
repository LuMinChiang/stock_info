from selenium import webdriver
import os

current_directory = os.getcwd()
url = "https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E4%B8%8A%E5%B8%82&INDUSTRY_CAT=%E4%B8%8A%E5%B8%82%E5%85%A8%E9%83%A8&SHEET=%E4%BA%A4%E6%98%93%E7%8B%80%E6%B3%81&SHEET2=%E6%97%A5&RPT_TIME=%E6%9C%80%E6%96%B0%E8%B3%87%E6%96%99"
print(url)
driver_directory = current_directory+"/chromedriver-mac-arm64/chromedriver"
print(driver_directory)

cService = webdriver.ChromeService(executable_path=driver_directory)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=cService, options=options)

driver.get(url)
driver.implicitly_wait(5)
content = driver.page_source
print(type(content))
#print(content)


with open(current_directory+"/website_content.html", "w") as f:
    f.write(content)


driver.quit()
