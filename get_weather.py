import requests
from pprint import pprint as prnt
import json


url = 'https://wttr.in/%D0%9D%D0%BE%D0%B2%D0%BE%D0%BC%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D1%8C%D0%BA?format=j1'

r = requests.get(url)
content = r.content.decode('utf-8').strip('\n')

file = json.loads(content)

def real_temp(fahrenheit: int) -> int:
    celsius = (fahrenheit - 32) / (9 / 5) 
    if celsius > 0:
        return f'+{round(celsius)}'
    return str(round(celsius))


#TODO 1: current_condition

weatherDesc = file["current_condition"][0]['weatherDesc'][0]['value']
temp_C = real_temp(int(file["current_condition"][0]['temp_F']))
feelsLike_C = file["current_condition"][0]['FeelsLikeC']
full_temp = f'{temp_C}({feelsLike_C})°C'
wind_course = file["current_condition"][0]["winddir16Point"]
wind = wind_course + ' ' + file["current_condition"][0]["windspeedKmph"] + " km/h"
precipitation = file["current_condition"][0]['precipMM'] + ' mm'
sun_rise = file["weather"][0]['astronomy'][0]["sunrise"]
sun_set = file["weather"][0]['astronomy'][0]["sunset"]
sunshine = f"{sun_rise.strip(' AM')} - {sun_set.replace(' ', '')}"
#TODO 2: tomorrow weather

temp_C_next = real_temp(int(file["weather"][1]['hourly'][4]['tempF'])) + '°C'
precip_morn = file['weather'][1]['hourly'][2]['precipMM'] + ' mm'
prec_morn_descr_next = f'Осадки(6:00) {precip_morn}'
weatherDesc_next = file['weather'][1]['hourly'][4]['weatherDesc'][0]['value']



print(
    f"""Сейчас:         Завтра:
{weatherDesc}   {weatherDesc_next}
{full_temp}         {temp_C_next}
{wind}      {prec_morn_descr_next}
{precipitation}      
{sunshine}"""
)

