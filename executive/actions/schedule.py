from executive.actions.models import ScheduledAction
from executive.actions.add import AddAction

class ScheduleAction(AddAction):
    options = [
        'name', 'cron']
    def _add(self, options):
        action = ScheduledAction(**options) 
        action.save()

if __name__ == "__main__":
    ScheduleAction().run()














