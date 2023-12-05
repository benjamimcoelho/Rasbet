from apostas.models import ApostaFormula1,PartidaFutebol

import requests
import json
import os




# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = '050b69e8a2a644cd74a2f95f5efffd3d'

SPORT = 'soccer_portugal_primeira_liga' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'eu' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h,spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal' # decimal | american

DATE_FORMAT = 'iso' # iso | unix

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getJogos():

    if not os.path.exists("data.json"):

        odds_response = requests.get(
            f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
            params={
                'api_key': API_KEY,
                'regions': REGIONS,
                'markets': MARKETS,
                'oddsFormat': ODDS_FORMAT,
                'dateFormat': DATE_FORMAT,
            }
        )

        if odds_response.status_code != 200:
            print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

        else:
            odds_json = odds_response.json()
            with open('data.json', 'w') as f:
                json.dump(odds_json, f)

            print('Number of events:', len(odds_json))
            for event in odds_json:
                print(event)

            # Check the usage quota
            print('Remaining requests', odds_response.headers['x-requests-remaining'])
            print('Used requests', odds_response.headers['x-requests-used'])
    else:
        with open('data.json') as f:
            data = json.load(f)

            for d in data:
                try:
                    addJogo(d)
                except:
                    pass

def addJogo(json):
    check = False
    odds_casa = 1
    odds_visitante = 1
    odds_empate = 1
    for x in json["bookmakers"]:
        for y in x["markets"]:
            for k in y["outcomes"]:
                if k["name"] == "Draw":
                    check = True
                    odds_empate = k["price"]
                else:
                    if k["name"] == json["home_team"]:
                        odds_casa = k["price"]
                    if k["name"] == json["away_team"]:
                        odds_visitante = k["price"]
            if check == True:
                break
        
        if check == True:
            break
    
    j = PartidaFutebol(titulo="Portugal",
                        commence_time=json["commence_time"],
                        equipa_casa=json["home_team"],
                        equipa_visitante=json["away_team"],
                        odds_casa=odds_casa,
                        odds_visitante=odds_visitante,
                        odds_empate=odds_empate)
    j.save()
