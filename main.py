from core.schemas.user import UserDBSchema


user = UserDBSchema(
    email='vasyapupkin@gmail.com',
    username='username',
    password='Qwerty1234!',
    hashed_password='$2b$12$36c9mXCL8bs6KwwPkMh58O4GOHRiqWdtVgffoE5/wdecnd3qZhv8a'
)
print(user.hashed_password)
#
# user = UserDBSchema(
#     email='vasyapupkin@gmail.com',
#     username='username',
#     password='Qwerty1234!'
# )
# print(user.hashed_password)
#
# user = UserDBSchema(
#     email='vasyapupkin@gmail.com',
#     username='username',
#     password='Qwerty1234!'
# )
# print(user.hashed_password)