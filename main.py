#!/usr/bin/python
from request import response
from helpers import validation
from db_connect import MongoDatabase
import getopt
import sys


argumentList = sys.argv[1:]
username = input("insert git username:\n")
repo_name = input("insert repository name: \n")
branch_name = input("insert branch name: \n")

# in case running this program with parameters given inline: uncomment below and comment above code

"""try:
    arguments, values = getopt.getopt(argumentList, "u:r:b:", ["username", "repository", "branch"])
except:
    print("error exiting ...")
    exit()
for currentArgument, currentValue in arguments:
    if currentArgument in ["-u", "--username"]:
        print("current_value = " + str(currentValue))
        username = currentValue
        print("username = "+str(username))
    if currentArgument in ["-r", "--repository"]:
        repo_name = currentValue
        print("repo_name = "+str(repo_name))
    if currentArgument in ["-b", "--branch"]:
        branch_name = currentValue
        print("branch_name = "+str(branch_name))"""


if validation(username) and validation(repo_name) and validation(branch_name):
    print("\nusername: " + username + " \n repo name: " + repo_name + " \n branch name:" + branch_name + " \n")

    request = response(username, repo_name, branch_name)

    if not request:
        exit()
    else:
        sha_tab = request[0]
        messages_tab = request[1]
        committers_tab = request[2]

        db = MongoDatabase()

        user_id = db.check_user_exist(username)
        repo_id = db.check_repo_exist(repo_name, user_id)
        branch_id = db.check_branch_exist(branch_name, repo_id)
        db.check_commits_exist(sha_tab, messages_tab, committers_tab, branch_id)
        db.close()
else:
    print("wrong inputs")
