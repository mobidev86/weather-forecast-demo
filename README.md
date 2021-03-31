# Weather forecast 

Find weather data of a place using latitude and longitude

## Setup

The first thing to do is to clone the repository:

```shell script
$ git clone https://github.com/mobidev86/weather-forecast-demo.git
$ cd weather-forecast-demo/
```

Create a virtual environment to install dependencies in and activate it:

Install python 3 and virtual environment 

Make virtualenv:


```shell script
$ virtualenv venv -p python3
``` 
 
Activate virtual environment : 


```shell script
$ source venv/bin/activate
```

Then install the dependencies:

```shell script
(venv)$ pip install -r requirement.txt
```

Once `pip` has finished downloading the dependencies:

Make database in postgresql and update database settings in .env file.

```shell script
DB_NAME=weather-forecast
DB_USER=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=5432
```

Apply Migrations:

```shell script
(venv)$ python manage.py migrate
```

Run server :
```shell script
(venv)$ python manage.py runserver
```

Register user using following post api in postman

`http://localhost:8000/register/` 


Get Authentication Token using following post api

`http://localhost:8000/api-token-auth/`

Get weather data using following post api, pass authentication token in header:

`http://localhost:8000/weather/`

body 

`{
    "detailing_type":0,
    "lat": "23.022500",
    "long": "72.571400"
}`

detailing_type choices:

```
0 for Current weather 
1 for Minute forecast for 1 hour
2 for Hourly forecast for 48 hours
3 for Daily forecast for 7 days
```