# 自动填写 PAFD

## 对验证码识别的修改

说明：本次修改使用了[图鉴](http://ttshitu.com/)的付费API，你需要自己注册你的账号。在原来的基础上，你还需要设置CODE_ID:图鉴的账号，CODE_PSW:图鉴的密码这两个环境变量。

#### 运行：
```
nohup python3 -u script.py > script.log 2>&1 &
