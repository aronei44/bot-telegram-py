from database import session
from models.message_logs import MessageLogs
from models.members import Member
from datetime import datetime
import psycopg2


def logger(id, message, user_id, date = datetime.now()) -> None:
    try:
        data = MessageLogs(id, {"text":message}, date, user_id)
        session.add(data)
        session.commit()
    except Exception as e:
        print("ERROR : ", str(e))
        session.rollback()

def saveuser(user) -> None:
    try:
        data = Member(id=user['id'],name=user['first_name'],username=user['username'])
        session.add(data)
        session.commit()
    except psycopg2.errors.UniqueViolation as e:
        session.rollback()
    except Exception as e:
        print("ERROR : ", str(e))
        session.rollback()


def response(input_text) -> str:
    saveuser(input_text['user'])
    logger(input_text['message_id'], input_text['text'], input_text['user']['id'])
    return str(input_text)