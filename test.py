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
  teams_by_division[division].append(team['name'])

for division in sorted(teams_by_division.keys()):
  teams_by_division[division].sort()

app = Flask(__name__)
app.config['SECRET_KEY'] = '76d20590d2ac659cc82a23e2d7b653ce'
CORS(app)

@app.route('/', methods=['GET'])
def home():
  return render_template('index.html', teams_data=teams_data, teams_by_division=teams_by_division, months=calendar.month_name)

@app.route('/schedule', methods=['POST'])
def schedule():
  with open('test_data.json') as f:
    return f.read()
  # data = request.get_data().decode()
  # data_dict = json.loads(data)
  # for team in teams_data:
  #   if team['name'] == data_dict['team']:
  #     the_team = team
  #     break
  # team = the_team['teamName'].lower().replace(' ', '')
  # schedule = Schedule(team, data_dict['month'],'2020')
  # with open('test_data.json', 'w') as f:
  #   f.write(json.dumps(schedule.month_data))
  # return json.dumps(schedule.month_data)


if __name__ == '__main__':
  app.run(debug=True)