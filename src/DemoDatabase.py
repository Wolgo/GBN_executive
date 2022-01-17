# This file is only meant to set up a database for the demo.

def InitDB(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS projects (
        id integer PRIMARY KEY,
        title text NOT NULL
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS actions (
        id integer PRIMARY KEY,
        action_title text NOT NULL,
        deadline text NOT NULL,
        completed integer NOT NULL,
        project_id integer NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    )""")

    cursor.execute("""INSERT INTO projects(id, title) 
                SELECT 0, 'Project Zeus' 
                WHERE NOT EXISTS(SELECT 1 FROM projects WHERE id = 0 AND title = 'Project Zeus');
    """)

    cursor.execute("""INSERT INTO projects(id, title) 
                SELECT 1, 'Project Ares' 
                WHERE NOT EXISTS(SELECT 1 FROM projects WHERE id = 1 AND title = 'Project Ares' );
    """)

    cursor.execute("""INSERT INTO actions(id, action_title , deadline, completed, project_id) 
                SELECT 0, 'A simple example action', '2025-12-03', 1, 0
                WHERE NOT EXISTS(SELECT 1 FROM actions WHERE id = 0);
    """)

    cursor.execute("""INSERT INTO actions(id, action_title , deadline, completed, project_id) 
                SELECT 1, 'A second action', '2027-12-03', 0, 0
                WHERE NOT EXISTS(SELECT 1 FROM actions WHERE id = 1);
    """)

    cursor.execute("""INSERT INTO actions(id, action_title , deadline, completed, project_id) 
                SELECT 2, 'Clean code', '2025-06-03', 0, 1
                WHERE NOT EXISTS(SELECT 1 FROM actions WHERE id = 2);
    """)

    cursor.execute("""INSERT INTO actions(id, action_title , deadline, completed, project_id) 
                SELECT 3, 'Expand functionality', '2025-12-05', 0, 1
                WHERE NOT EXISTS(SELECT 1 FROM actions WHERE id = 3);
    """)

    cursor.execute("""INSERT INTO actions(id, action_title , deadline, completed, project_id) 
                SELECT 4, 'Set requirements', '2025-12-03', 0, 1
                WHERE NOT EXISTS(SELECT 1 FROM actions WHERE id = 4);
    """)
