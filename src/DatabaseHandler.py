import sqlite3

from DemoDatabase import InitDB


class DatabaseHandler:
    def __init__(self):
        self.connection = sqlite3.connect("executive.db")
        # Setup default data for demo if database is empty
        InitDB(self.connection.cursor())

    def commit(self):
        self.connection.commit()

    def get_projects(self):
        return self.connection.cursor().execute("""SELECT * from projects""")

    def get_actions_of_project(self, project_id):
        return self.connection.cursor().execute("""SELECT * FROM actions WHERE project_id = ?""", project_id)

    def get_project_by_title(self, title):
        return self.connection.cursor().execute("""SELECT * FROM projects WHERE title = '?'""", title)

    def add_project(self, title):
        self.connection.cursor().execute("""INSERT INTO projects(title) SELECT '?'""", title)

    def remove_project(self, project_id):
        self.connection.cursor().execute("""DELETE FROM projects WHERE id = ?""", project_id)

    def add_action_to_project(self, action_title, deadline, project_ID):
        self.connection.cursor().execute("""INSERT INTO actions(action_title , deadline, completed, project_id) 
                                            VALUES  (?, ?, ?, ?)""", (action_title, deadline, 0, project_ID))
        return self.connection.cursor().execute(
            """SELECT id FROM actions WHERE action_title = ? AND deadline = ? AND project_id = ? """,
            (action_title, deadline, project_ID))

    def change_completion(self, new_value, action_id):
        self.connection.cursor().execute("""UPDATE actions SET completed = ? WHERE id= ?""", (new_value, action_id))
