# daily-news
### 调用多个主流社媒的api获取资讯，在dify搭建智能体，Python调用dify的api，生成日报每日推送邮箱

## 主流社媒的api
可以从https://api.vvhan.com/    里面挑选实时资讯api，在dify的代码节点进行调用。代码节点代码示例如dify_python_test.py，需要严格注意输出格式。

## 工作流搭建
可直接导入daily news assistant.yml
![image](https://github.com/user-attachments/assets/22e865da-d4cd-4ba8-a8e2-e5db9a4b6655)

## 每日推送到邮箱
需要开启dify的后端服务api，在daily_news.py中修改apikey以及发送和接收邮箱，163邮箱需要开启SMTP服务并记录授权码。
授权码的获取可以参考https://zhuanlan.zhihu.com/p/622514194



