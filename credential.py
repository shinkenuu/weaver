import json
import os


def get_credential(owner: str, subject: str):
    def get_crendentials():
        with open(os.path.join(os.path.expanduser('~'), 'credentials.json'), 'r') as file:
            json_content = json.load(file)
        return [registry['credentials'] for registry in json_content if registry['owner'] == owner][0]

    return [cred for cred in get_crendentials() if cred['subject'] == subject][0]
