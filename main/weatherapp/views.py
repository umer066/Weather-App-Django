from django.shortcuts import render
from django.contrib import messages
import requests 
import datetime

# Create your views here.

def home(request):
    
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'city not available'
        
    url =f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=4d3d3bc9db9b9a96a18cf552234e881b'

    #   convert temp into celsius and farenheit's
    PARAMS = {'units':'metric'}  


# using try and except statement to handle key-error 
    try:

        data = requests.get(url,PARAMS).json()

        # data description of weather
        description = data ['weather'][0]['description']
        # description of weather icon 
        icon = data ['weather'][0]['icon']
         # description of temperature of weather 
        temp = data['main']['temp']


        day = datetime.date.today()
        time = datetime.time()


        return render(request,'index.html', {'description': description, 'icon':icon, 'temp':temp, 'day':day, 'time':time, 'city':city, 'exception_occured':False})
    
    except:
        exception_occcured= True
        messages.error(request,'entered is not availble')
        day = datetime.date.today()
        time = datetime.time()

        return render(request,'index.html', {'description': 'clear sky', 'icon':'01d', 'temp':'25', 'day':day, 'time':time, 'city':'city not available', 'exception_occured':True})



    