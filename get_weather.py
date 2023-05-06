import requests
import json


url = 'https://wttr.in/?format=j1'

r = requests.get(url)
content = r.content.decode('utf-8').strip('\n')

file = json.loads(content)

def real_temp(fahrenheit: int) -> int:
    celsius = (fahrenheit - 32) / (9 / 5) 
    if celsius > 0:
        return f'+{round(celsius)}'
    return str(round(celsius))


def cut_the_text(value: str):
    if len(value) > 15:
        a,b,c = value.split()
        s =  f"{a[:4]}.{b[:4]}.{c[:4]}"
        return s
    return value

#weatherDesc = file["current_condition"][0]['weatherDesc'][0]['value']
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

#tomorrow weather

temp_C_next = real_temp(int(file["weather"][1]['hourly'][4]['tempF'])) + '°C'
precip_morn_6 = file['weather'][1]['hourly'][2]['precipMM'] + ' mm'
precip_morn_12 = file['weather'][1]['hourly'][4]['precipMM'] + ' mm'
#prec_morn_descr_next = f'Опади(6:00) {precip_morn}'
weatherDesc_next = file['weather'][1]['hourly'][4]['weatherDesc'][0]['value']
city = file['nearest_area'][0]['areaName'][0]['value']

if __name__ == '__main__':
    print(
f"""Сьогодні:         Завтра:
{cut_the_text(weatherDesc)}    {cut_the_text(weatherDesc_next)}
{full_temp}         {temp_C_next}
ОПАДИ:
{precipitation}           (6:00) {precip_morn_6}
                (12:00) {precip_morn_12}
{wind}
{sunshine}"""
    )


