import json
import os
import sys
from Gemini_client import GeminiClient
import pandas as pd
from transcribe_prompt import transcribe, system_instruction_header, faq_template
import logging
from typing import List, Dict
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def read_csv_first_column(transcribe):
    """
    读取CSV文件的Keyword列内容
    Args:
        transcribe: 文件标识
    Returns:
        combined_list: 合并后的关键词列表
    """
    combined_list = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 检查暂停标志文件是否存在
    pause_flag_file = os.path.join(current_dir, 'pause_generation')
    if os.path.exists(pause_flag_file):
        logging.info("Found pause flag file. Generation paused.")
        return []
        
    csv_file = os.path.join(current_dir, "..", "Keyword_transcribe_combined.csv")
    
    try:
        df = pd.read_csv(csv_file)
        if not df.empty and "Keyword" in df.columns:
            # 获取所有非空的关键词
            keywords = df["Keyword"].dropna().tolist()
            combined_list = [str(value) for value in keywords]
            logging.info(f"Successfully read {len(combined_list)} keywords from CSV")
        else:
            logging.warning("CSV file is empty or missing 'Keyword' column")
    except Exception as e:
        logging.error(f"Error reading CSV file: {str(e)}")
    
    return combined_list

def setup_logging():
    """设置日志配置"""
    log_file = 'seo_generation.log'
    
    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.INFO)
    
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # 先清除所有的handler，防止重复
    logger.handlers.clear()
    
    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

def load_templates():
    """
    Load templates for content generation
    
    Returns:
        Dictionary containing templates for data format and product introduction
    """
    return {
        "dataformat_list": [
            "TranscribePageContent",
            "FAQ"
        ]
    }

def add_transcribe_content(responses_dict):
    """
    Add default transcribe page content structure to the responses dictionary.
    
    Args:
        responses_dict: Dictionary to add the default structure to
        
    Returns:
        Updated dictionary with default transcribe page structure
    """
    default_structure = {
        "title": "AI-Powered Transcription",
        "TranscribePageContent": {
            "title": "",
            "subtitle": "",
            "features": [
                {
                    "title": "",
                    "description": ""
                },
                {
                    "title": "",
                    "description": ""
                },
                {
                    "title": "",
                    "description": ""
                }
            ]
        },
        "FAQ": [
            {
                "question": "",
                "answer": ""
            }
        ]
    }
    
    responses_dict.update(default_structure)
    return responses_dict

def pause_after_iterations(iteration_count, pause_interval=4, pause_duration=60):
    """
    检查是否需要暂停
    
    Args:
        iteration_count: 当前迭代次数
        pause_interval: 每多少次迭代后暂停
        pause_duration: 暂停时长(秒)
    """
    if iteration_count > 0 and iteration_count % pause_interval == 0:
        logging.info(f"已处理{iteration_count}个关键词，暂停{pause_duration}秒...")
        time.sleep(pause_duration)
        
def validate_data_format(input_data: dict, format_config: dict) -> bool:
    """
    验证输入数据是否符合指定格式
    
    Args:
        input_data (dict): 需要验证的输入数据
        format_config (dict): 格式配置，指定每个key应该对应的数据类型
        
    Returns:
        bool: 验证是否通过
    """
    import logging
    
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # 检查所有必需的key是否存在
        for key, expected_type in format_config.items():
            if key not in input_data:
                logger.error(f"缺少必需的键: {key}")
                return False
            
            # 获取实际的值和类型
            actual_value = input_data[key]
            actual_type = type(actual_value)
            
            # 将字符串类型的类型名转换为实际的类型对象
            if isinstance(expected_type, str):
                expected_type = eval(expected_type)
            
            # 检查类型是否匹配
            if not isinstance(actual_value, expected_type):
                logger.error(f"键 '{key}' 的类型不匹配: 期望 {expected_type.__name__}, 实际 {actual_type.__name__}")
                return False
        
        logger.info("数据格式验证通过")
        print("数据格式检验没有问题")
        return True
        
    except Exception as e:
        logger.error(f"验证过程中发生错误: {str(e)}")
        return False

def process_faq_response(key_word, response_json):
    """处理FAQ响应，使用模板生成标准化的FAQ"""
    # 使用模板生成FAQ，将关键词替换到模板中
    formatted_faqs = []
    for template in faq_template:
        formatted_faq = {
            "question": template["question"].format(subject=key_word),
            "answer": template["answer"].format(subject=key_word)
        }
        formatted_faqs.append(formatted_faq)
    return formatted_faqs

