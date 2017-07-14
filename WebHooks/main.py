import argparse
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# Use RequestParser to pull out the intentName, memoryVariables and chatResult.
parser = reqparse.RequestParser()
parser.add_argument('intentName')
parser.add_argument('memoryVariables', type=dict, action='append')
parser.add_argument('chatResult', type=dict)

class HelloWorld(Resource):
    # This recieves requests that use the POST method.
    def post(self):
        # Uses the request parser to extract what we want from the JSON.
        args = parser.parse_args()
        intent = str(args['intentName'])
        variables = args['memoryVariables']

        # Captures the first variable and it's currentValue.
        colourVariable = variables[0]
        colour = colourVariable['currentValue']

        # A default answer if we don't have an option for that value.
        result = "I don't recognise that colour."

        # Set the response text based on the colour currentValue.
        if colour is "red":
            result = "Red is the same colour as a Strawberry."
        elif colour is "green":
            result = "Green is the colour of the grass."
        elif colour is "blue":
            result = "Blue is the colour of the sky."
        elif result is "yellow":
            result = "Yellow is the colour of the sun."

        # The response in the form {"text": "_ is the colour of _."} and an OK.
        return {"text": result}, 200

api.add_resource(HelloWorld, '/')

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Webhook deployment')
    PARSER.add_argument('--port', help='port to serve on', type=int,
                        default=5000)
    
    BUILD_ARGS = PARSER.parse_args()
    app.run(host='0.0.0.0', debug=True, port=BUILD_ARGS.port)
