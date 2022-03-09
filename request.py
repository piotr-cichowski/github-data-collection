import requests


# function to get response from GitHub rest-api
# function returns three different data tabs (sha_tab, message_tab, committer_tab) from request response converted to json
def response(username, repo, branch):
    requests.ConnectionError()
    sha_tab = []
    message_tab = []
    committer_tab = []
    request_link = "https://api.github.com/repos/" + username + "/" + repo + "/commits?sha=" + branch + "&per_page=50"
    print("link " + request_link)

    r = requests.get(request_link)
    print("status code " + str(r.status_code))

    if str(r.status_code) == '200':
        print("status: ok")
        anw = r.json()
        for lis in anw:
            sha = lis['sha']
            sha_tab.append(sha)
            message = lis['commit']['message']
            message_tab.append(message)
            committer = lis['commit']['committer']['name']
            committer_tab.append(committer)
            print(repo + "/" + branch + "/" + sha + ": " + message + " " + committer)
        return sha_tab, message_tab, committer_tab
    elif str(r.status_code) == '404':
        print("not found data in GitHub rest-api")
        return False
