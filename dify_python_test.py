
def main() -> dict:
    import requests

    url = "https://api.vvhan.com/api/hotlist/pengPai"

    def extract_last_segment(url):
        if not url:
            return None
        return url.rstrip('/').split('/')[-1]
    name = extract_last_segment(url)

    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # 取前十条新闻
    news_list = data.get("data", [])[:10]
    # hot_news只保留title和url
    title_list = []
    for item in news_list:
        title_list.append(item.get("title"))

    url_list = []
    for item in news_list:
        url_list.append(item.get("url"))
        
    result = {
        'name': name,
        'title_list': title_list,
        'url_list': url_list
    }
    return result
   
