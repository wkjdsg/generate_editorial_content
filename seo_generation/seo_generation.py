import json
import pandas as pd
import os
from GeminiClient import GeminiClient
from seo_generation.example_tutor_prompt import course_info,product_using,product_reading,product_transcribe,faq,reading,solver,transcribe,system_instruction_header
import logging
from typing import List, Dict
from pathlib import Path
import time


def read_csv_first_column():
    """
    读取指定专业相关的CSV文件并提取第一列内容
    Args:
        major_name: 专业名称
    Returns:
        combined_list: 合并后的第一列内容列表
    """
    combined_list = []
    csv_files = [
        'tutor/data/major_name solver.csv',
        'tutor/data/major_name tutor.csv',
        'tutor/data/major_name_ai.csv'
    ]
    
    for file_path in csv_files:
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                if not df.empty and len(df.columns) > 0:
                    # 提取第一列内容并添加到combined_list
                    combined_list.extend(df.iloc[:, 0].tolist())
            except Exception as e:
                print(f"读取文件 {file_path} 时出错: {str(e)}")
    
    return combined_list

#首先读取csv文件，并获得第一列的内容并且拼接成一个list，
#在

def setup_logging():
    """配置日志记录"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('seo_generation.log'),
            logging.StreamHandler()
        ]
    )

def load_templates() -> Dict[str, List[str]]:
    """从配置文件加载模板"""
    # 这里可以改成从实际的配置文件加载
    return {
        "dataformat_list": [
            f"{product_using}",
            f"{product_reading}",
            f"{product_transcribe}",
            f"{faq}"
        ],
        "product_intro_list": [solver, reading, transcribe, solver+reading+transcribe+'return just a list of dictionaries,each dictionary has a question and answer']
    }

def add_dict(responses_dict,add_dict = None):
    default_course_structure = {
        "courseInfo": {
            "courseBasicInfo": {
                "courseTitle": " ",
                "school": " ",
                "courseCode": " ",
                "credits": " ",
                "semester": " ",
                "department": " "
            },
            "instructorInfo": {
                "instructorName": " ",
                "titlePosition": " ",
                "officeAddress": " ",
                "officeHours": " ",
                "contactInfo": {
                    "email": " ",
                    "phone": " "
                }
            },
            "assessmentAndGradingPolicy": {
                "weightings": {
                    "assignments": " ",
                    "quizzes": " ",
                    "midterm": " ",
                    "final": " ",
                    "projects": " ",
                    "attendance": " "
                },
                "assessmentMethods": [" ", " "]
            }
        }
    }
    if add_dict is not None:
        responses_dict.update(add_dict)
    else:
        responses_dict.update(default_course_structure)
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
        logging.info(f"Processed {iteration_count} keywords, pausing for {pause_duration} seconds...")
        print(f"Processed {iteration_count} keywords, pausing for {pause_duration} seconds...")
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
                logger.error(f"Missing required key: {key}")
                return False
            
            # 获取实际的值和类型
            actual_value = input_data[key]
            actual_type = type(actual_value)
            
            # 将字符串类型的类型名转换为实际的类型对象
            if isinstance(expected_type, str):
                expected_type = eval(expected_type)
            
            # 检查类型是否匹配
            if not isinstance(actual_value, expected_type):
                logger.error(f"Type mismatch for key '{key}': expected {expected_type.__name__}, got {actual_type.__name__}")
                print(f"Type mismatch for key '{key}': expected {expected_type.__name__}, got {actual_type.__name__}")
                return False
        
        logger.info("Data format validation passed")
        print("Data format validation successful")
        return True
        
    except Exception as e:
        logger.error(f"Error during validation: {str(e)}")
        print(f"Error during validation: {str(e)}")
        return False

def generate_seo_content(key_words_list: List[str]) -> List[Dict]:
    """生成SEO内容的主要逻辑"""
    templates = load_templates()
    system_body_keylist = ["productUsingInCourse","productUsingInCoursereading","productUsingInCoursetranscribe","FAQ"]
    system_body_list = [
        {key: dataformat + intro}
        for key, (dataformat, intro) in zip(
            system_body_keylist,
            zip(templates["dataformat_list"], templates["product_intro_list"])
        )
    ]
    
    all_results = []
    
    for idx, key_word in enumerate(key_words_list, 1):
        logging.info(f"Processing keyword: {key_word}")
        responses_dict = {}  # 创建一个字典来存储每个关键词的所有响应
        
        # 每处理4个关键词后暂停1分钟
        pause_after_iterations(idx)
        
        for system_body in system_body_list:
            try:
                messages = [{
                    "role": "user",
                    "parts": [f"your positioning is to help students as a {key_word}"]
                }]
                
                # 获取当前 system_body 字典的键和值
                current_key = list(system_body.keys())[0]
                current_value = system_body[current_key]
                system_instruction = system_instruction_header + current_value + '\nreturn in above json format strictly\n'
                client = GeminiClient()
                print(system_instruction+'\n\n==========')
                MAX_RETRIES = 3  # 最大重试次数
                retry_count = 0
                
                while retry_count < MAX_RETRIES:
                    try:
                        response = client.generate_with_history(
                            history=messages,
                            system_instruction=system_instruction
                        )
                        
                        response_json = json.loads(response)
                        
                        # 定义格式配置
                        format_configs = {
                            "productUsingInCourse": dict,
                            "productUsingInCoursereading": dict,
                            "productUsingInCoursetranscribe": dict,
                            "FAQ": list
                        }
                        
                        # 检查当前响应是否符合格式要求
                        if current_key in format_configs and not isinstance(response_json, format_configs[current_key]):
                            error_msg = f"Format validation failed: {current_key} should be {format_configs[current_key].__name__} type, retry {retry_count + 1}"
                            logging.warning(error_msg)
                            print(error_msg)
                            retry_count += 1
                            continue
                        
                        # 验证通过，更新字典并跳出循环
                        success_msg = f"Successfully processed {current_key} for keyword {key_word}"
                        logging.info(success_msg)
                        print(success_msg)
                        responses_dict.update({current_key: response_json})
                        responses_dict = add_dict(responses_dict)
                        break
                        
                    except Exception as e:
                        error_msg = f"Processing failed: {str(e)}, retry {retry_count + 1}"
                        logging.error(error_msg)
                        print(error_msg)
                        retry_count += 1
                
                if retry_count >= MAX_RETRIES:
                    error_msg = f"Reached maximum retry attempts {MAX_RETRIES}, skipping {current_key} processing for keyword {key_word}"
                    logging.error(error_msg)
                    print(error_msg)
                    continue
                
            except json.JSONDecodeError as e:
                logging.error(f"JSON parsing error for keyword {key_word}: {str(e)}")
                print(f"JSON parsing error for keyword {key_word}: {str(e)}")
                logging.debug(f"Raw response: {response}")
                print(f"Raw response: {response}")
            except Exception as e:
                logging.error(f"Error processing keyword {key_word}: {str(e)}")
                print(f"Error processing keyword {key_word}: {str(e)}")
        
        if responses_dict:
            # 合并所有响应到一个字典中
            all_results.append(responses_dict)
        else:
            logging.warning(f"No valid content generated for keyword {key_word}")
            print(f"No valid content generated for keyword {key_word}")

    # 保存结果到JSON文件
    output_file = r"tutor\generate_seo_data\seo_content_results.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        logging.info(f"Results saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving results to file: {str(e)}")
    
    return all_results



if __name__ == "__main__":
    setup_logging()
    
    try:
        key_words_list = read_csv_first_column()
        
        # 将关键词列表保存为JSON文件
        json_path = "tutor/generate_seo_data/keywords.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(key_words_list, f, ensure_ascii=False, indent=4)
        
        logging.info(f"Starting SEO content generation for {len(key_words_list)} keywords")
        print(f"Starting SEO content generation for {len(key_words_list)} keywords")
        results = generate_seo_content(key_words_list)
        logging.info("Content generation completed successfully")
        print("Content generation completed successfully")
            
    except Exception as e:
        logging.error(f"Program execution failed: {str(e)}")


#读取
# tutor\[major_name] solver.csv
# tutor\[major_name] tutor.csv
# tutor\major_name_ai.csv
# 然后分别提取第一列的内容并用append的方式拼接成一个list
