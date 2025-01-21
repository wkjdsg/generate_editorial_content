import json
import pandas as pd
import os
from GeminiClient import GeminiClient
from tutor_prompt import course_info,product_using,product_reading,product_transcribe,faq,reading,solver,transcribe,system_instruction_header
import logging
from typing import List, Dict
from pathlib import Path


def read_csv_first_column(tutor):
    """
    读取指定专业相关的CSV文件并提取第一列内容
    Args:
        major_name: 专业名称
    Returns:
        combined_list: 合并后的第一列内容列表
    """
    combined_list = []
    csv_files = [
        f'{tutor}/major_name solver.csv',
        f'{tutor}/major_name tutor.csv',
        f'{tutor}/major_name_ai.csv'
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
        "product_intro_list": [solver, reading, transcribe, '']
    }

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
    
    for key_word in key_words_list:
        logging.info(f"Processing keyword: {key_word}")
        responses_dict = {}  # 创建一个字典来存储每个关键词的所有响应
        
        for system_body in system_body_list:
            try:
                messages = [{
                    "role": "user",
                    "parts": [f"your positioning is to help students as a {key_word}"]
                }]
                
                # 获取当前 system_body 字典的键和值
                current_key = list(system_body.keys())[0]
                current_value = system_body[current_key]
                system_instruction = system_instruction_header + current_value + '\nreturn in above json format:\n'
                client = GeminiClient()
                print(system_instruction+'\n\n==========')
                response = client.generate_with_history(
                    history=messages,
                    system_instruction=system_instruction
                )
                
                response_json = json.loads(response)
                responses_dict.update({current_key: response_json})  # 使用字典update方法直接添加键值对
                logging.info(f"Successfully generated content for {key_word}")
                
            except json.JSONDecodeError as e:
                logging.error(f"JSON parsing error for keyword {key_word}: {str(e)}")
                logging.debug(f"Raw response: {response}")
            except Exception as e:
                logging.error(f"Error processing keyword {key_word}: {str(e)}")
        
        if responses_dict:
            # 合并所有响应到一个字典中
            all_results.append(responses_dict)
        else:
            logging.warning(f"No valid content generated for keyword {key_word}")
    
    # 保存结果到JSON文件
    output_file = "seo_content_results.json"
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
        key_words_list = read_csv_first_column("tutor")[:3]
        logging.info(f"Starting SEO content generation for {len(key_words_list)} keywords")
        results = generate_seo_content(key_words_list)
        logging.info("Content generation completed successfully")
            
    except Exception as e:
        logging.error(f"Program execution failed: {str(e)}")


#读取
# tutor\[major_name] solver.csv
# tutor\[major_name] tutor.csv
# tutor\major_name_ai.csv
# 然后分别提取第一列的内容并用append的方式拼接成一个list
