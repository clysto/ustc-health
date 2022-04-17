import logging
import re

import requests
from bs4 import BeautifulSoup

from ustc_credential import UstcCredential


class HealthReporter:
    def __init__(self, credential: UstcCredential) -> None:
        self.credential = credential

    def report(self, health_info: dict):
        session = requests.Session()
        logging.info(f"使用学号和密码登陆")
        try:
            result = self.credential.login(
                session,
                "https://weixine.ustc.edu.cn/2020",
                "https://weixine.ustc.edu.cn/2020/caslogin",
                "https://weixine.ustc.edu.cn/2020/home",
            )
        except Exception as err:
            logging.error(err)
            return
        logging.info("登陆成功")

        token = re.findall(r"name=\"_token\" value=\"(.+)\"", result.text)[0]
        health_info["_token"] = token

        logging.info("开始上报健康信息")

        result = session.post(
            "http://weixine.ustc.edu.cn/2020/daliy_report",
            data=health_info,
            headers={
                "content-type": "application/x-www-form-urlencoded",
            },
        )
        # 判断是否成功
        soup = BeautifulSoup(result.text, "html.parser")
        msg = soup.select_one(".flash-message p").find(text=True).strip()
        match = re.findall(r"上报成功", msg)
        logging.info(msg)
        if len(match) == 0:
            return False
        else:
            return True
