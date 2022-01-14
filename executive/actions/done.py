from datetime import datetime
from sys import argv

from pytz import timezone

from executive.actions.models import Action, ScheduledAction

if __name__ == "__main__":
    options = argv[1:]
    if options[0] == "-s":
        action = ScheduledAction[options[1]]
        action.lastcompleted = datetime.now(timezone('Europe/Amsterdam'))
    else:
        action = Action[options[0]]
        action.completed = True
    action.save()
    print("Well done!")
    print("Set action '{action.name}' to completed.".format(**locals()))
    print("call decide.py for your next action")
