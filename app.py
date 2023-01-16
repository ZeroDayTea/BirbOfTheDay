from flask import Flask, render_template, request, jsonify
from datetime import datetime
import random
import json

app = Flask(__name__)

BIRB_MIN = 1
BIRB_MAX = 634

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
    app.run()
