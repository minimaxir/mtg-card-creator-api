from flask import Flask, request, jsonify, make_response
import subprocess
import pexpect
import time
import base64
import os
import uuid
import logging

p = pexpect.spawn('wine mse.exe --cli --raw', cwd="MSE", timeout=60)
p.expect(".*has been updated.")

app = Flask(__name__)


@app.route('/', methods=['POST'])
def homepage():
    params = request.get_json()
    encoded_text = params['text']
    unique_id = uuid.uuid4().hex
    file_ext = params.get('ext', 'jpg')

    card_file_name = '{}.{}'.format(unique_id, file_ext)

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
    p.sendline(':load card.mse-set')
    p.expect('0')
    p.sendline(
        'write_image_file(set.cards.0, file: "{}")'.format(card_file_name))
    p.expect('0')

    while not os.path.exists("MSE/{}".format(card_file_name)):
        time.sleep(0.5)

    try:
        card_image = base64.b64encode(
            open("MSE/{}".format(card_file_name), "rb").read()).decode('utf-8')
        os.remove("MSE/{}".format(card_file_name))
    except:
        card_image = ''

    r = make_response(jsonify({'text_format': gatherer_text,
                               'image': card_image}))

    r.headers['Access-Control-Allow-Origin'] = '*'

    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
