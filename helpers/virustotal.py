import requests

API_KEY = '53fc8fcb34397a326376729f594ce29fae66a137ba312f6bf4854ec385dcd67b'

def upload_file(path):
    url = "https://www.virustotal.com/api/v3/files"

    files = { "file": (path, open(path, "rb")) }
    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
    }

    response = requests.post(url, files=files, headers=headers)

    return response.json()['data']['links']['self']

def get_info_file(path):

    url = upload_file(path)

    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
    }

    response = requests.get(url, headers=headers)
    return response.json()['data']['attributes']['results']

# def print_info(dictionary):
#     for name in dictionary:
#         print('Антивірус:', name)
#         print('Результат:', dictionary[name]['result'])
#         print('\n')

# result = get_info_file('text.txt')

# print_info(result)


