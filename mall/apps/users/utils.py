# from mall import settings
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#
#
# def get_token(instance, email):
#     s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
#     data = {
#         'id': instance.id,
#         'email': email
#     }
#     token = s.dumps(data)
#     return token