def generate_seo_content(key_words_list: List[str]) -> List[Dict]:
    """生成SEO内容的主要逻辑"""
    templates = load_templates()
    all_results = []
    output_file = os.path.abspath("seo_content_results.json")
    logging.info(f"Will save results to: {output_file}")
    
    for idx, key_word in enumerate(key_words_list, 1):
        logging.info(f"Processing keyword: {key_word}")
        responses_dict = {}
        
        # 每处理4个关键词后暂停1分钟
        pause_after_iterations(idx)
        
        try:
            # 构建更具体的系统指令
            system_instruction = f"""
            You are an AI assistant specialized in generating SEO-optimized content for transcription services.
            Your task is to create engaging, informative content that highlights the benefits and features of our transcription service.
            
            IMPORTANT: You must return ONLY valid JSON data in the exact format specified below.
            Do not include any other text, explanations, or markdown formatting.
            The response must start with '{{' and end with '}}'.
            
            Required JSON Format:
            {{
                "title": "A compelling title that includes '{key_word}' and 'AskSia' (50-60 characters)",
                "subtitle": "An engaging subtitle that expands on the value proposition (100-120 characters)",
                "features": [
                    {{
                        "title": "Create a dynamic title combining speed/real-time with '{key_word}'",
                        "description": "A detailed description emphasizing speed and efficiency (150-200 characters)"
                    }},
                    {{
                        "title": "Create a title highlighting AI accuracy with '{key_word}'",
                        "description": "An explanation focusing on accuracy and reliability (150-200 characters)"
                    }},
                    {{
                        "title": "Create a title combining global reach with '{key_word}'",
                        "description": "Details about multilingual capabilities and worldwide access (150-200 characters)"
                    }}
                ]
            }}
            
            Title Creation Guidelines:
            1. Make each feature title unique and memorable
            2. Naturally incorporate '{key_word}' into the title
            3. Highlight the specific benefit (speed/accuracy/language)
            4. Keep titles concise and impactful
            5. Ensure professional tone
            
            Content Guidelines:
            1. Return a single, valid JSON object
            2. Fill all fields with meaningful content
            3. Use '{key_word}' naturally throughout
            4. Include 'AskSia' in relevant places
            5. Focus on user benefits
            6. Maintain consistent tone
            7. No need to highlight 'AI'
            
            IMPORTANT: Your response must be a valid JSON object. Do not include any text before or after the JSON.
            """
            
            messages = [{
                "role": "user",
                "parts": ["Generate SEO content in the exact JSON format specified. Return only the JSON object."]
            }]
            
            client = GeminiClient()
            print(f"Generating content for keyword: {key_word}\n")
            
            response = client.generate_with_history(
                history=messages,
                system_instruction=system_instruction
            )
            
            # 清理响应文本，确保它是有效的 JSON
            response = response.strip()
            if not response.startswith("{"):
                response = response[response.find("{"):]
            if not response.endswith("}"):
                response = response[:response.rfind("}") + 1]
            
            print(f"Cleaned response:\n{response}\n")
            
            try:
                response_json = json.loads(response)
                
                # 验证 JSON 结构
                if not isinstance(response_json, dict):
                    raise ValueError("Response must be a JSON object")
                
                required_fields = ["title", "subtitle", "features"]
                for field in required_fields:
                    if field not in response_json:
                        raise ValueError(f"Missing required field: {field}")
                
                if not isinstance(response_json["features"], list) or len(response_json["features"]) != 3:
                    raise ValueError("Features must be an array with exactly 3 items")
                
                for feature in response_json["features"]:
                    if not isinstance(feature, dict) or "title" not in feature or "description" not in feature:
                        raise ValueError("Each feature must have a title and description")
                
                responses_dict["TranscribePageContent"] = response_json
                print("Successfully validated JSON format")
                
                # 生成 FAQ
                faq_response = process_faq_response(key_word, faq_template)
                responses_dict["FAQ"] = faq_response
                
                # 只有在所有内容都成功生成时才添加到结果中
                all_results.append(responses_dict)
                
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format: {str(e)}")
            
        except Exception as e:
            error_msg = f"Error processing keyword {key_word}: {str(e)}"
            logging.error(error_msg)
            print(error_msg)
            continue
        
        # 保存中间结果
        try:
            if all_results:  # 只在有结果时保存
                logging.info(f"Writing results to file: {json.dumps(all_results, ensure_ascii=False)[:200]}...")
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(all_results, f, ensure_ascii=False, indent=2)
                logging.info(f"Successfully saved intermediate results to {output_file}")
            
        except Exception as e:
            logging.error(f"Error saving intermediate results to file: {str(e)}")
    
    return all_results



if __name__ == "__main__":
    setup_logging()
    
    try:
        key_words_list = read_csv_first_column("transcribe")[:]
        
        # 将关键词列表保存为JSON文件
        json_path = "keywords.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(key_words_list, f, ensure_ascii=False, indent=4)
        
        logging.info(f"Starting SEO content generation for {len(key_words_list)} keywords")
        results = generate_seo_content(key_words_list)
        logging.info("Content generation completed successfully")
            
    except Exception as e:
        logging.error(f"Program execution failed: {str(e)}")
