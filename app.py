import os
from flask import Flask, render_template, session, redirect, request, url_for
from flask_dance.consumer import OAuth2ConsumerBlueprint

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

iam_escape_bp = OAuth2ConsumerBlueprint(
    "oauth-iam", __name__,
    client_id=os.environ.get("IAM_CLIENT_ID"),
    client_secret=os.environ.get("IAM_CLIENT_SECRET"),
    base_url="https://iam-escape.cloud.cnaf.infn.it",
    token_url="https://iam-escape.cloud.cnaf.infn.it/token",
    authorization_url="https://iam-escape.cloud.cnaf.infn.it/authorize",
    scope="openid profile email"
)

app.register_blueprint(iam_escape_bp, url_prefix="/login")

@app.route("/")
def index():
    if not iam_escape_bp.session.authorized:
        return redirect(url_for("oauth-iam.login"))
    resp = iam_escape_bp.session.get("/userinfo")
    assert resp.ok
    return resp.content