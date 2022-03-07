

from datetime import datetime
from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    
    appid = "b73a30fce13d7789baabaae9578c3aa0"
    city_id = 0
    s_city = "Москва"

    if request.method == 'POST':
         s_city = request.POST['city']

    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                    params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                for d in data['list']]
        city_id = data['list'][0]['id']
    except Exception as e:
        pass
    
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': 'b73a30fce13d7789baabaae9578c3aa0'})
    data = res.json()

    url_icon = 'http://openweathermap.org/img/wn/'+ data['weather'][0]['icon']+'@2x.png'
    dt = datetime.utcfromtimestamp(int(data['dt'])+int(data['timezone'])).strftime('%d.%m %H:%M')
    wind_direction = ''
    if data['wind']['deg'] >= 0 and data['wind']['deg'] <= 23:
        wind_direction='С'
    elif data['wind']['deg'] > 23  and data['wind']['deg'] <= 68:
        wind_direction='СВ'
    elif data['wind']['deg'] > 68 and data['wind']['deg'] <= 113:
        wind_direction='В'
    elif data['wind']['deg'] > 113 and data['wind']['deg'] <= 158:
        wind_direction='ЮВ' 
    elif data['wind']['deg'] > 158 and data['wind']['deg'] <= 203:
        wind_direction='Ю'
    elif data['wind']['deg'] > 203 and data['wind']['deg'] <= 248:
        wind_direction='ЮЗ'       
    elif data['wind']['deg'] > 248 and data['wind']['deg'] <= 293:
        wind_direction='З'     
    elif data['wind']['deg'] > 293 and data['wind']['deg'] <= 338:
        wind_direction='СЗ'
    else:
        wind_direction='С'   
        
    
    
    context = {
        'city': data['name'],
        'description':data['weather'][0]['description'],
        'temp': round(data['main']['temp']),
        'feels_like': round(data['main']['feels_like']),
        'pressure': round(data['main']['pressure'] * 0.750063755419211),
        'humidity':data['main']['humidity'],
        'speed':data['wind']['speed'],
        'deg':wind_direction,
        'dt':dt,
        'icons':url_icon,

    } 
    return render(request,'mainapp/index.html',{'context': context})