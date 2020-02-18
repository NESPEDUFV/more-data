import json, re

path_user_json_input = '../../data/dados_profile/user_profile_17092019.json'
path_user_json_output = './json/user_profile_17092019.json'

def read_json_file(path):
    stopchar = """\\"""
    with open(path, "r") as f:
        str = "[" + f.read()
        str = str.replace(stopchar, "")
        str = str.replace('''"{''', '{')
        str = str.replace('''}"''', '}')
        str = str.replace('''"[''', '[')
        str = str.replace(''']"''', ']')
        str = str.replace('''""''', '''"''')
        str = str.replace(''':",''', ''':"",''')
        str = str.replace("\n", ",\n")
        str = str + "]"
        return json.loads(json.dumps(str))


def write_json_file(path_input, path_output):
    with open(path_output, 'w') as outfile:
        outfile.write(read_json_file(path_input))

if __name__ == "__main__":
    write_json_file(path_user_json_input, path_user_json_output)
