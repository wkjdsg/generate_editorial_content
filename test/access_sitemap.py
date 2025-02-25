import requests
import re
from urllib.parse import urlparse
from datetime import datetime
import json

def fetch_sitemap():
    # 设置请求URL
    url = "https://www.asksia.ai/college-ai/sitemap.xml"
    print(f"开始访问网址: {url}")
    
    try:
        # 发送GET请求
        print("正在发送GET请求...")
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        
        print(f"请求成功! 状态码: {response.status_code}")
        print(f"响应头信息: \n{response.headers}")
        print("\n原始响应内容的前500个字符:")
        print(response.text[:500])
        print("-" * 50)
        
        # 使用正则表达式提取URL和日期
        print("\n开始解析数据...")
        pattern = r'<loc>(https://[^<]+)</loc>\s*<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>'
        matches = re.findall(pattern, response.text)
        print(f"共找到 {len(matches)} 个URL条目")
        print("-" * 50)
        
        # 创建更适合 Next.js 使用的数据结构
        results = {
            "pages": [],
            "metadata": {
                "totalCount": 0,
                "generatedAt": datetime.now().isoformat(),
                "domain": "www.asksia.ai"
            }
        }
        
        for index, (url, date) in enumerate(matches, 1):
            parsed_url = urlparse(url)
            path = parsed_url.path
            
            # 获取最后一个斜杠后的内容作为标题，并美化格式
            raw_title = path.split('/')[-1]
            # 将连字符替换为空格，并将首字母大写
            title = ' '.join(word.capitalize() for word in raw_title.split('-'))
            
            # 添加到结果列表
            results["pages"].append({
                "url": url,
                "path": path,  # 添加路径便于前端路由
                "title": title,
                "lastModified": date,
                "slug": raw_title  # 添加 slug 用于 URL 构建
            })
        
        # 更新总数
        results["metadata"]["totalCount"] = len(results["pages"])
        
        # 将结果保存为JSON文件
        with open('sitemap_data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("\nJSON数据已保存到 sitemap_data.json 文件中")
            
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        print(f"详细错误信息: {str(e)}")
    except Exception as e:
        print(f"处理数据时出错: {e}")
        print(f"错误类型: {type(e).__name__}")

if __name__ == "__main__":
    print("程序开始执行...")
    print("当前时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("-" * 50)
    
    fetch_sitemap()
    
    print("\n程序执行完成!")
