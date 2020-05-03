import requests

key = 'qFMbGz7tiBQkWzjMOUAgbQ'
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": "9781632168146"})
print(res.json())
