from sys import argv
from executive.actions.models import Project
if __name__ == "__main__":
    arguments = argv[1:]
    p = Project(name = arguments[0])
    if len(arguments) == 2:
        p.parent = Project[arguments[1]]
    p.save()
    if p.parent:
        print("created subproject {p.id} with parent {p.parent.id}: {p.name}".format(**locals()))
    else:
        print("created project {p.id}: {p.name}".format(**locals()))
    p.save()
