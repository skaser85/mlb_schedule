import urllib.request
import os
import json

with open('teams_data.json', 'r') as f:
  teams = json.load(f)

for team in teams:
  team_id = team['id']
  team_abbr = team['abbreviation']
  url_light = f'https://www.mlbstatic.com/team-logos/team-cap-on-light/{team_id}.svg'
  file_name_light = f'{team_abbr}_on_light.svg'
  url_dark = f'https://www.mlbstatic.com/team-logos/team-cap-on-dark/{team_id}.svg'
  file_name_dark = f'{team_abbr}_on_dark.svg'
  urllib.request.urlretrieve(url_light, file_name_light)
  urllib.request.urlretrieve(url_dark, file_name_dark)
