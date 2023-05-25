import requests
import json


url = 'https://wttr.in/?format=j1&lang=uk'

r = requests.get(url)
content = r.content.decode('utf-8').strip('\n')
data = json.loads(content)


def real_temp(fahrenheit: int):
    celsius = (fahrenheit - 32) / (9 / 5)
    if celsius > 0:
        return f'+{round(celsius)}'
    return str(round(celsius))


def cut_the_text(value: str):
    if len(value) > 15:
        a, b, c = value.split()
        s = f"{a[:4]}.{b[:4]}.{c[:4]}"
        return s
    return value


weatherDesc = data['current_condition'][0]['lang_uk'][0]['value']
temp_C = real_temp(int(data["current_condition"][0]['temp_F']))
feelsLike_C = data["current_condition"][0]['FeelsLikeC']
full_temp = f'{temp_C}({feelsLike_C})°C'
wind_course = data["current_condition"][0]["winddir16Point"]
wind = wind_course+' '+data["current_condition"][0]["windspeedKmph"]+" km/h"
precipitation = data["current_condition"][0]['precipMM'] + ' mm'
sun_rise = data["weather"][0]['astronomy'][0]["sunrise"]
sun_set = data["weather"][0]['astronomy'][0]["sunset"]
sunshine = f"{sun_rise.strip(' AM')} - {sun_set.replace(' ', '')}"

# tomorrow weather

temp_C_next = real_temp(int(data["weather"][1]['hourly'][4]['tempF'])) + '°C'
precip_morn_6 = data['weather'][1]['hourly'][2]['precipMM'] + ' mm'
precip_morn_12 = data['weather'][1]['hourly'][4]['precipMM'] + ' mm'
# prec_morn_descr_next = f'Опади(6:00) {precip_morn}'
weatherDesc_next = data['weather'][1]['hourly'][4]['lang_uk'][0]['value']
# weatherDesc_next = data['weather'][1]['hourly'][4]['weatherDesc'][0]['value']
region = data['nearest_area'][0]['region'][0]['value']


print(f"\
{region.center(26+len(region), '-')}\n\
Сьогодні:         Завтра:\n\
{weatherDesc.ljust(13)} {weatherDesc_next.ljust(12)}\n\
{full_temp.ljust(10)} {temp_C_next.rjust(11)}\n\
ОПАДИ:\n\
{precipitation.ljust(10)} {precip_morn_6.rjust(13)}(6:00)\n\
             {precip_morn_12.rjust(11)}(12:00)\n\
{wind}\n\
{sunshine}\
")
