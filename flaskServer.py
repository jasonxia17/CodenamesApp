from flask import Flask, request, jsonify
from cluegiver import getClues
import base64
from boxRecognition import imageToWordList

app = Flask(__name__)

@app.route('/clue', methods=['POST'])
def handleClueRequest():
    import time
    t0 = time.time()
    jsonContent = request.get_json()
    try:
        result = getClues(jsonContent['wordObjectList'], jsonContent['teamName'])
        print(time.time() - t0)
        return jsonify(result)
    except ValueError as err:
        return jsonify({'err': str(err)})

@app.route('/photo', methods=['POST'])
def handlePhotoRequest():
    im_json = request.get_json()
    with open("requestPhoto.jpg", "wb") as output:
        output.write(base64.b64decode(im_json["imageBase64"]))
    wordList = imageToWordList("requestPhoto.jpg")
    return jsonify(wordList)

@app.route('/<name>', methods=['GET', 'POST'])
def hello_name(name):
    return name + ' is not a valid route'

if __name__ == '__main__':
   app.run(host='0.0.0.0')