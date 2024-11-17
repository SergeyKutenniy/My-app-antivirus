import requests

API_KEY = '53fc8fcb34397a326376729f594ce29fae66a137ba312f6bf4854ec385dcd67b'
URL = "https://www.virustotal.com/api/v3/files"

def upload_file(path):
    try:
        with open(path, "rb") as f:
            files = {"file": (path, f)}
            headers = {"accept": "application/json", "x-apikey": API_KEY}
            response = requests.post(URL, headers=headers, files=files)
        if response.status_code == 200:
            result = response.json().get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
            return f"Шкідливий: {result.get('harmless', 0)}, Зловмисний: {result.get('malicious', 0)}"
        else:
            return f"Помилка API: {response.status_code}"
    except Exception as e:
        return f"Упс, сталася помилка: {e}"


