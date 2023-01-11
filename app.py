from flask import Flask, render_template
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

def run():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    run()
