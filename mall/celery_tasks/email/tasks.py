# from django.core.mail import send_mail
# from celery_tasks.main import app
# # from mall import settings
# #
# #
# # def get_token(instance, email):
# #     from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# #     s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
# #     data = {
# #         'id': instance.id,
# #         'email': email
# #     }
# #     token = s.dumps(data)
# #     return token
# from users.utils import get_token
#
# @app.task(name='send_ative_email')
# def send_ative_email(instance,email):
#     token =get_token(instance, email)
#
#     subject = '美多商场激活邮件'
#     # message,          内容
#     message = ''
#     # from_email,       谁发送的
#     # 谁发送的
#     from_email = 'qi_rui_hua@163.com'
#     # recipient_list    收件人列表
#     recipient_list = ['836903920@qq.com']
#     verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=%s' % token.decode()
#     html_message = '<p>尊敬的用户您好！</p>' \
#                    '<p>感谢您使用美多商城。</p>' \
#                    '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
#                    '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
#
#     send_mail(subject, message, from_email, recipient_list, html_message=html_message)