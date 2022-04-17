# USTC 自动健康上报

> **本脚本仅供学习交流使用，请勿过分依赖。开发者对使用或不使用本脚本造成的问题不负任何责任，不对脚本执行效果做出任何担保，原则上不提供任何形式的技术支持。**

## 本地运行测试

首先下载脚本:

```sh
git clone https://github.com/clysto/ustc-health
cd ustc-health
```

创建一个 `config.ini` 配置文件:

```ini
[credential]
# 学号
student_id=
# 密码
password=

[health]
# 居住地
juzhudi=
# 宿舍楼
dorm_building=二栋
# 宿舍号
dorm=511
body_condition=1
body_condition_detail= 
# 1: 正常在校园内
# 2: 正常在家
# 3: 居家留观
# 4: 集中留观
# 5: 住院治疗
# 6: 其他
now_status=1
now_status_detail=
has_fever=0
last_touch_sars=0
last_touch_sars_date=
last_touch_sars_detail=
is_danger=0
is_goto_danger=0
# 紧急联系人
jinji_lxr=
# 紧急联系人关系
jinji_guanxi=
# 紧急联系人电话
jiji_mobile=
other_detail=
```

运行脚本:

```sh
./run.py
2022-04-17 19:04:47,808  INFO      读取配置文件 config.ini
2022-04-17 19:04:47,809  INFO      使用学号和密码登陆
2022-04-17 19:04:49,395  INFO      登陆成功
2022-04-17 19:04:49,396  INFO      开始上报健康信息
2022-04-17 19:04:49,901  INFO      上报成功，最近一次上报是32分钟36秒 之前，请每日按时打卡
```

## GitHub Actions 自动打卡

结合 GitHub Actions 实现每日自动打卡。

首先点击页面上的 **Use this template** 按钮创建自己的仓库。然后编写一个 workflow 配置文件(.github/workflows/report.yml):

> 可以直接在 GitHub 界面中创建，点击 **Add file** 按钮，输入新建文件的路径即可。

```yml
name: Auto Report

on: 
  push:
    branches:
      - main
  schedule:
    - cron: '0 10,21 * * *'

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run script
      env:
        CONFIG: ${{ secrets.config }}
      run: |
        echo "$CONFIG" > ./config.ini
        python3 run.py
```

上面的配置文件中 `cron` 为 `'0 10,21 * * *'`，即北京时间（东八区） 18:00 和 5:00 执行脚本，可以根据自己的需要更改时间。同时配置文件中使用 Github Secrets 来生成配置文件**避免你的个人信息泄漏**。

> 这里是生成配置文件的部分，`CONFIG` 就是 Github Secrets 中设置的 `CONFIG` 变量。
>
> ```sh
> echo "$CONFIG" > ./config.ini
> python3 run.py
> ```

**你需要在 Github Secrets (Settings / Secrets / Actions / New repository secret) 中设置 `CONFIG` 变量，它的值就是 `config.ini` 中的内容。**

以上步骤之后，将代码 push 到 GitHub，在 Actions 设置 (Settings / Actions / Allow all actions and reusable workflows) 中允许运行即可。
