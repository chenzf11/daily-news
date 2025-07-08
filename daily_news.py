import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import schedule
import time
import re

# API配置
api_url = "https://tomcat-right-basically.ngrok-free.app/v1/chat-messages"
api_key = "app-xxxxxxx"

# 请求头
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

# 请求体
payload = {
    "inputs": {},
    "query": "生成今日早报",
    "response_mode": "streaming",  # 可改为blocking获取阻塞响应
    "user": "abc-123"
}

def get_final_answer():
    """
    发送请求并返回 workflow_finished 节点的 answer 内容。
    """
    last_workflow_finished = None
    try:
        response = requests.post(
            api_url,
            headers=headers,
            data=json.dumps(payload),
            timeout=100,
            stream=True
        )
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    text = line.decode('utf-8').strip()
                    if text.startswith("data:"):
                        data_str = text[5:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            data_json = json.loads(data_str)
                            # 记录最后一个 workflow_finished 事件
                            if data_json.get("event") == "workflow_finished":
                                last_workflow_finished = data_json
                        except Exception as e:
                            print(f"解析JSON失败: {e}，内容: {data_str}")
            # 返回 workflow_finished 节点的 answer 字段
            if last_workflow_finished:
                answer = last_workflow_finished.get("data", {}).get("outputs", {}).get("answer")
                return answer
            else:
                print("未检测到 workflow_finished 事件")
                return None
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"请求异常: {e}")
        return None

def markdown_to_html_with_groups(md_text):
    lines = md_text.splitlines()
    html = ""
    group = None
    news_idx = 1
    for line in lines:
        line = line.strip()
        # 检查分组标题
        if line.startswith('## '):
            group = line[2:].strip()
            html += f'<h3>{group}</h3>\n'
            news_idx = 1  # 每组内重新编号
        # 匹配 [标题](url)
        m = re.match(r'\d+\. \[(.*?)\]\((.*?)\)', line)
        if m:
            title, url = m.group(1), m.group(2)
            html += f'{news_idx}. <a href="{url}">{title}</a><br>\n'
            news_idx += 1
        # 也兼容无序号的 [标题](url)
        elif re.match(r'\[(.*?)\]\((.*?)\)', line):
            m2 = re.match(r'\[(.*?)\]\((.*?)\)', line)
            title, url = m2.group(1), m2.group(2)
            html += f'{news_idx}. <a href="{url}">{title}</a><br>\n'
            news_idx += 1
        # 其它内容直接转为段落
        elif line and not line.startswith('#'):
            html += f'<p>{line}</p>\n'
    return html

def send_news_email():
    # 邮件服务器配置
    smtp_server = 'smtp.163.com'
    smtp_port = 25
    sender_email = 'xxxxxxx@163.com'
    sender_password = 'xxxxxx'  # 授权码
    recipient_email = 'yyyyyyyyy@163.com'

    # 获取新闻内容
    news_content = get_final_answer()
    if not news_content:
        news_content = '未获取到今日早报内容。'
    else:
        news_content = markdown_to_html_with_groups(news_content)

    # 创建HTML邮件
    message = MIMEText(news_content, 'html', 'utf-8')
    message['From'] = Header('发件人 <{}>'.format(sender_email), 'utf-8')
    message['To'] = Header('收件人 <{}>'.format(recipient_email), 'utf-8')
    message['Subject'] = Header('今日早报', 'utf-8')

    try:
        smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        smtp_connection.login(sender_email, sender_password)
        smtp_connection.sendmail(sender_email, recipient_email, message.as_string())
        smtp_connection.quit()
        print("邮件发送成功！")
    except Exception as e:
        print("邮件发送失败：", e)

# 每天15:10执行一次
schedule.every().day.at("08:00").do(send_news_email)

if __name__ == "__main__":
    print("开始定时发送早报邮件，每天8:00发送一次。按 Ctrl+C 可随时终止。")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("已手动终止定时邮件服务。")



