import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    bot_event = event
    command = bot_event['text']
    print command
    print(event)
    log.debug(event)
    return {
        'text': 'Your command: ' + bot_event['text']
    }