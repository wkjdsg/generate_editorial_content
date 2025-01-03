# 这是一个自动生成数据集的代码，控制了google gemini的PTM，以及生成数据集的样式。
# 通过执行该脚本，可以根据指定的json文件，生成不同学校、不同课程的pagedata json，并保存到对应的folder当中

import json
from generate_seo_content import run_seo_generation_pipeline
import os

def loop_syllabus_generate_seo_content(syllabus_list: list) -> dict:
    """
    遍历syllabus列表，为每个syllabus生成SEO内容
    
    Args:
        syllabus_list (list): 包含多个字典的列表，每个字典都有'syllabus'键
        
    Returns:
        dict: 合并后的SEO内容结果
    """
    results = {}
    
    for item in syllabus_list:
        if 'syllabus' in item:
            syllabus_text = item['syllabus']
            seo_result = run_seo_generation_pipeline(syllabus_text)
            results.update(seo_result)
    
    return results

def generate_tsx_file(input_dict: dict) -> None:
    """
    将输入字典转换为TSX文件，包含四个导出常量，并保存到对应的文件夹结构中
    
    Args:
        input_dict (dict): 包含CourseInfo、Qsolver、Reading、transcribe数据的字典
    """
    # 获取文件名所需的信息
    course_info = input_dict.get('CourseInfo', {})
    basic_info = course_info.get('courseBasicInfo', {})
    print(basic_info)
    
    # 构建文件名
    file_name = f"{basic_info.get('courseCode')}.tsx"
    
    # 构建TSX文件内容
    tsx_content = f"""import type {{ CourseInfo, Qsolver, Reading, transcribe }} from './types';

export const courseInfo: CourseInfo = {json.dumps(input_dict.get('CourseInfo', {}), indent=2)};

export const productUsingInCourse: Qsolver = {json.dumps(input_dict.get('Qsolver', {}), indent=2)};

export const productUsingInCoursereading: Reading = {json.dumps(input_dict.get('Reading', {}), indent=2)};

export const productUsingInCoursetranscribe: transcribe = {json.dumps(input_dict.get('transcribe', {}), indent=2)};
"""
    
    # 构建文件夹路径
    base_path = "seo_tool_pages_data"
    semester_path = os.path.join(base_path, basic_info.get('semester', ''))
    school_path = os.path.join(semester_path, basic_info.get('school', ''))
    
    # 创建必要的文件夹
    os.makedirs(school_path, exist_ok=True)
    
    # 写入文件到对应的文件夹
    file_path = os.path.join(school_path, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(tsx_content)

if __name__ == "__main__":
    # 从 JSON 文件读取测试数据
    with open('processed_placeholderdata.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # 使用第一个元素作为测试输入
    test_school_data = test_data[0]
    test_syllabus = run_seo_generation_pipeline(test_school_data['syllabus'])
    
    # 测试 generate_tsx_file 函数
    generate_tsx_file(test_syllabus)
    print("TSX 文件生成完成！")




