import requests
import json

def upload_data(url,title,prefix,content,action = "create"):
    headers = {
        'Content-Type': 'application/json'
    }
    url = url
    payload = json.dumps(
        {
            "title": title,
            "prefix": prefix,
            "action": action,
            "content": content
        }
    )
    response = requests.request("POST", url=url, headers=headers, data=payload)
    print(response.text)

if __name__ == "__main__":
    url = "https://api.asksia.ai/page/action/?api-key=yXEgKvoc.HpvdgHgd7u7UVTCsIlVBybbdRKcF0RxP"
    prefix = "tutor"
    with open(r"tutor\seo_content_results.json", "r",encoding="utf-8") as file:
        content = json.load(file)
        content = content[0]
    with open(r"tutor\keywords.json", "r",encoding="utf-8") as file:
        keywords = json.load(file)
    title = keywords[0]
    upload_data(url,title,prefix,content,action = "create")
