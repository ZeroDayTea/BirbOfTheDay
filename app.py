from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from datetime import datetime
import random
import json

app = Flask(__name__)

BIRB_MIN = 1
BIRB_MAX = 634

# load email settings and setup for sending emails
with open('mail_settings.json') as json_file:
    mail_settings = json.load(json_file)
    app.config.update(mail_settings)
    mail = Mail(app)

# send daily birb email
def send_email(email, imgsrc, birb, date, fact):
    try:
        with app.app_context():
            birbMsg = Message(subject="Today's Birb Of The Day Is...", sender=app.config.get("MAIL_USERNAME"), recipients=[email])
            msg.html = render_template('/emails/dailybirb.html', imgsrc=imgsrc, birb=birb, date=date, fact=fact)
            mail.send(birbMsg)
    except:
        print("Error sending email")

@app.route('/')
def returnbirb():
    # get daily seed
    dateStart = datetime(2023, 1, 10)
    curDate = datetime.now()
    diff = curDate - dateStart
    random.seed(diff.days)
    birbIndex = random.randint(BIRB_MIN, BIRB_MAX)

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
            emailFile.write("\n")
            emailFile.write(email)
            emailFile.close()
            data = {"message": "Success!"}
            return jsonify(data)

if __name__ == "__main__":
    send_email("patrick.dobranowski@gmail.com", "https://www.allaboutbirds.org/guide/assets/photo/309038471-480px.jpg", "HairyWoodpecker", "January 16, 2023", "The larger of two look alikes, the Hairy Woodpecker is a small but powerful bird that forages along trunks and main branches of large trees. It wields a much longer bill than the Downy Woodpecker's almost thornlike bill. Hairy Woodpeckers have a somewhat soldierly look, with their erect, straight-backed posture on tree trunks and their cleanly striped heads. Look for them at backyard suet or sunflower feeders, and listen for them whinnying from woodlots, parks, and forests.")
    app.run()
