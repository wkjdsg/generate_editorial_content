import requests
import json
import logging
import time


def upload_data(url, title, prefix, content, action="create", max_retries=3):
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('upload_data.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    payload = json.dumps({
        "title": title,
        "prefix": prefix,
        "action": action,
        "content": content
    })
    
    # Log request information
    logger.info(f"Sending request to: {url}")
    logger.info(f"Title: {title}")
    logger.info(f"Prefix: {prefix}")
    logger.info(f"Action type: {action}")
    
    for attempt in range(max_retries):
        try:
            response = requests.request("POST", url=url, headers=headers, data=payload)
            response.raise_for_status()
            logger.info(f"Request successful! Status code: {response.status_code}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
            if attempt == max_retries - 1:
                logger.error(f"All retry attempts failed for title: {title}")
                return False
            logger.info(f"Retrying in 1 seconds...")
            time.sleep(1)

def load_data(keywords_path, contents_path):
    """加载关键词和内容数据"""
    with open(keywords_path, "r", encoding="utf-8") as file:
        keywords = json.load(file)
    with open(contents_path, "r", encoding="utf-8") as file:
        contents = json.load(file)
    return keywords, contents

def save_failed_data(failed_data, error_file="failed_uploads.json"):
    """保存失败的数据到文件"""
    if not failed_data:
        return
    
    try:
        with open(error_file, "w", encoding="utf-8") as f:
            json.dump(failed_data, f, ensure_ascii=False, indent=4)
        logging.info(f"Failed items have been saved to {error_file}")
    except Exception as e:
        logging.error(f"Error saving failed items to file: {str(e)}")

def process_uploads(url, prefix, keywords, contents):
    """处理上传任务"""
    failed_items = []
    failed_data = []
    
    for index, (content, keyword) in enumerate(zip(contents, keywords), 1):
        title = keyword
        logging.info(f"Processing item {index}/{len(keywords)}: {title}")
        try:
            success = upload_data(url, title, prefix, content, action="create")
            if not success:
                failed_items.append((index, title))
                failed_data.append({
                    "index": index,
                    "title": title,
                    "content": content
                })
                logging.error(f"Failed to upload item {index}: {title}")
        except Exception as e:
            failed_items.append((index, title))
            failed_data.append({
                "index": index,
                "title": title,
                "content": content
            })
            logging.error(f"Unexpected error processing item {index}: {title}")
            logging.exception(e)
    
    return failed_items, failed_data

def main0127():
    # Configure logging for main
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(r'good-grades\upload_data.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    url = "https://api.asksia.ai/page/action/?api-key=yXEgKvoc.HpvdgHgd7u7UVTCsIlVBybbdRKcF0RxP"
    prefix = "good-grades"
    
    # 加载数据
    keywords, contents = load_data(
        r"good-grades\generate_seo_data\keywords.json",
        r"good-grades\generate_seo_data\seo_content_results.json"
    )
    
    # 处理上传
    failed_items, failed_data = process_uploads(url, prefix, keywords, contents)
    
    # 保存失败数据
    save_failed_data(failed_data)
    
    # 输出结果
    if failed_items:
        logging.error(f"Upload completed with {len(failed_items)} failures:")
        for index, title in failed_items:
            logging.error(f"Failed item {index}: {title}")
    else:
        logging.info("All items uploaded successfully!")

if __name__ == "__main__":
    main0127()


