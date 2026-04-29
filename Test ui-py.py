import hashlib
pasword = '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b'

print(len(pasword))

def hash_password(pas):
    return hashlib.sha256(pas.encode()).hexdigest()

# print(hash_password(input('Введите пароль ')))

if hash_password(input('Введите пороль ')) == pasword:
    print('wellcome')
else:
    print('password no true')