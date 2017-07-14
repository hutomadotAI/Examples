import argparse
from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import urllib2

class getWeather(Resource):

    def forecast(self, city):
        answer = None
        # calls the  weather API and loads the response
        res = urllib2.urlopen(weather_today + city)
        data = json.load(res)
        # gets the temperature information
        temp = data['main']['temp']
        # converts the returned temperature in Celsius
        c = temp - 273.15
        # and converts the returned temperature in fahrenheit
        f = 1.8 * (temp - 273) + 32
        # compose the answer we want to return to the user
        answer = str(
            data['weather'][0]['description']).capitalize() + '. Current temperature is %.2fC' % c + '/%.2fF' % f
        return answer

    # This recieves requests that use the POST method.
    def post(self):
        # Uses the request parser to extract what we want from the JSON.
        args = parser.parse_args()
        variables = args['memoryVariables']
        city = variables[0]['value']

        # calls the getForecast function
        response = self.forecast(city)

        # Captures the first variable and it's currentValue.
        return {"text": response}, 200



if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Weather bot launcher')
    PARSER.add_argument('apikey', help='openweathermap API key', type=str,
                        default='')
    PARSER.add_argument('--port', help='port to serve on', type=int,
                        default=5000)
    

    BUILD_ARGS = PARSER.parse_args()
    # endpoint to a weather API
    weather_today = 'http://api.openweathermap.org/data/2.5/weather?appid={}&q='.format(BUILD_ARGS.apikey)

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(getWeather, '/getWeather')

    # Use RequestParser to pull out the intentName, memoryVariables and chatResult.
    parser = reqparse.RequestParser()
    parser.add_argument('intentName')
    parser.add_argument('memoryVariables', type=dict, action='append')
    parser.add_argument('chatResult', type=dict)

    app.run(host='0.0.0.0', debug=True, port=BUILD_ARGS.port)