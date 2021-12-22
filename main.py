import requests
import sys
import json
from datetime import datetime
from datetime import timedelta


class WeatherForecast:
    def __init__(self):
        self.data_pogoda = []
        self.sl_historia = self.wczytaj_historie()

    def get_api_response(self):
        url = "https://visual-crossing-weather.p.rapidapi.com/forecast"

        querystring = {"aggregateHours": "24", "location": "Washington,DC,USA", "contentType": "json", "unitGroup": "us",
                       "shortColumnNames": "0"}

        headers = {
            'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com",
            'x-rapidapi-key': sys.argv[1]
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response
        print(response)

    def wczytaj_historie(self):
        with open('historia.json') as file:
            wczytaj = json.load(file)
        return wczytaj

    def __iter__(self):
        for k, v in self.sl_historia.items():
            yield k, v

    def __getitem__(self, item):
        if item in self.sl_historia:
            return self.sl_historia.get(item)
        elif datetime.strptime(item, '%Y-%m-%d').date() < datetime.now().date():
            return 'Nie wiem'
        elif datetime.strptime(item, '%Y-%m-%d').date() > (datetime.now() + timedelta(days=14)).date():
            return "nie wiem"
        else:
            response = self.get_api_response()
            sl_prognoza = {}
            for slownik in response.json()['locations']['Washington,DC,USA']['values']:
                # print(slownik['datetimeStr'], slownik['precip'])
                sl_prognoza[slownik['datetimeStr'][:10]] = 'bedzie padac' if slownik['precip'] > 0 else 'nie bedzie padac'
            self.sl_historia.update(sl_prognoza)
            self.zapisz_historie()
            return self.sl_historia[item]

    def items(self):
        for data, pogoda in self.sl_historia.items():
            self.data_pogoda.extend([data, pogoda])
        for v in self.data_pogoda:
            yield v

    def zapisz_historie(self):
        with open('historia.json', 'w') as file:
            json.dump(self.sl_historia, file)


wf = WeatherForecast()
# print(wf[...])

# for v in wf.items():
#     print(v)

for data, pogoda in wf:
    print(data, pogoda)