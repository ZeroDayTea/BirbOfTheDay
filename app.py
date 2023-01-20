from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from datetime import datetime
import random
import json
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup

app = Flask(__name__)

BIRB_MIN = 1
BIRB_MAX = 634

# load email settings and setup for sending emails
with open('mail_settings.json') as json_file:
    mail_settings = json.load(json_file)
    app.config.update(mail_settings)
    mail = Mail(app)
    
# get daily seed
def get_seed():
    # get daily seed
    dateStart = datetime(2023, 1, 10)
    curDate = datetime.now()
    diff = curDate - dateStart
    random.seed(diff.days)
    birbIndex = random.randint(BIRB_MIN, BIRB_MAX)
    return birbIndex

# send daily birb email to individual
def send_email(email, imgsrc, birb, date, description, link, fact1, fact2, fact3, fact4, fact5):
    try:
        with app.app_context():
            birbMsg = Message(subject="Today's Birb Of The Day Is...", sender=app.config.get("MAIL_USERNAME"), recipients=[email])
            birbMsg.html = render_template('/emails/dailybirb.html', imgsrc=imgsrc, birb=birb, date=date, description=description, link=link, fact1=fact1, fact2=fact2, fact3=fact3, fact4=fact4, fact5=fact5)
            mail.send(birbMsg)
    except Exception as e:
        print("Error sending email")
        print(e)

def mass_email():
    birbIndex = get_seed()

    # retrieve birb data
    birbfile = open("birds.json")
    birbs = json.load(birbfile)
    dailyBirb = birbs[str(birbIndex)]

    # retrieve email list
    emailFile = open("emails.txt")
    emails = emailFile.readlines()
    
    # some webscraping to get facts and description from page
    print(dailyBirb["url"])
    url = dailyBirb["url"]
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'}
    res = requests.get(url, headers=headers)
    data = res.text
    data = data.replace("\n", "")
    description = BeautifulSoup(data.split('Description</h2><p>')[1].split('</p>')[0], 'lxml').text

    factsSection = data.split('Cool Facts')[1].split('</div></section>')[0]
    factsSection = factsSection.replace("\n", "")
    fact1 = BeautifulSoup(factsSection.split('<ul><li>')[1].split('</li>')[0], 'lxml').text
    fact2 = BeautifulSoup(factsSection.split('</li><li>')[1].split('</li>')[0], 'lxml').text
    fact3 = BeautifulSoup(factsSection.split('</li><li>')[2].split('</li>')[0], 'lxml').text
    fact4 = BeautifulSoup(factsSection.split('</li><li>')[3].split('</li>')[0], 'lxml').text
    fact5 = BeautifulSoup(factsSection.split('</li><li>')[4].split('</li>')[0], 'lxml').text
    
    today = datetime.now().strftime("%B %d, %Y")

    # retrieve map information
    mapsImage = data.split('maps-range">')[1].split('</a>')[0]

    # send email to each individual
    for email in emails:
        send_email(email.strip(), dailyBirb["imageurl"], dailyBirb["name"], today, description, url, fact1, fact2, fact3, fact4, fact5)
    
# run mass email every day at 12:00 AM using APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=mass_email, trigger="interval", hours=24)
scheduler.start()

@app.route('/')
def returnbirb():
    birbIndex = get_seed()

    # retrieve birb data
    birbfile = open("birds.json")
    birbs = json.load(birbfile)
    dailyBirb = birbs[str(birbIndex)]
    return render_template("index.html", imgurl=dailyBirb["imageurl"], name=dailyBirb["name"], family=dailyBirb["family"], url=dailyBirb["url"])

@app.route('/addemail', methods=['POST'])
def addemail():
    if request.method == 'POST':
        email = request.form.get("email")
        if email is None or email == "":
            data = {"message": "Error: email not provided"}
            return jsonify(data)
        else:
            print(json.dumps(request.form))
            # add individual's email to daily email list
            emailFile = open("emails.txt", "a")
            emailsList = emailFile.read()
            emailsList = emailsList.split("\n")
            if email in emailsList:
                data = {"message": "Error: email already subscribed"}
                return jsonify(data)
            emailFile.write("\n")
            emailFile.write(email)
            emailFile.close()
            data = {"message": "Success!"}
            return jsonify(data)

if __name__ == "__main__":
    mass_email()
    app.run()
