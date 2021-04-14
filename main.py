import requests
import json
import tweepy
import datetime
import twitterCredentials as tc #File containing api key, secret key, tokens

def makeTitle(s: str) -> str:
    '''Capitalizes each word in s'''
    #Because s.title() doesn't quite work with apostrophes
    output = ""
    s = s.split()

    for word in s:
        output += "{} ".format(word.capitalize())

    return output.strip()

def getJeopardyQuestion() -> dict:
    '''Gets a question from the jService API'''
    link = "https://jservice.io/api/random"
    response = requests.get(link)
    jsonData = json.loads(response.text)
    questionID = jsonData[0]["id"]
    answer = jsonData[0]["answer"]
    question = jsonData[0]["question"]
    value = jsonData[0]["value"]
    category = jsonData[0]["category"]["title"]

    questionInfo = dict()
    questionInfo["id"] = questionID
    questionInfo["answer"] = answer
    questionInfo["question"] = question
    questionInfo["value"] = value
    questionInfo["category"] = makeTitle(category)

    return questionInfo

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(tc.API_KEY, tc.API_SECRET_KEY)
    auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        jq = getJeopardyQuestion()
        message = "{} for ${}:\n{}".format(jq["category"], jq["value"], jq["question"])
        #api.update_status(message)
            
    except tweepy.error.TweepError:
        print("Authentication Error")
