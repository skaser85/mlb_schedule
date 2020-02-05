from flask import Flask, render_template, url_for, request, redirect
from flask_cors import CORS
import json
import calendar
from Schedule import Schedule

with open('teams_data.json', 'r') as f:
  teams_data = json.load(f)

teams_by_division = {}
for team in teams_data:
  division = team['division']['name']
  if not teams_by_division.get(division):
    teams_by_division[division] = []
  # add team_abbr here
  teams_by_division[division].append({ 'name': team['name'], 'abbr': team['abbreviation'] })

for division in sorted(teams_by_division.keys()):
  # this is now a dict, so we need to sorty by the team['name'] value
  teams_by_division[division] = sorted(teams_by_division[division], key=lambda d: d['name'])

app = Flask(__name__)
app.config['SECRET_KEY'] = '76d20590d2ac659cc82a23e2d7b653ce'
CORS(app)

@app.route('/', methods=['GET'])
def home():
  return render_template('index.html', teams_data=teams_data, teams_by_division=teams_by_division, months=calendar.month_name)

@app.route('/schedule', methods=['POST'])
def schedule():
  data = request.get_data().decode()
  data_dict = json.loads(data)
  year = '2020'
  month = data_dict['month']
  
  for team in teams_data:
    if team['abbreviation'] == data_dict['team']:
      the_team = team
      break
  
  team = the_team['teamName'].lower().replace(' ', '')
  team_abbr = the_team['abbreviation']

  with open('schedule_data.json', 'r') as f:
    schedule_data = json.loads(f.read())

  if not schedule_data.get(team_abbr):
    schedule = Schedule(team, month, year)
    schedule_data[team_abbr] = {
      'data': the_team,
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

  return json.dumps(schedule_data[team_abbr]['schedule'][year][month])


if __name__ == '__main__':
  app.run(debug=True)