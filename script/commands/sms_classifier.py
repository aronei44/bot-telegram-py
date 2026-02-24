from telegram import ForceReply, Update
from telegram.ext import ContextTypes
from helpers import load_from_update
from sqlalchemy import text
from database import session
import pickle
import os
import nltk
# Define a few command handlers. These usually take the two arguments update and
# context.
async def spam_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   path = os.path.dirname(__file__)
   file = open(path+"/ml_model/supervised/lr_sms.pkl","rb")
   model = pickle.load(file)
   teks = [update.message.text]
   result = model.predict_proba(teks)
   res = result[0]
   if(res[1] >= .5):
      text = f"""
Bro/Sis, pesan anda memiliki kemungkinan pesan spam sebesar : {round(res[1]*100, 2)} %.
Yo bisa yo ga kirim pesan spam.....
hehe      
      """
      await update.message.reply_text(text)


async def info_lr_sms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = """
Spam Message Classifier

Model train yang digunakan: Logistic Regression
Dataset yang digunakan: Sms Spam Dataset
Lisensi dataset: https://creativecommons.org/licenses/by-sa/4.0/
Sumber dataset: Rahmi, F. and Wibisono, Y.  (2016). Aplikasi SMS Spam Filtering pada Android menggunakan Naive Bayes, Unpublished manuscript.

Model dilatih oleh @aronei44
    """
    await update.message.reply_text(text)

async def download_nltk(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    nltk.download('stopwords')
    nltk.download('punkt')