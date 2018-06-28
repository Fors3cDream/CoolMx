_author_ = "killer"
_date_ = "6/27/18 5:15 PM"


from random import Random

from users.models import EmailVerifyRecord
from django.core.mail import send_mail, EmailMessage
from CoolMx.settings import EMAIL_FROM
from django.template import loader  # 以html格式发送邮件

# 生成随机字符串
def random_str(random_length=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


# 发送注册邮件
def send_register_eamil(email, send_type="register"):
    # 发送之前先保存到数据库，到时候查询链接是否存在

    # 实例化一个EmailVerifyRecord对象
    email_record = EmailVerifyRecord()
    # 生成随机的code放入链接
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    # 定义邮件内容:
    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = " 注册激活链接"
        email_body = "欢迎注册:  请点击下面的链接激活你的账号: http://127.0.0.1:8081/active/{0}".format(code)

        # email_body = loader.render_to_string(
        #             "email_register.html",  # 需要渲染的html模板
        #             {
        # "active_code":code  # 参数
        # }
        # )

        # msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        # msg.content_subtype = "html"
        # send_status = msg.send()

        #使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email,])

        # 如果发送成功
        if send_status:
            return 1

    elif send_type == "forget":
        email_title = " 重置链接"
        email_body = "请点击下面的链接重置您的密码: http://127.0.0.1:8081/reset/{0}".format(code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email, ])

        # 如果发送成功
        if send_status:
            return 1