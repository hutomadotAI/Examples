# WebHook Example
In this folder there are several files relating to using WebHooks in the platform, as an example of what the requests and responses look like, and example code for how to use them.

## The Request  
Here is an example of the JSON payload your endpoint will receive when a request is made from our service. It currently contains three main attributes for you to use.

```JSON
{
  "intentName": "colour",
  "variablesMap": {
    "colour": {
      "entity": "colour",
      "value": "blue",
      "mandatory": true,
      "entity_keys": [
        "blue",
        "green",
        "red",
        "yellow"
      ],
      "prompts": [
        "colour?"
      ],
      "times_prompted": 0,
      "max_prompts": 3,
      "persistent": false,
      "system_entity": false,
      "label": "colour",
      "requested": false
    }
  },
  "chatResult": {
    "score": 0.937956076610585,
    "query": "i like the colour blue",
    "answer": "Sorry no response",
    "elapsedTime": 1.214
  }
}
```

The first attribute is the **intentName** attribute. The intentName attribute is simply that, the name of the intent that you created in the platform that you've triggered to use your endpoint.

The second is the **variablesMap** attribute. This contains a dictionary of entity variables that your intent has captured, with some extra information. It will tell you the:  
**value** - The current value held by the variable.  
**mandatory** - Whether this variable was mandatory.  
**entity_keys** - The possible values that this variable could have, including the current value.  
**prompts** - The prompts used to ascertain this value.  
**times_prompted** - The number of times the user was prompted to capture the value.  
**max_prompts** - The maximum number of times to prompt the user.  

The third is the **chatResult** attribute. One key of interest is:  
**query** - What the user has said to prompt this call.

## The Response
Currently, the response you must return is very simple, as shown below. It requires a JSON response, that takes a single attribute, **text**, which is the text response you want to return to the user. If this is left blank, it will default to one of the responses specified in the intent.

```JSON
{
  "text":"Blue is the colour of the sky."
}
```

## Webhook signature
If you provide an HTTPS endpoint for your webhook, then the HTTP call will be signed with the signature value sent in the `X-Hub-Signature` HTTP header.

The HTTP message's content will be signed using HMAC SHA256, using a "Webhook signing secret" that you can obtain via your Bot's setting page in the developer console.

## Example Code
We've provided an example Python in [main.py](main.py) program that demonstrates how to handle the example payload, including how to validate the signature. To use this example, you will need to install Flask Restful which can be achieved with pip:  
`pip install flask-restful`

A requirements.txt file is included that lists all 3rd party modules required. 

Flask Restful is compatible with most versions of Python, please check their [documentation](http://flask-restful.readthedocs.io/en/0.3.5/installation.html) to check compatibility.
