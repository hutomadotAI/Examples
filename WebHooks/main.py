import argparse
from flask import Flask
from flask_restful import Resource, Api, reqparse

class HelloWorld(Resource):
    # This recieves requests that use the POST method.
    def post(self):
        # Uses the request parser to extract what we want from the JSON.
        args = REQUEST_PARSER.parse_args()
        intent = str(args['intentName'])
        variables = args['variablesMap']

        # Captures the first variable and it's currentValue.
        colour_variable = variables['colour']
        colour = colour_variable['value']

        print("colour is " + colour)

        # A default answer if we don't have an option for that value.

        # Set the response text based on the colour currentValue.
        if colour == "red":
            result = "Red is the same colour as a Strawberry."
        elif colour == "green":
            result = "Green is the colour of the grass."
        elif colour == "blue":
            result = "Blue is the colour of the sky."
        elif colour == "yellow":
            result = "Yellow is the colour of the sun."
        else:
            result = "I don't recognise that colour."

        # The response in the form {"text": "_ is the colour of _."} and an OK.
        return {"text": result}, 200


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Example bot launcher')
    PARSER.add_argument('--port', help='port to serve on', type=int,
                        default=5000)
    
    BUILD_ARGS = PARSER.parse_args()

    APP = Flask(__name__)
    API = Api(APP)

    # Use RequestParser to pull out the intentName, memoryVariables and chatResult.
    REQUEST_PARSER = reqparse.RequestParser()
    REQUEST_PARSER.add_argument('intentName')
    REQUEST_PARSER.add_argument('variablesMap', type=dict)
    REQUEST_PARSER.add_argument('chatResult', type=dict)
    API.add_resource(HelloWorld, '/')
    
    APP.run(host='0.0.0.0', debug=True, port=BUILD_ARGS.port)
