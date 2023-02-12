import requests

url = "http://127.0.0.1:8000"


def get_access_token():
    r = requests.post(f'{url}/generate-token')
    return r.json()["access_token"]


def test_hello():
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    response = requests.post(f'{url}/hello', headers=headers)
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print("Request failed with status code:", response.status_code)


if __name__ == "__main__":
    test_hello()
