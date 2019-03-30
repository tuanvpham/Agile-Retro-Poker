import requests
from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1Session
from jira.client import JIRA
import os


def read(file_path):
    """ Read a file and return it's contents. """
    with open(file_path) as f:
        return f.read()


# The Consumer Key created while setting up the "Incoming Authentication" in
# JIRA for the Application Link.
CONSUMER_KEY = os.environ['OauthKey']
CONSUMER_SECRET = os.environ['dont_care']
VERIFIER = os.environ['jira_verifier']

# The contents of the rsa.pem file generated (the private RSA key)
RSA_KEY = read('jira_privatekey.pem')

# The URLs for the JIRA instance
JIRA_SERVER = 'https://agilecommandcentralgroup10.atlassian.net'
REQUEST_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/request-token'
AUTHORIZE_URL = JIRA_SERVER + '/plugins/servlet/oauth/authorize'
ACCESS_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/access-token'


def connect_1():
    # Step 1: Get a request token
    oauth = OAuth1Session(CONSUMER_KEY, signature_type='auth_header',
                          signature_method=SIGNATURE_RSA, rsa_key=RSA_KEY)
    request_token = oauth.fetch_request_token(REQUEST_TOKEN_URL)
    resource_owner_key = request_token['oauth_token']
    resource_owner_secret = request_token['oauth_token_secret']

    redir_url = (AUTHORIZE_URL + "?oauth_token=" +
                request_token['oauth_token'] +
                "&oauth_callback=http://agilecentralcommand.us-east-2.elasticbeanstalk.com/oauth_user" +
                "?oauth_token_secret=" + resource_owner_secret)

    access_tokens = {
        'oauth_token': resource_owner_key,
        'oauth_token_secret': resource_owner_secret,
        'oauth_url': redir_url
    }
    return access_tokens


def connect_2(resource_owner_key, resource_owner_secret):
    oauth = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=VERIFIER,
        signature_method=SIGNATURE_RSA,
        rsa_key=RSA_KEY
    )
    # Step 3: Get the access token
    access_token = oauth.fetch_access_token(ACCESS_TOKEN_URL)
    jira_options = {
        'access_token': access_token['oauth_token'],
        'access_token_secret': access_token['oauth_token_secret'],
        'consumer_key': CONSUMER_KEY,
        'key_cert': RSA_KEY
    }
    return jira_options
