from datetime import datetime

from requests import get, post, put, delete

print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/6').json())
print(get('http://localhost:5000/api/v2/users/999999').json())
print(get('http://localhost:5000/api/v2/users/q').json())
print(get('http://localhost:5000/api/v2/users/').json())

print(delete('http://localhost:5000/api/v2/users/2').json())
print(delete('http://localhost:5000/api/v2/users/999').json())
print(delete('http://localhost:5000/api/v2/users/q').json())
print(delete('http://localhost:5000/api/v2/users/').json())

print(post('http://localhost:5000/api/v2/users', json={}).json())
print(post('http://localhost:5000/api/v2/users',
           json={'id': 1}).json())
print(post('http://localhost:5000/api/v2/users',
           json={'id': 'int_must'}).json())
print(post('http://localhost:5000/api/v2/users',
           json={
               'surname': 'Petrov',
               'name': 'Petr',
               'email': f'petr_{datetime.now().timestamp()}@example.com',
               'age': 28,
               'address': 'm',
               'position': 'Engineer',
               'speciality': 'Mechanical'
           }).json())
