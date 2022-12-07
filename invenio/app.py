import os

from flask import Flask, redirect, url_for
from flask_babelex import Babel
from flask_login import current_user
from flask_menu import Menu as FlaskMenu
from invenio_accounts import InvenioAccounts
from invenio_accounts.views import blueprint as blueprint_user
from invenio_db import InvenioDB
from invenio_mail import InvenioMail
from invenio_userprofiles import InvenioUserProfiles
from invenio_userprofiles.views import blueprint_ui_init as blueprint_userprofile_init

from invenio_oauthclient import InvenioOAuthClient
from invenio_oauthclient.contrib import github
from invenio_oauthclient.views.client import blueprint as blueprint_client
from invenio_oauthclient.views.settings import blueprint as blueprint_settings

from invenio_oauthclient._compat import monkey_patch_werkzeug  # noqa isort:skip

monkey_patch_werkzeug()  # noqa isort:skip

from flask_oauthlib.client import OAuth as FlaskOAuth  # noqa isort:skip

OAUTHCLIENT_REMOTE_APPS = dict(
    myapp=dict(
        title='IAM ESCAPE',
        description='IAM ESCAPE Test',
        authorized_handler="invenio_oauthclient.handlers"
                   ":authorized_default_handler",
        disconnect_handler="invenio_oauthclient.handlers"
                   ":disconnect_handler",
        params=dict(
            request_token_params={'scope': 'email'},
            base_url='https://iam-escape.cloud.cnaf.infn.it/',
            request_token_url=None,
            access_token_url="https://iam-escape.cloud.cnaf.infn.it/token",
            access_token_method='POST',
            authorize_url="https://iam-escape.cloud.cnaf.infn.it/authorize",
            app_key="IAM_ESCAPE_APP_CREDENTIALS",
        ),
        )
    )

IAM_ESCAPE_APP_CREDENTIALS = dict(
    consumer_key=os.environ.get("IAM_CLIENT_ID"),
    consumer_secret=os.environ.get("IAM_CLIENT_SECRET"),
)

# Create Flask application
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI", "sqlite:///app.db"
)

app.config.update(
    ACCOUNTS_USE_CELERY=False,
    CELERY_ALWAYS_EAGER=True,
    CELERY_CACHE_BACKEND="memory",
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    CELERY_RESULT_BACKEND="cache",
    MAIL_SUPPRESS_SEND=True,
    SECRET_KEY="CHANGE_ME",
    SECURITY_PASSWORD_SALT="CHANGE_ME_ALSO",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    APP_THEME=["semantic-ui"],
    THEME_ICONS={"semantic-ui": dict(link="linkify icon")},
)

Babel(app)
FlaskMenu(app)
InvenioDB(app)
InvenioAccounts(app)
FlaskOAuth(app)
InvenioOAuthClient(app)

app.register_blueprint(blueprint_client)
app.register_blueprint(blueprint_settings)
app.register_blueprint(blueprint_accounts)

InvenioAdmin(app, permission_factory=lambda x: x, view_class_factory=lambda x: x)