from sys import argv
from executive.actions.models import Action, ScheduledAction
from datetime import datetime
from pytz import timezone

class CompleteAction(object):
    def run(self):
        options = argv[1:]
        if options[0] == "-s":
            action = ScheduledAction[options[1]]
            action.lastcompleted = datetime.now(timezone('Europe/Amsterdam'))
        else:
            action = Action[options[0]]
            action.completed = True
        action.save()
        self._reward(action)

    def _reward(self, action):
        print("Well done!")
        print("Set action '{action.name}' to completed.".format(**locals()))
        print("call decide.py for your next action")

if __name__ == "__main__":
    CompleteAction().run()
