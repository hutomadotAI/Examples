from json import JSONDecodeError
import requests

# where to find the API
apiRoot = "https://api.hutoma.ai/v1/"

# Your Client Key
# This can be found in the AI setting page
auth = 'YOUR_AUTH_KEY_HERE'

# The AI id
# This can be also found in the AI setting page
aiId = 'YOUR_AI_ID_HERE'


# Chat response wrapper
class ChatResponse:
    def __init__(self, callResult):
        self.success = False
        try:
            # decode from json if possible
            result = callResult.json()
            # if there is a status then the response came from the API server
            if result['status']:
                # so store a copy of the json
                self.response = result
                # copy the json result code
                code = result['status']['code']
                # assemble a description of the result
                self.text = str(code) + ': ' + result['status']['info']
                # if we got a 200 OK then the the json object has the answer data
                if code == 200:
                    self.success = True
            else:
                # otherwise, assemble a description from the HTTP results
                self.text = 'Error ' + str(callResult.status_code) + ': ' + callResult.reason
        except JSONDecodeError:
            self.text = 'Error ' + str(callResult.status_code) + ': ' + callResult.reason


# chat API call
def chat(apiRoot, auth, aiid, sayWhat, chatID=""):
    # build the query
    query = {'q': sayWhat}
    if chatID != "":
        query['chatId'] = chatID
    # add the auth header
    headers = {'Authorization': "Bearer " + auth}
    # make the http call and put the result into a wrapper
    return ChatResponse(requests.get(apiRoot + "ai/" + aiid + "/chat", params=query, headers=headers))


# history and chatId are stored between calls to keep track of the conversation
history = ""
chatId = ""

while True:
    # user input
    q = input("Human: ")
    # make the http call
    chatResponse = chat(apiRoot, auth, aiId, q, chatID=chatId)
    # if the call succeeded then print the answer and store the chatId
    if chatResponse.success:

        # gets the current chat score
        score = float(chatResponse.response["result"]["score"])
        # if the score if greater than 0.5 output the AI response. 
        # if not, redirect the conversation to a human agent
        if (score > 0.5):
            print("Ai: ", chatResponse.response["result"]["answer"])
            chatId = chatResponse.response["chatId"]
        else:
            print("Ai: Looks like I am not understanding our conversation. Let me connect you with an agent. Please wait.")
            chatId = ''
            # TODO: Add here the code that will connect with your backend
    else:
        # otherwise, tell the user what went wrong and exit
        print(chatResponse.text)
        break
