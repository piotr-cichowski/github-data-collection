import psycopg2
from helpers import inserted_data


class database:
    # initialisation of database class with connecting to psql and creating cursor
    def __init__(self):
        self._conn = psycopg2.connect(host="localhost",
                                      database="project",
                                      user="userapi",
                                      password="test123",
                                      port="5432")
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("connection with db closed")
        self.close()

    # connection getter
    def connection(self):
        return self._conn()

    # cursor getter
    def cursor(self):
        return self._cursor()

    # commit database
    def commit(self):
        self._conn.commit()

    # closing connection with database
    def close(self):
        if self.commit:
            self.commit()
        self._conn.close()

    # executing sql query without getting results
    def execute(self, sql, params=None):
        self._cursor.execute(sql, params or ())

    # method to get all results from cursor
    def fetchall(self):
        return self._cursor.fetchall()

    # method to get one result from cursor
    def fetchone(self):
        return self._cursor.fetchone()

    # method to
    def query(self, sql, params=None):
        self._cursor.execute(sql, params or ())
        x = self._cursor.fetchall()
        return x

    # method to check if given user exist in database
    def check_user_exist(self, username):
        if username:
            self._cursor.execute('SELECT id '
                                 'FROM users '
                                 'WHERE user_name LIKE %(str)s ;',
                                 {'str': username})
            response = self.fetchone()

            if response is None:
                u_id = self.insert_user(username)
                print("\nuser_id: " + str(u_id))
            else:
                print("\nusername: " + username + " exist in database")
                u_id = response[0]
                print("id of this user: " + str(u_id))
            return u_id
        else:
            print("error while checking if user exist in database")
            return

    # method to check if given repository exist in database
    def check_repo_exist(self, repo, user_id):
        if repo and user_id:
            self._cursor.execute("SELECT repos.id "
                                 "FROM repos "
                                 "INNER JOIN users ON repos.user_id = users.id "
                                 "WHERE repos.repository_name LIKE %(str)s AND users.id = %(int)s ;",
                                 {'str': repo, 'int': user_id})
            response = self.fetchone()

            if response is None:
                rp_id = self.insert_repo(repo, user_id)
                print("repo_id: " + str(rp_id))
            else:
                print("repository: " + repo + " of given user exist in database")
                rp_id = response[0]
                print("id of this repository: " + str(rp_id))
            return rp_id
        else:
            print("error while checking if repository exist in database")
            return

    # method to check if given branch exist in database
    def check_branch_exist(self, branch, repo_id):
        if branch and repo_id:
            self._cursor.execute("SELECT branches.id "
                                 "FROM branches "
                                 "INNER JOIN repos ON branches.repo_id = repos.id "
                                 "WHERE branches.branch_name LIKE %(str)s "
                                 "AND repos.id = %(int)s;",
                                 {'str': branch, 'int': repo_id})
            response = self.fetchone()
            if response is None:
                br_id = self.insert_branch(branch, repo_id)
                print("branch_id: " + str(br_id))
            else:
                print("branch: " + branch + " of given repository exist in database")
                br_id = response[0]
                print("id of this branch: " + str(br_id))
            return br_id
        else:
            print("error while checking if branch exist in database")
            return

    # method to check if given commits exist in database
    def check_commit_exist(self, sha, messages, committers, u_id, br_id):
        if sha:
            self._cursor.execute("SELECT sha "
                                 "FROM commits "
                                 "WHERE sha IN %(str)s ;",
                                 {'str': tuple(sha)})
            response = self.fetchall()
            rows = self._cursor.rowcount
            if rows == len(sha):
                print("\nall commits already in database")
            else:
                if response is None:
                    self.insert_commit(inserted_data(sha, messages, committers, u_id, br_id, []))
                else:
                    self.insert_commit(inserted_data(sha, messages, committers, u_id, br_id, response))
            return True
        else:
            print("error while checking if commit exist in database")
            return False

    # inserting user to database
    def insert_user(self, user):
        self._cursor.execute("INSERT INTO users (user_name) "
                             "VALUES (%(str)s) "
                             "RETURNING id;",
                             {'str': user})
        r = self._cursor.fetchone()[0]
        return r

    # inserting repository to database
    def insert_repo(self, repo, user_id):
        self._cursor.execute("INSERT INTO repos (repository_name, user_id) "
                             "VALUES (%(str)s, %(int)s) "
                             "RETURNING id;",
                             {'str': repo, 'int': user_id})
        r = self._cursor.fetchone()[0]
        return r

    # inserting branch to database
    def insert_branch(self, branch, repo_id):
        self._cursor.execute("INSERT INTO branches (branch_name, repo_id) "
                             "VALUES (%(str)s, %(int)s) "
                             "RETURNING id;",
                             {'str': branch, 'int': repo_id})
        r = self._cursor.fetchone()[0]
        return r

    # inserting commits to database
    def insert_commit(self, tab):
        args = ','.join(self._cursor.mogrify("(%s, %s, %s, %s, %s)", i).decode('utf-8')
                        for i in tab)
        self._cursor.execute("INSERT INTO commits (sha, message, user_id, branch_id, committer) "
                             "VALUES " + args)
