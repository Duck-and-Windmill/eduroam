from flask import Flask, render_template, request
import json
import os
import base64
import codecs
import data.classifier
import kairos_face
import credentials
import numpy as np
import nutrition_data as BiggestNut
from nutrition import find_food_nutrition
from refine import refine_results

kairos_face.settings.app_id = credentials.app_id
kairos_face.settings.app_key = credentials.key


template_dir = os.path.abspath('static')
app = Flask(__name__, template_folder=template_dir)
user = False

@app.route('/')
def main():
    print(kairos_face.get_gallery("hackathon"))
    return render_template("index.html")

@app.route('/send-static-image',  methods=["POST"])
def sendStaticImage():
    print('recieved image')
    save_image(request.form['image'], 'stream.jpg')

    model = data.classifier.model()
    pred = model.predict_class('stream.jpg')

    print(pred)

    possibilities = [item for (item_id, item, confidence) in pred[0]]
    print(possibilities)

    bestGuess = refine_results(possibilities[0])
    if (bestGuess == 'pomegranate' or bestGuess == "punching_bag"):
        bestGuess = "apple"

    elif (bestGuess == 'harp'):
        bestGuess = 'banana'

    elif (bestGuess == "pretzel"):
        bestGuess = 'bagel'

    elif (bestGuess == 'bow_tie' or bestGuess=='hair_spray' or bestGuess=="maraca"):
        bestGuess = "grape"

    elif (bestGuess == 'shower_cap' or bestGuess == "king_crab"):
        bestGuess = "muffin"

    elif bestGuess == "torch":
        bestGuess = "ramen"

    bestGuesses = json.dumps(possibilities)

    print(find_food_nutrition(bestGuess))

    return json.dumps({
        'food': bestGuess,
        'nutrition': find_food_nutrition(bestGuess)
    })
    # #look up facts
    # print('Looking up Nutrition facts for: ', bestGuess)
    # Nuts = BiggestNut.get_nutrition_data(bestGuess)
    # # Nut=json.dumps(Nuts)
    # print(Nuts)
    # results=[possibilities, Nuts]
    # resultsString=json.dumps(results)
    # return resultsString
    # # classifier.model("test.png")

    # return 'finished'


@app.route('/register-face', methods=['POST'])
def register_face():
    save_image(request.form['image'], 'face.jpg')
    print(kairos_face.enroll_face(file='face.jpg', subject_id=request.form['name'], gallery_name='hackathon'))
    return 'finished'

@app.route('/check-face', methods=['POST'])
def check_face():
    save_image(request.form['image'], 'face.jpg')
    response = kairos_face.recognize_face(file='face.jpg', gallery_name='hackathon')
    print(response)
    match = response['images'][0]['candidates'][0]
    print(match)
    return match['subject_id']

def save_image(raw_data, name):
    image64 = raw_data.split(',')[1]
    image_data = bytes(image64, encoding='ascii')

    with open(name, 'wb') as f:
        f.write(base64.decodebytes(image_data))


if __name__ == "__main__":

    app.run()
