import re

import requests


class UstcCredential:
    def __init__(self, student_id, password) -> None:
        self.student_id = student_id
        self.password = password

    def login(self, session: requests.Session, origin, service, examination):
        result = session.get("https://passport.ustc.edu.cn/login?service=" + service)
        cas_lt = re.findall(r"name=\"CAS_LT\" value=\"(.+)\"", result.text)[0]
        # 获取登陆验证码, 这一行不能删除, 必须要获取验证码才可以登陆(即使后面可以绕过验证码)
        session.get(
            "https://passport.ustc.edu.cn/validatecode.jsp?type=login", stream=True
        )
        # showCode = '0' 绕过验证码
        data = {
            "model": "uplogin.jsp",
            "service": service,
            "warn": "",
            "showCode": "0",
            "username": self.student_id,
            "password": self.password,
            "button": "",
            "CAS_LT": cas_lt,
            "LT": "",
        }
        session.post("https://passport.ustc.edu.cn/login", data=data)
        # 判断是否登陆成功
        result = session.get(origin)
        if result.url != examination:
            raise Exception("USTC 统一身份认证登陆失败")
        return result
