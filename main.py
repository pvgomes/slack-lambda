import importlib
import os

available_commands = ['Help', 'Query', 'Wiki']

def lambda_handler(event, context):
    bot_event = event
    commands = bot_event['text'].split(" ")
    command = commands[0].title()
    commands.pop(0)
    argument = ' '.join(commands)

    if command in available_commands:
        command_class = getattr(importlib.import_module("src.commands"), command)
        commandInstance = command_class()
        response = commandInstance.execute(argument)
    else:
        response = "Command %s does not exist" % command

    return {
        'text': response + "environment value for key database_user " + os.environ['database_user']
    }
