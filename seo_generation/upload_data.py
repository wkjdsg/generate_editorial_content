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
    print(f"Sending request to: {url}")
    logger.info(f"Title: {title}")
    print(f"Title: {title}")
    logger.info(f"Prefix: {prefix}")
    print(f"Prefix: {prefix}")
    logger.info(f"Action type: {action}")
    print(f"Action type: {action}")
    
    for attempt in range(max_retries):
        try:
            response = requests.request("POST", url=url, headers=headers, data=payload)
            response.raise_for_status()
            logger.info(f"Request successful! Status code: {response.status_code}")
            print(f"Request successful! Status code: {response.status_code}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
            print(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
            if attempt == max_retries - 1:
                logger.error(f"All retry attempts failed for title: {title}")
                print(f"All retry attempts failed for title: {title}")
                return False
            logger.info(f"Retrying in 1 seconds...")
            print(f"Retrying in 1 seconds...")
            time.sleep(1)

if __name__ == "__main__":
    # Configure logging for main
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('upload_data.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    url = "https://api.asksia.ai/page/action/?api-key=yXEgKvoc.HpvdgHgd7u7UVTCsIlVBybbdRKcF0RxP"
    prefix = "tutor"
    with open(r"tutor\generate_seo_data\keywords.json", "r",encoding="utf-8") as file:
        keywords = json.load(file)
    with open(r"tutor\generate_seo_data\seo_content_results.json", "r",encoding="utf-8") as file:
        contents = json.load(file)
    
    failed_items = []
    for index, (content, keyword) in enumerate(zip(contents, keywords), 1):
        title = keyword
        logger.info(f"Processing item {index}/{len(keywords)}: {title}")
        print(f"Processing item {index}/{len(keywords)}: {title}")
        try:
            success = upload_data(url, title, prefix, content, action="create")
            if not success:
                failed_items.append((index, title))
                logger.error(f"Failed to upload item {index}: {title}")
                print(f"Failed to upload item {index}: {title}")
        except Exception as e:
            failed_items.append((index, title))
            logger.error(f"Unexpected error processing item {index}: {title}")
            print(f"Unexpected error processing item {index}: {title}")
            logger.exception(e)
            print(f"Exception: {str(e)}")
        
    if failed_items:
        logger.error(f"Upload completed with {len(failed_items)} failures:")
        print(f"Upload completed with {len(failed_items)} failures:")
        for index, title in failed_items:
            logger.error(f"Failed item {index}: {title}")
            print(f"Failed item {index}: {title}")
    else:
        logger.info("All items uploaded successfully!")
        print("All items uploaded successfully!")


