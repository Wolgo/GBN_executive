"""The script of greatness!"""

from datetime import datetime, date

import pytz

from executive.actions.models import Action, ScheduledAction, Project
from executive.tools.cron import CronHandler


def run():
    action = maintenance_action() or timed_action() or next_action()
    printout(action)
    return action


def empty_project():
    for p in Project.select():
        if len(Action.select().where(Action.project == p.id, Action.completed == False)) == 0:
            if len(Project.select().where(Project.parent == p.id)) == 0:
                return p
    return None


def maintenance_action():
    EmptyProject = empty_project()
    if len(Project.select()) == 0:
        return new_project_action()
    elif EmptyProject:
        return fill_project_action(EmptyProject)


def new_project_action():
    return new(
        "Add a first project using 'ex addproject (name) [parent id]'",
        date.today())


def fill_project_action(project):
    lastcompletednotice = ""
    lastdone = Action.select().filter(Action.project_id == project.id, Action.completed == True).order_by(
        Action.deadline.desc())
    if lastdone:
        lastcompletednotice += "\nlast completed action: {lastdone[0].name} at {lastdone[0].deadline}".format(
            **locals())
    return new(
        "Add an action to project {project.id}: {project.name}".format(**locals()) + lastcompletednotice,
        date.today(),
        project=project
    )


def timed_action():
    actions = ScheduledAction.select()
    for action in actions:
        cron = CronHandler(action.cron)
        lastenabled = cron.lastenabled()
        if not lastenabled:
            return None
        else:
            action.timeenabled = datetime(lastenabled.year,
                                          lastenabled.month,
                                          lastenabled.day,
                                          lastenabled.hour,
                                          lastenabled.minute)
        if action.lastcompleted:
            lastcompleted = action.lastcompleted.astimezone(pytz.timezone('Europe/Amsterdam'))
        else:
            return action
        if lastcompleted < lastenabled:
            return action


def next_action():
    actions = Action.select().where(Action.completed == False)
    nextaction = actions[0]
    for a in actions:
        if a.deadline < nextaction.deadline:
            nextaction = a
    return nextaction


def new(name, deadline, project=None):
    nextaction = Action(
        name=name,
        deadline=deadline,
        project=project)
    nextaction.save()
    return nextaction


def upcoming():
    """What timed action is next up?"""
    actions = ScheduledAction.select()
    _nexttimes = []
    for a in actions:
        _next = CronHandler(a.cron).nextenabled()
        if _next:
            _nexttimes.append((_next, a))
    if _nexttimes:
        return list(sorted(_nexttimes))[0]  # return the first time for action along with the action


def printout(action):
    _class = action.__class__
    if _class == ScheduledAction:
        print("[{action.id}]: {action.timeenabled}: {action.name}".format(**locals()))
    else:
        Upcoming = upcoming()
        if upcoming:
            print("Next scheduled action: {upcoming[1].name} at {upcoming[0]}".format(**locals()))

    if _class == Action:
        if action.project_id:
            project_str = get_parents(Project[action.project_id])
        else:
            project_str = ""
        print("{project_str} \n {action.id}: {action.deadline}: {action.name}".format(**locals()))


def get_parents(project):
    if not hasattr(project, 'parent_id') or not project.parent_id:
        return "> " + project.name
    else:
        parent = Project[project.parent_id]
        return get_parents(parent) + "\n> " + project.name


if __name__ == "__main__":
    run()
