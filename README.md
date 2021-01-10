# zfjbot-pcrjjc-backend

backend server for hoshino bot plugin pcrjjc(https://github.com/lulu666lulu/pcrjjc)

## 说明

涉及一些敏感操作，拒绝回答任何问题，自行看代码领悟
（我都是copy大佬的，我也不懂

## 使用

抓包获取自己的登录信息，以及`headers`，修改`run.py`

``` python
# run.py
# headers部分一大片自己改

# 大概95行修改
viewer_id=xxxxxxxxxxxxx
uid="xxxxxxxxxxxxxx"
access_key="xxxxxxxxxxxxxxxxxxxxxxx"
```

## 双击使用

默认api

``` url
htttp://127.0.0.1:9025/api/pcrjjc/get_profile?target_viewer_id={要查询的id}
```

个人使用demo

<http://pcr.zfjdhj.cn/api/pcrjjc/get_profile?target_viewer_id={要查询的id}>

## 感谢

部分代码参考
<https://github.com/infinityedge01/qqbot2>
<https://github.com/lulu666lulu/pcrjjc>
