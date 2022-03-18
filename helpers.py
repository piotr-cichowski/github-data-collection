
def create_dict(sha, messages, committers, branch_id, exclude):
    if sha and messages and committers and branch_id:
        tab = []
        temp = []
        length = len(sha)
        for i in range(0, len(exclude)):
            temp.append(str(exclude[i]['sha']))
        if length == len(messages) and length == len(committers):
            for i in range(0, length):
                if sha[i] in temp:
                    continue
                else:
                    tab += [{'sha': sha[i],
                             'message': messages[i],
                             'committer': committers[i],
                             'branch_id': branch_id}]
        else:
            print('length of given lists must be equal')
            return
    else:
        print('not all attributes were given')
        return
    return tab


def validation(string):
    if " " in string or string[0].isdigit():
        return False
    else:
        return True
