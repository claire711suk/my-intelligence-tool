import feedparser
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai

# 配置 Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-3-flash-preview')

# RSS 源配置
RSS_FEEDS = {
    "科技/互联网": [
        "https://36kr.com/feed",
        "https://www.huxiu.com/rss/0.xml",
        "https://www.tmtpost.com/rss.xml"
        "https://www.huxiu/moment.com/rss.xml"
    ],
    "投资逻辑": [
        "https://xueqiu.com/hots/topic/rss"
    ],
    "全球热点": [
        "https://news.ycombinator.com/rss",
        "https://www.producthunt.com/feed"
    ]
}

def fetch_rss_content(url, limit=5):
    try:
        feed = feedparser.parse(url)
        entries = []
        for entry in feed.entries[:limit]:
            entries.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", entry.get("description", ""))
            })
        return entries
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def summarize_content(category, content_list):
    if not content_list:
        return "暂无更新内容。"
    
    prompt_base = f"你是一位精通全行业的资深分析师。请针对以下【{category}】类别的文章进行深度总结：\n\n"
    for item in content_list:
        prompt_base += f"- 标题: {item['title']}\n  链接: {item['link']}\n  内容摘要: {item['summary'][:300]}\n\n"
    
    if category == "科技/互联网":
        prompt_base += "要求：总结业务逻辑、市场变化、融资数据。请直接输出纯文本段落，不要使用 Markdown 符号（如 #, *, **），每个观点为一个自然段。"
    elif category == "投资逻辑":
        prompt_base += "要求：总结：热门投资行业具体热门公司或项目、分析其估值逻辑、护城护、风险提示。请直接输出纯文本段落，不要使用 Markdown 符号（如 #, *, **），每个观点为一个自然段。"
    else:  # 全球热点
        prompt_base += "要求：以‘趋势观察员’视角，分析为何火、本质创新、对个体的启发。请直接输出纯文本段落，不要使用 Markdown 符号（如 #, *, **），每个观点为一个自然段。"

    try:
        response = model.generate_content(prompt_base)
        return response.text
    except Exception as e:
        print(f"AI Summarization Error: {e}")
        return "AI 摘要生成失败。"

def clean_text(text):
    import re
    # 移除 Markdown 标题符号 (#)
    text = re.sub(r'#+\s*', '', text)
    # 移除加粗符号 (**)
    text = text.replace('**', '')
    # 移除列表符号 (*)
    text = re.sub(r'^\s*[\*\-]\s*', '', text, flags=re.MULTILINE)
    return text.strip()

def generate_html(summaries, articles_data):
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    
    sections_html = ""
    for category in ["科技/互联网", "投资逻辑", "全球热点"]:
        raw_summary = summaries.get(category, "暂无摘要")
        summary = clean_text(raw_summary)
        
        # 将文本按行分割，并包裹在带缩进的段落中
        paragraphs = summary.split('\n')
        formatted_summary = ""
        for p in paragraphs:
            if p.strip():
                formatted_summary += f'<p class="mb-3 text-justify" style="text-indent: 2em;">{p.strip()}</p>'

        articles = articles_data.get(category, [])
        links_html = ""
        if articles:
            links_html = '<div class="mt-6 pt-4 border-t border-gray-100"><h3 class="serif text-sm font-bold mb-2 text-gray-400 uppercase tracking-wider">深度阅读</h3><ul class="space-y-2">'
            for art in articles[:5]:
                links_html += f'<li><a href="{art["link"]}" target="_blank" class="text-xs text-emerald-600 hover:text-emerald-800 hover:underline flex items-center gap-1"><span>·</span> {art["title"]}</a></li>'
            links_html += '</ul></div>'

        sections_html += f"""
                <div class="card p-6 flex flex-col">
                    <div class="flex-grow">
                        <h2 class="serif text-xl font-bold mb-4">{category}</h2>
                        <div class="markdown-content text-sm leading-relaxed text-gray-600">
                            {formatted_summary}
                        </div>
                    </div>
                    {links_html}
                </div>
        """

    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>蒂蒂的智库 - {today}</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
        <style>
            body {{
                background-color: #F5F2ED;
                font-family: 'Inter', sans-serif;
                color: #333;
            }}
            .serif {{ font-family: 'Noto Serif SC', serif; }}
            .card {{
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.03);
                transition: transform 0.2s;
            }}
            .card:hover {{ transform: translateY(-2px); }}
            h2 {{ color: #5A5A40; border-bottom: 2px solid #5A5A40; padding-bottom: 8px; }}
            .markdown-content ul {{ list-style-type: disc; padding-left: 20px; }}
            .markdown-content li {{ margin-bottom: 8px; }}
        </style>
    </head>
    <body class="p-6 md:p-12">
        <div class="max-w-6xl mx-auto">
            <header class="mb-12 text-center">
                <h1 class="serif text-4xl font-bold mb-2">蒂蒂的智库</h1>
                <p class="text-gray-500 tracking-widest uppercase text-sm">{today}</p>
            </header>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {sections_html}
            </div>

            <footer class="mt-16 text-center text-gray-400 text-xs">
                <p>Generated by Didi's Intelligence Hub & Gemini 3 Flash</p>
            </footer>
        </div>
    </body>
    </html>
    """
    return html_template

def send_email(html_content):
    email_user = os.environ.get("EMAIL_USER")
    email_password = os.environ.get("EMAIL_PASSWORD")
    if not email_user or not email_password:
        print("Email credentials not set. Skipping email.")
        return

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_user  # 发送给自己
    msg['Subject'] = f"【每日智库】{datetime.datetime.now().strftime('%Y-%m-%d')}"
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email_user, email_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    summaries = {}
    articles_data = {}
    for category, urls in RSS_FEEDS.items():
        all_entries = []
        for url in urls:
            all_entries.extend(fetch_rss_content(url))
        
        articles_data[category] = all_entries
        print(f"Summarizing {category}...")
        summaries[category] = summarize_content(category, all_entries)
    
    html_content = generate_html(summaries, articles_data)
    
    # 保存为 index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # 发送邮件
    send_email(html_content)

if __name__ == "__main__":
    main()
