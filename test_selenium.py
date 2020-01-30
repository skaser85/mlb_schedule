from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
import pandas as ps

driver = Chrome('chromedriver.exe')

driver.get('https://www.mlb.com/reds/schedule/2020-03')

schedule_table = WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath('//*[@id="club-schedule_index"]/main/div[2]/div/div/div[1]/div/div[1]/div[4]/table[2]'))
# schedule_table = WebDriverWait(driver, 30).until(lambda driver: driver.find_elements_by_tag_name('table'))

weeks = schedule_table.find_elements_by_class_name('date-row')

week1 = weeks[0]

week1_days = week1.find_elements_by_class_name('date-cell')

week1_sunday = week1_days[0]

week1_sunday_dom = week1_sunday.find_elements_by_class_name('day-of-month-label')[0]

week1_sunday_dom = 0 if week1_sunday_dom.text == '' else week1_sunday_dom.text

week1_sunday_details = week1_sunday.find_elements_by_class_name('date-details')[0]
opponent_name = week1_sunday_details.find_elements_by_class_name('opponent-name')[0].get_property('innerText')
opponent_tricode = week1_sunday_details.find_elements_by_class_name('opponent-tricode')[0].text

#game1 > div.matchup-area > div.matchup > div.opponent-name

print(week1_sunday_dom)
print(opponent_tricode)
print(opponent_name)

#https://www.mlbstatic.com/team-logos/team-cap-on-light/113.svg

driver.quit()