from flask import Flask, request, jsonify, make_response
import subprocess
import base64
import os
import uuid

app = Flask(__name__)

gen_images = 0

@app.route('/', methods=['POST'])
def homepage():
    global gen_images
    params = request.get_json()
    encoded_text = params['text']
    unique_id = uuid.uuid4().hex
    file_ext = params.get('ext', 'jpg')

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
    p = subprocess.Popen('wine mse.exe --cli --raw card.mse-set',
                         cwd="MSE", shell=True,
                         stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    p.stdin.write(str.encode('write_image_file(set.cards.0, file: "{}.{}")'.format(unique_id, file_ext)))
    p.communicate()[0]
    p.stdin.close()

    # Kill the wineserver periodically to prevent death
    gen_images += 1
    if gen_images == 20:
        subprocess.Popen('wineserver -k', shell=True)
        gen_images == 0

    card_image = base64.b64encode(
        open("MSE/{}.{}".format(unique_id, file_ext), "rb").read()).decode('utf-8')
    os.remove("MSE/{}.{}".format(unique_id, file_ext))

    r = make_response(jsonify({'text_format': gatherer_text,
                               'image': card_image}))

    r.headers['Access-Control-Allow-Origin'] = '*'

    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
