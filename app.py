from flask import Flask, request, jsonify, make_response
import subprocess
import base64
import os

app = Flask(__name__)


@app.route('/', methods=['POST'])
def homepage():
    params = request.get_json()
    encoded_text = params['text']

    # Write encoded text to file so it can be decoded
    with open("encoded.txt", "w") as f:
        f.write(encoded_text)

    # Decode both a Gatherer-format text and a MSE card set
    subprocess.call(['python2.7', 'mtgencode/decode.py', '-e',
                     'rfields', '-g', 'encoded.txt', 'card.txt'])
    subprocess.call(['python2.7', 'mtgencode/decode.py', '-e',
                     'rfields', '-mse', 'encoded.txt', 'MSE/card'])

    # Load decoded Gatherer text
    with open("card.txt", "r") as f:
        gatherer_text = f.read().strip()

    # Create card image and encode as base64.
    p = subprocess.Popen(['wine',
                          'mse.exe',
                          '--cli',
                          '--raw',
                          'card.mse-set'],
                         cwd="MSE",
                         stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    p.stdin.write(b'write_image_file(set.cards.0, file: "card.jpg")')
    p.communicate()[0]
    p.stdin.close()

    card_image = base64.b64encode(
        open("MSE/card.jpg", "rb").read()).decode('utf-8')

    r = make_response(jsonify({'text_format': gatherer_text,
                               'image': card_image}))

    r.headers['Access-Control-Allow-Origin'] = '*'

    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)),
            debug=True)
