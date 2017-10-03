import importlib

available_commands = ['Help', 'Query', 'Wiki']

def lambda_handler(event, context):
    bot_event = event
    command = bot_event['text'].title()

    if command in available_commands:
        command_class = getattr(importlib.import_module("src.commands"), command)
        commandInstance = command_class()
        response = commandInstance.execute()
    else:
        response = "Command %s does not exist" % command

    return {
        'text': response
    }