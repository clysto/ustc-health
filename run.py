#!/usr/bin/env python3

import argparse
import configparser
import logging

from health_reporter import HealthReporter
from ustc_credential import UstcCredential

FORMAT = "%(asctime)s  %(levelname)-8s  %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

def parse_config(config_file):
     # 读取配置文件
    logging.info(f"读取配置文件 {config_file}")
    config = configparser.ConfigParser()
    config.read(config_file)
    if "credential" not in config:
        raise Exception("配置文件缺少 credential 部分")
    if "health" not in config:
        raise Exception("配置文件缺少 health 部分")
    if "student_id" not in config["credential"]:
        raise Exception("配置文件缺少 student_id")
    if "password" not in config["credential"]:
        raise Exception("配置文件缺少 password")
    return config


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='USTC 健康自动上报')
    parser.add_argument("--config", help="配置文件路径", default="config.ini")
    args = parser.parse_args()

    # 解析配置文件
    try:
        config = parse_config(args.config)
    except Exception as err:
        logging.error(err)
        exit(-1)

    # 读取学号和密码
    student_id = config["credential"]["student_id"]
    password = config["credential"]["password"]

    credential = UstcCredential(student_id, password)
    reporter = HealthReporter(credential)

    # 读取上报信息
    health_info = dict(config["health"])
    # 信息上报
    if reporter.report(health_info):
        exit(0)
    else:
        exit(-1)
