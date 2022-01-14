import traceback
from sys import argv

from django.db import connection, transaction

if __name__ == "__main__":
    query = argv[1]
    with transaction.commit_manually():
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            if query.startswith("select"):
                rows = []
                for x in range(100):
                    row = cursor.fetchone()
                    if row:
                        rows.append(row)
                else:
                    for row in rows:
                        print(row)
            else:
                if query.startswith("delete"):
                    if "where" not in query:
                        confirm = input(
                            "Really delete everything?\nIf so, please write 'yes sir, delete everything.'\n>")
                        if confirm != "yes sir, delete everything.":
                            raise Exception("aborted")

            print("query affected {} rows".format(cursor.rowcount))
            connection.commit()
        except Exception as e:
            traceback.print_exc(e)
