from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import calendar
import json

class Schedule:
  days_of_the_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday']
  
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--window-size=1920x1080')
  chrome_path = 'chromedriver.exe'

  def __init__(self, team, month_name, year):
    self.team = team
    self.month_name = month_name
    self.month_num = self.getMonthNum()
    self.year = year
    self.url = f'https://www.mlb.com/{self.team}/schedule/{self.year}-{self.month_num}'
    self.month_data = {
      'month': self.month_name,
      'year': self.year,
      'weeks': {
        'week1': {},
        'week2': {},
        'week3': {},
        'week4': {},
        'week5': {},
        'week6': {}
      }
    }
    self.driver = Chrome(executable_path=self.chrome_path, chrome_options=self.chrome_options)
    self.getSchedule()

  def getMonthNum(self):
    month_idx = list(calendar.month_name).index(self.month_name)
    if month_idx < 10:
      month_num = '0' + str(month_idx)
    else:
      month_num = str(month_num)
    return month_num

  def getGameData(self, el):
      data = {
        'game_exists': False,
        'opponent': el.find_elements_by_class_name('opponent-name')[0].get_property('innerText').strip(),
        'start_time': el.find_elements_by_class_name('primary-time')[0].get_property('innerText').strip(),
        'opponent_tricode': el.find_elements_by_class_name('opponent-tricode')[0].get_property('innerText').strip()
      }
      data['game_exists'] = True if data['opponent'] else False
      return data

  def getSchedule(self):
    self.driver.get(self.url)

    schedule_table = WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_xpath('//*[@id="club-schedule_index"]/main/div[2]/div/div/div[1]/div/div[1]/div[4]/table[2]'))

    weeks = schedule_table.find_elements_by_class_name('date-row')

    for (i, week) in enumerate(weeks):
      days  = week.find_elements_by_class_name('date-cell')
      week_title = f'week{i + 1}'
      for (d, day) in enumerate(days):
        day_of_the_week = self.days_of_the_week[d]

        day_of_month = day.find_elements_by_class_name('day-of-month-label')[0].get_property('innerText')
        
        game_details = day.find_elements_by_class_name('date-details')[0]

        game1_el = game_details.find_element_by_id('game1')
        game1_data = self.getGameData(game1_el)

        game2_el = game_details.find_element_by_id('game2')
        game2_data = self.getGameData(game2_el)

        self.month_data['weeks'][week_title][day_of_the_week] = {
          'day_of_the_month': day_of_month,
          'data': {
            'Game1': game1_data,
            'Game2': game2_data
          }
        }

    self.driver.quit()

if __name__ == "__main__":
  team = 'marlins'
  month = 'March'
  year = '2020'
  with open('teams_data.json', 'r') as f:
    teams_data = json.loads(f.read())
  with open('schedule_data.json', 'r') as f:
    schedule_data = json.loads(f.read())
  team_data = [t for t in teams_data if t['teamName'].lower() == team][0]
  team_abbr = team_data['abbreviation']
  if not schedule_data.get(team_abbr):
    schedule = Schedule(team, month, year)
    schedule_data[team_abbr] = {
      'data': team_data,
      'schedule': {
        year: {
          month: schedule.month_data
        }
      }
    }
  elif not schedule_data[team_abbr]['schedule'].get(year):
    schedule = Schedule(team, month, year)
    schedule_data[team_abbr]['schedule'][year] = { month: schedule.month_data }
  elif not schedule_data[team_abbr]['schedule'][year].get(month):
    schedule = Schedule(team, month, year)
    schedule_data[team_abbr]['schedule'][year][month] = schedule.month_data

  with open('schedule_data.json', 'w') as f:
    f.write(json.dumps(schedule_data))


# team_abbr: {
#   data: teams_data,
#   schedule: {
#     year: {
#       month:{
#         week1: {},
#         ...
#         week6: {}
#       }
#     }
#   }
# }