import requests

# 1. создание пользователя
json = {'username': 'user_1',
        'password': '12345',
        'mail': 'ss@ss'}
response = requests.post('http://127.0.0.1:5000/users', json=json)
print('1. Создание пользователя')
print(response.status_code)
print(response.text)

# 2. Некорректное создание объявления: не указан логин
json = {'caption': 'test 1',
        'description': 'Test description',
        }
response = requests.post('http://127.0.0.1:5000/adverts', json=json)
print('2. Некорректное создание объявления: не указан логин')
print(response.status_code)
print(response.text)

# 3. Некорректное создание объявления 2: указан пользователь, которого нет
json = {'caption': 'test 1',
        'description': 'Test description',
        'user': 'Vasya',
        'password': '1'
        }
response = requests.post('http://127.0.0.1:5000/adverts', json=json)
print('3. Некорректное создание объявления 2: указан пользователь, которого нет')
print(response.status_code)
print(response.text)

# 4. Некорректное создание объявления 3: указан пользователь и некорректный логин
json = {'caption': 'test 2',
        'description': 'Test description',
        'user': 'user_1',
        'password': '12'
        }
response = requests.post('http://127.0.0.1:5000/adverts', json=json)
print('4. Некорректное создание объявления 3: указан пользователь и некорректный логин')
print(response.status_code)
print(response.text)

# 5. Корректное создание объявления
json = {'caption': 'test 3',
        'description': 'Test description',
        'user': 'user_1',
        'password': '12345'
        }
response = requests.post('http://127.0.0.1:5000/adverts', json=json)
print('5. Корректное создание объявления')
print(response.status_code)
print(response.text)


# 6. Корректное изменение объявления
json = {'caption': 'test new',
        'description': 'Test description patch',
        'user': 'user_1',
        'password': '12345'
        }
response = requests.patch('http://127.0.0.1:5000/adverts/1', json=json)
print('6. Корректное изменение объявления')
print(response.status_code)
print(response.text)

# 7. Просмотр измененного объявления
response = requests.get('http://127.0.0.1:5000/adverts/1')
print('7. Просмотр измененного объявления')
print(response.status_code)
print(response.text)

# 8. Корректное удаление объявления
json = {'user': 'user_1',
        'password': '12345'
        }
response = requests.delete('http://127.0.0.1:5000/adverts/1', json=json)
print('8. Корректное удаление объявления')
print(response.status_code)
print(response.text)

# 9. Просмотр удаленного объявления
response = requests.get('http://127.0.0.1:5000/adverts/1')
print('9. Просмотр удаленного объявления')
print(response.status_code)
print(response.text)