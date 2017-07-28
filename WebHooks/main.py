"""Sample webhook in Python 2.7, demonstrating how to check signature and get data"""
import argparse
import hmac
import hashlib

# Use Flask framework
from flask import Flask, request
from flask_restful import Resource, Api

class ColourBot(Resource):
    """Simple webhook Flask class"""
    def __init__(self):
        """The HMAC secret"""
        self.hmac_key = PARSER_ARGS.hmac_key

    def post(self):
        """This receives requests that use the POST method."""
        json_data = request.get_json()
        headers = request.headers
        if self.hmac_key:
            try:
                # check for X-Hub-Signature (only HTTPS)
                x_hub_signature = headers['X-Hub-Signature']
                # signature is always HMAC SHA256
                hash_sent = x_hub_signature.replace("sha256=", "").strip()
            except KeyError:
                print("No signature sent")
            else:
                data_bytes = request.get_data("utf8")
                hasher = hmac.new(self.hmac_key, digestmod=hashlib.sha256)
                hasher.update(data_bytes)
                hex_digest = hasher.hexdigest()
                if not hex_digest == hash_sent:
                    # signature mismatch, return HTTP 400 error
                    return "invalid signature", 400
                else:
                    print ("Signatures match")

        intent = json_data['intentName']
        variables = json_data['variablesMap']

        # Captures the variable labelled 'colour' and its value.
        colour_variable = variables['colour']
        colour = colour_variable['value']

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
            # A default answer if we don't have an option for that value.
            result = "I don't recognise that colour."

        # The response in the form {"text": "_ is the colour of _."} and an OK.
        return {"text": result}, 200


if __name__ == "__main__":
    """Initialization of the server from command line, taking various arguments, type -h for help"""
    PARSER = argparse.ArgumentParser(description='Example bot launcher')
    PARSER.add_argument('--port', help='port to serve on', type=int,
                        default=5000)
    PARSER.add_argument('--hmac-key', help='HMAC-SHA256 secret')
    
    PARSER_ARGS = PARSER.parse_args()

    APP = Flask(__name__)
    API = Api(APP)
    API.add_resource(ColourBot, '/')
    
    APP.run(host='0.0.0.0', debug=True, port=PARSER_ARGS.port)
