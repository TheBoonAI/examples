import os
import logging

import boonsdk
from boonsdk.entity.webhook import validate_webhook_request_headers

import slack_sdk
import flask


WEBHOOK_SECRET = os.environ['WEBHOOK_SECRET']
SLACK_TOKEN = os.environ['SLACK_TOKEN']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']

SLACK_CLIENT = slack_sdk.WebClient(token=SLACK_TOKEN)


logger = logging.getLogger(__name__)
app = flask.Flask(__name__)


def send_slack_message(asset, score):
    likely_hood = 100.0 - score
    text = f'{likely_hood}% chance of unsafe content! Please review asset {asset.id}'
    try:
        SLACK_CLIENT.chat_postMessage(
          channel=SLACK_CHANNEL,
          text=text
        )
    except slack_sdk.SlackApiError as e:
        logger.warning(f'Error posting to slack {e}', e)


@app.route('/', methods=['POST'])
def webhook():

    try:
        # Validate the request is coming from BoonAI.
        validate_webhook_request_headers(flask.request.headers, WEBHOOK_SECRET)

        # Get the BoonAI asset from the request
        asset = boonsdk.Asset(flask.request.get_json()['asset'])

        # Get The "safe" label if one exists
        safe = asset.get_predicted_label('clarifai-unsafe-detection', 'safe')
        if safe and safe['score'] <= 0.6:
            send_slack_message(asset, safe['score'])

        return '', 200
    except Exception as e:
        logger.warning("Faied to process request ", e)
        return '', 400