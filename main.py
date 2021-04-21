import requests
import json
import tweepy
import datetime
import time
import twitterCredentials as tc #File containing api key, secret key, tokens
import jeopardyDatabase

#TO-DO: Refactor

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
    answer = jsonData[0]["answer"]
    question = jsonData[0]["question"]
    value = jsonData[0]["value"]
    category = jsonData[0]["category"]["title"]

    questionInfo = dict()
    questionInfo["answer"] = answer
    questionInfo["question"] = question
    questionInfo["value"] = value
    questionInfo["category"] = makeTitle(category)

    return questionInfo

def getValidQuestion(tries: int = 10) -> dict:
    '''Keeps trying to pull a Jeopardy question with no None values'''
    while tries > 0:
        tries -= 1
        question = getJeopardyQuestion()

        if all(question.values()): #Check if every value of question is not None
            return question

        else:
            time.sleep(5) #Wait 5 seconds before calling the jService API again

    return None #Return None if failed after all tries
        

if __name__ == "__main__":
    jd = jeopardyDatabase.JeopardyDatabase()
    jd.createTable()
    auth = tweepy.OAuthHandler(tc.API_KEY, tc.API_SECRET_KEY)
    auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        lastHour = datetime.datetime.now() - datetime.timedelta(hours = 1)
        lastQuestion = jd.getHourQuestion(lastHour)
        
        if lastQuestion != None:
            api.update_status("Correct Response: {}".format(lastQuestion[5]), lastQuestion[1])
        
        jq = getValidQuestion()
        message = "{} for ${}:\n{}".format(jq["category"], jq["value"], jq["question"])
        api.update_status(message)
        tweetID = api.user_timeline(screename = tc.BOT_HANDLE, count = 1)[0].id
        jd.insertQuestion(tweetID, jq["category"], jq["value"], jq["question"], jq["answer"])
        

    except tweepy.error.TweepError:
        print("Authentication Error")

    jd.close()
