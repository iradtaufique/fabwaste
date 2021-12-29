import requests

headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1hbnVmMUBnbWFpbC5jb20iLCJmdWxsX25hbWUiOiJtYW51ZmFjdHVyZTEiLCJpZCI6OH0.r8P7esy3NLp1z-ru0ENxCuB3jG0VzF7HVTXvWJg8Uec'}

r = requests.get('http://localhost:8000/api/textile-products-api/')

print(r.text)
