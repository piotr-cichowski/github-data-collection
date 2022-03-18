import requests


def response(username, repo, branch):
    requests.ConnectionError()
    sha_tab = []
    message_tab = []
    committer_tab = []
    request_link = "https://api.github.com/repos/" + username + "/" + repo + "/commits?sha=" + branch + "&per_page=20"
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
            print(repo + "/" + branch + "/" + sha + ": " + message.replace('\n', ' ') + " " + committer)
        return sha_tab, message_tab, committer_tab

    elif str(r.status_code) == '404':
        print("not found data in GitHub rest-api")
        return False
    elif str(r.status_code) == '400':
        print("BAD REQUEST")
    elif str(r.status_code) == '401':
        print("Unauthorized acces")
    elif str(r.status_code) == '403':
        print("FORBIDDEN")
    elif str(r.status_code) == '406':
        print("NOT ACCEPTABLE")
    elif str(r.status_code) == '410':
        print("GONE")
    elif str(r.status_code) == '429':
        print("Too many requests")
    elif str(r.status_code) == '500':
        print("Internal server error")
    elif str(r.status_code) == '502':
        print("BAD GATEWAY")
    elif str(r.status_code) == '503':
        print("service unavailable")
    elif str(r.status_code) == '504':
        print("GATEWAY TIMEOUT")
    else:
        print("something goes wrong")
