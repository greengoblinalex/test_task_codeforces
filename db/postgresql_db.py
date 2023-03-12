import random
from collections import OrderedDict

import psycopg2

from .constants import MAX_ID_COUNT_IN_CONTESTS


class Database:
    def __init__(self, host, user, password, db_name, port):
        self.con = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        self.cur = self.con.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
        id SERIAL PRIMARY KEY,
        themes TEXT,
        amount_of_decided TEXT,
        name_and_number TEXT,
        complexity TEXT
        )""")

        self.cur.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_name LIKE 'contest%';")
        self.contest_count = self.cur.fetchone()[0]

        self.cur.execute("SELECT COUNT(*) FROM tasks",
                         (self.contest_count,))
        self.task_id_count = self.cur.fetchone()[0]

        self.cur.execute(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'contest%s')", (self.contest_count,))
        if self.cur.fetchone()[0] is False:
            self.create_new_contest()

        self.con.commit()

    def create_new_contest(self):
        self.contest_count += 1
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS contest%s(
        id SERIAL PRIMARY KEY,
        tasks_id INTEGER REFERENCES tasks(id)
        )""", (self.contest_count,))

    def add_row(self, themes, amount_of_decided, name_and_number, complexity):
        self.cur.execute("""
            SELECT name_and_number
            FROM tasks
            WHERE name_and_number=%s
            """, (name_and_number,))

        if self.cur.fetchone() is None:
            self.cur.execute("""
                INSERT INTO tasks(themes, amount_of_decided, name_and_number, complexity)
                VALUES(%s, %s, %s, %s);
                """, (themes, amount_of_decided, name_and_number, complexity))
            self.task_id_count += 1

            self.cur.execute("SELECT COUNT(*) FROM contest%s",
                             (self.contest_count,))
            if self.cur.fetchone()[0] >= MAX_ID_COUNT_IN_CONTESTS:
                self.create_new_contest()

            self.cur.execute("""
                INSERT INTO contest%s(tasks_id)
                VALUES(%s);
                """, (self.contest_count, self.task_id_count))
            self.con.commit()

    def get_random_records(self, complexity, theme):
        self.cur.execute("""
        SELECT *
        FROM tasks
        WHERE complexity=%s AND themes LIKE %s
        LIMIT 10;
        """, (complexity, theme))

        results = self.cur.fetchall()
        new_results = []
        for result in results:
            new_results.append(list(result[1:]))

        return new_results
    
    # def get_random_contest_records(self, complexity, theme):
    #     random_contest = random.randint(1, self.contest_count)
    #     self.cur.execute("""
    #     SELECT *
    #     FROM contest%s
    #     JOIN tasks ON contest%s.tasks_id = tasks.id 
    #     WHERE tasks.complexity=%s AND themes LIKE %s
    #     LIMIT 10;
    #     """, (random_contest, random_contest, complexity, theme))

    #     results = self.cur.fetchall()
    #     new_results = []
    #     for result in results:
    #         new_results.append(list(result[3:]))

    #     return new_results

    def get_all_themes(self):
        self.cur.execute("""
        SELECT string_agg(themes, ',')
        FROM tasks;
        """)
        result = self.cur.fetchone()[0].split(',')
        result = list(OrderedDict.fromkeys(result))
        result.sort()
        return result
    
    def get_all_complexity(self):
        self.cur.execute("""
        SELECT string_agg(complexity, ',')
        FROM tasks;
        """)
        result = self.cur.fetchone()[0].split(',')
        result = list(OrderedDict.fromkeys(result))
        result.remove('')
        result = [int(i) for i in result]
        result.sort()
        return result

    def close_connection(self):
        self.cur.close()
        self.con.close()
