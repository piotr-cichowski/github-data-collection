import request
from db_connect import database
from helpers import val

# data inserted by user
username = input("insert git username:\n")
repo_name = input("insert repository name: \n")
branch_name = input("insert branch name: \n")

# inputs validation
if val(username) and val(repo_name) and val(branch_name):
    print("\nusername: " + username + " \n repo name: " + repo_name + " \n branch name:" + branch_name + " \n")

    # creating request to GitHub REST-API
    r = request.response(username, repo_name, branch_name)
    # checking status of given request
    if not r:
        exit()
    else:
        # creating separate tabs with data from requests
        sha_tab = r[0]
        messages_tab = r[1]
        committers_tab = r[2]

        # creating db object for class database(creating connection with PostgreSQL database)
        db = database()

        # checking if inserted data(username, repository name and branch name) exist in database.
        # If false, repository will be added to table with unique ids.
        # if true, id of that data will be saved to variable for future inserting queries
        u_id = db.check_user_exist(username)
        rp_id = db.check_repo_exist(repo_name, u_id)
        br_id = db.check_branch_exist(branch_name, rp_id)

        # checking if all inserts was success and commit changes to database
        if db.check_commit_exist(sha_tab, messages_tab, committers_tab, u_id, br_id):
            db.commit()
            print("Data successfully inserted to database")
        else:
            print("error while inserting data to database\n data not inserted!")
        db.close()

else:
    print("wrong inputs")
