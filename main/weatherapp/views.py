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

        response = requests.get(url, params=PARAMS, timeout=10)
        response.raise_for_status()

        data = response.json()

        # data description of weather, icon and temperature
        description = data ['weather'][0]['description']
        icon = data ['weather'][0]['icon']
        temp = data['main']['temp']

        day = datetime.date.today()
        time = datetime.datetime.now().time()


        return render(request,'index.html', {
            'description': description, 
            'icon':icon,
            'temp':temp,
            'day':day,
            'time':time, 
            'city':city,
            'exception_occured':False})
    
   
    except requests.exceptions.Timeout:
        messages.error(request, "The request time out. PLease try again later.")
        exception_occurred = True

    except requests.exceptions.ConnectionError:
        messages.error(request, "There was a connection error.  Please check your internet connection.")
        exception_occurred = True

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            messages.error(request, "The requested city was not found.")
        else:
            messages.error(request, f"HTTP error occurred: {http_err}")
        exception_occurred = True

    except requests.exceptions.RequestException as req_err:
        messages.error(request,f"An error occurred while fetching data: {req_err}")
        exception_occcured = True

    except KeyError as key_err:
        messages.error(request, f"Excepted data not found: {key_err}. Please try another city.")
        exception_occcured = True

    except ValueError :
        messages.error(request, "Invalid response received from the server.")
        exception_occcured = True

    except  Exception as err:
        messages.error(request, f"An excepted error occurred: {err}")
        exception_occcured == True


    day = datetime.date.today()
    time = datetime.datetime.now().time()

    return render(request,'index.html', {
        'description': 'N/A', 
        'icon':'01d', 
        'temp':'N/A', 
        'day':day, 
        'time':time, 
        'city':'Enter another city', 
        'exception_occured': True})
