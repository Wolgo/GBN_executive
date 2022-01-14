from executive.actions.add import AddAction
from executive.actions.models import ScheduledAction


class ScheduleAction(AddAction):
    options = [
        'name', 'cron']

    def _add(self, options):
        action = ScheduledAction(**options)
        action.save()


if __name__ == "__main__":
    ScheduleAction().run()
