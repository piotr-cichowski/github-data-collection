from helpers import create_dict
import pymongo


class MongoDatabase:
    def __init__(self):
        auth = {'user': 'rootuser',
                'pass': 'rootpass',
                'host': 'localhost',
                'port': '27017',
                'database': 'project'}
        self._conn = pymongo.MongoClient(("mongodb://" + auth['user'] + ":" + auth['pass'] + "@" + auth['host'] + ":" +
                                          auth['port']))
        self._db = self._conn[auth['database']]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('connection with mongodb closed')
        self._conn.close()

    def close(self):
        print("connection with database closed")
        self._conn.close()

    def get_conn(self):
        return self._conn

    def get_db(self):
        return self._db

    def choose_collection(self, collection):
        return self._db[collection]

    def check_user_exist(self, username):
        if username:
            response = self.choose_collection('user').find_one({'uname': username}, {'_id': 1})
            print("\n#################################\n")
            if response is None:
                user_id = self.insert_user(username)
                print("id of inserted user: " + str(user_id))
                return user_id
            else:
                print('user exist in database')
                print('id of this user: ' + str(response['_id']))
                return response['_id']
        else:
            print("error while checking if user exist in database")
            return False

    def insert_user(self, username):
        query = self.choose_collection('user').insert_one({'uname': username})
        return query.inserted_id

    def check_repo_exist(self, repo, user_id):
        if repo:
            response = self.choose_collection('repo').find_one({'rname': repo, 'user_id': user_id}, {'_id': 1})

            if response is None:
                repo_id = self.insert_repo(repo, user_id)
                print("id of inserted repo: " + str(repo_id))
                return repo_id
            else:
                print('repository exist in database')
                print('id of this repository: ' + str(response['_id']))
                return response['_id']
        else:
            print("error while checking if repository exist in database")
            return False

    def insert_repo(self, repo, user_id):
        query = self.choose_collection('repo').insert_one({'rname': repo, 'user_id': user_id})
        return query.inserted_id

    def check_branch_exist(self, branch, repo_id):
        if branch:
            response = self.choose_collection('branch').find_one({'bname': branch, 'repo_id': repo_id}, {'_id': 1})

            if response is None:
                branch_id = self.insert_branch(branch, repo_id)
                print("id of inserted branch: " + str(branch_id))
                return branch_id
            else:
                print('branch exist in database')
                print('id of this branch: ' + str(response['_id']))
                return response['_id']
        else:
            print("error while checking if branch exist in database")
            return False

    def insert_branch(self, branch, repo_id):
        query = self.choose_collection('branch').insert_one({'bname': branch, 'repo_id': repo_id})
        return query.inserted_id

    def check_commits_exist(self, sha, message, committer, branch_id):
        if sha:
            response = list(self.choose_collection('commit').find({'sha': {'$in': sha}}, {'sha': 1}))
            if len(response) == len(sha):
                print('\nall commits already in database')
            else:
                if response is None:
                    self.insert_commit(create_dict(sha, message, committer, branch_id, []))
                else:
                    self.insert_commit(create_dict(sha, message, committer, branch_id, response))
            return True
        else:
            print("error while checking if commit exist in database")
            return False

    def insert_commit(self, dict_mongo):
        print('data inserted to database')
        self.choose_collection('commit').insert_many(dict_mongo)
