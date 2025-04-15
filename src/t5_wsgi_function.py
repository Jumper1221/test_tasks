import requests


def application(environ, start_response):
    if environ.get("REQUEST_METHOD", "GET").upper() != "GET":
        start_response("405 Method Not Allowed", [("Content-Type", "text/plain")])
        return [b"Only GET method is allowed"]

    path = environ.get("PATH_INFO", "").strip("/")
    if len(path) != 3 and not path.isalpha():
        start_response("400 Bad Request", [("Content-Type", "text/plain")])
        return [b"Only 3-character currencies"]
    currency = path.upper()

    api_url = f"https://api.exchangerate-api.com/v4/latest/{currency}"

    try:
        response = requests.get(api_url)
    except requests.RequestException:
        start_response("502 Bad Gateway", [("Content-Type", "text/plain")])
        return [b"Can't connect to exchange server"]

    headers = [("Content-Type", "application/json")]
    start_response(f"{response.status_code} {response.reason}", headers)
    return [response.content]


# waitress-serve --port=8000 t5_wsgi_function:application
