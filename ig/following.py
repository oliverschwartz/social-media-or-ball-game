from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

driver.switch_to.window("https://www.instagram.com/accounts/login/")
driver.find_element_by_name("username").send_keys('ele381proj')
driver.find_element_by_name("password").send_keys('mattandollie')

driver.get('https://www.instagram.com/kingjames')
wait(5)
following_link = driver.find_element_by_link_text('248 following')
ActionChains(driver).move_to_element(following_link).click(following_link).perform()