import urllib.parse


def constructFormData(data):
    filtered_data = {k: v for k, v in data.items() if v is not None}
    encoded_data = [
        f"{k}={urllib.parse.quote(str(v), safe='()')}" for k, v in filtered_data.items()
    ]
    form_data = "&".join(encoded_data)
    return form_data
