import sqlite3
import datetime

class JeopardyDatabase:
    def __init__(self, name: str = "jeopardy.db"):
        self.db = sqlite3.connect(name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.cursor = self.db.cursor()

    def createTable(self) -> None:
        '''Creates a new table named QUESTIONS in the database'''
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS QUESTIONS(DATE TIMESTAMP PRIMARY KEY, TWEETID INT NOT NULL, CATEGORY TEXT NOT NULL, VALUE INT NOT NULL, QUESTION TEXT NOT NULL, ANSWER TEXT NOT NULL)
        """)
        self.db.commit()

    def insertQuestion(self, tweetid: int, category: str, value: int, question: str, answer: str) -> None:
        '''Inserts a question into the QUESTIONS database'''
        try:
            now = datetime.datetime.now()
            currentDate = "{:04d}-{:02d}-{:02d}".format(now.year, now.month, now.day)
            self.cursor.execute('''INSERT INTO QUESTIONS(DATE, TWEETID, CATEGORY, VALUE, QUESTION, ANSWER) VALUES(?, ?, ?, ?, ?)''', (currentDate, tweetid, category, value, question, answer))

        except sqlite3.IntegrityError:
            print("Invalid Entry")

    def getQuestionOn(self, date: datetime.datetime) -> tuple:
        '''Gets the data from a certain day'''
        currentDay = "{:04d}-{:02d}-{:02d}".format(date.year, date.month, date.day)
        nextDate = date + datetime.timedelta(days = 1)
        nextDay = "{:04d}-{:02d}-{:02d}".format(nextDate.year, nextDate.month, nextDate.day)
        self.cursor.execute('''SELECT * FROM QUESTIONS WHERE DATE(DATE) >= "{}" AND DATE(DATE) < "{}"'''.format(currentDay, nextDay))
        return self.cursor.fetchone()

    def close(self):
        '''Closes the connection to the database'''
        self.db.commit()
        self.db.close()
        