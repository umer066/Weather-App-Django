import os
from django.shortcuts import render
from django.contrib import messages
import requests 
import datetime
from dotenv import load_dotenv # type: ignore

# Create your views here.
load_dotenv()

API_KEY = os.getenv('API_KEY')


def home(request):
    
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Pakistan'
        
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    #   convert temp into celsius and farenheit's
    PARAMS = {'units':'metric'}  


# using try and except statement to handle key-error 
    try:

        data = requests.get(url,params=PARAMS).json()

        # data description of weather
        description = data ['weather'][0]['description']
        # description of weather icon 
        icon = data ['weather'][0]['icon']
         # description of temperature of weather 
        temp = data['main']['temp']


        day = datetime.date.today()
        time = datetime.datetime.now().time()


        return render(request,'index.html', {'description': description, 'icon':icon, 'temp':temp, 'day':day, 'time':time, 'city':city, 'exception_occured':False})
    
    except:
        exception_occcured= True
        messages.error(request,'Entered city is not in System!, Try another city')
        day = datetime.date.today()
        time = datetime.datetime.now().time()

        return render(request,'index.html', {'description': 'clear sky', 'icon':'01d', 'temp':'25', 'day':day, 'time':time, 'city':'Enter another city', 'exception_occured':True})



    