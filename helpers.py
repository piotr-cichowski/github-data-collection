
# preparing data tab for dynamic insert commits query
def inserted_data(sha, messages, committers, user_id, branch_id, exclude):
    if sha and messages and committers and user_id and branch_id:
        length = len(sha)
        tab = []
        temp = []
        for i in range(0, len(exclude)):
            temp.append(exclude[i][0])
        if length == len(messages) and length == len(committers):
            for i in range(0, length):
                if sha[i] in temp:
                    continue
                else:
                    tab.append((sha[i], messages[i], user_id, branch_id, committers[i]))
        else:
            print("length of given lists must be equal")
            return
    else:
        print('not all attributes were given')
        return
    return tab


# validation of user inputs
def val(string):
    if " " in string or string[0].isdigit():
        return False
    else:
        return True
