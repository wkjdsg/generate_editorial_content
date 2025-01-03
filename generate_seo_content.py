import os
from dotenv import load_dotenv
import logging
import google.generativeai as genai
import extract_pdf_content
from google.api_core import retry
from typing import Optional
import json


# 在文件开头加载 .env 文件
load_dotenv()

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('seo_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

    
def course_seo_content(api_key: str, syllabus_text: str) -> Optional[str]:
    try:
        # 从环境变量获取API密钥
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("API key not found in environment variables")

        # Configure API
        genai.configure(api_key=api_key)
        logger.info("API configured successfully")

        # Create the model with config
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }
    

        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="Please extract the class information according to the json field, if not found, reply 'not mentioned in the syllabus'"
                )
            logger.info("AI model initialized successfully")

            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": ["""
I will provide you with a JSON dictionary. 
Please refer to the syllabus I give you and fill in the corresponding information. 
If no relevant information is found, please write "not mentioned in the syllabus" in the corresponding field. 
Below is the JSON return format:
```json
{
    "courseBasicInfo": {
      "courseTitle": "string",
      "school": "string,Three capital letters as the initials of the school",
      "courseCode": "string",
      "credits": "string",
      "semester": "string",
      "department": "string"
    },
    "instructorInfo": {
      "instructorName": "string",
      "titlePosition": "string",
      "officeAddress": "string",
      "officeHours": "string",
      "contactInfo": {
        "email": "string",
        "phone": "string"
      }
    },
    "assessmentAndGradingPolicy": {
      "weightings": {
        "assignments": "string",
        "quizzes": "string",
        "midterm": "string",
        "final": "string",
        "projects": "string",
        "attendance": "string"
      },
      "assessmentMethods": ["string"]
    }
  }
```
                                """                                   
                                  ]},
                    {
                        "role": "user",
                        "parts": [syllabus_text],
                    },
                ]
            )
            
            response = chat_session.send_message("INSERT_INPUT_HERE")
            logger.info("Successfully generated SEO content")
            return response.text

        except genai.types.generation_types.BlockedPromptException as e:
            logger.error(f"Content generation blocked: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error during content generation: {str(e)}")
            raise

    except Exception as e:
        logger.error(f"Unexpected error in generate_seo_content: {str(e)}")
        return None
 


def transcribe_seo_content(api_key: str, syllabus_text: str) -> Optional[str]:
    try:
        # 从环境变量获取API密钥
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("API key not found in environment variables")

        # Configure API
        genai.configure(api_key=api_key)
        logger.info("API configured successfully")

        # Create the model with config
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }

        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="You will receive a product introduction and a syllabus. In order to better help students in this class understand how this product can be utilized in the classroom. Output in JSON format.You should reference as much classroom information and details from the syllabus as possible to supplement the json.\n\nfill this json:\n{\n  title: what can you do using Asksia AI Transcribe for your course study?;\n  description: string in a sentence;\n  coreFeatures: string ,in bullted points, each point should be concise and just in a setence(you need to find detailed information from the syllabus and interpret it in conjunction with the product introduction. );\n} \n",
            )
            logger.info("AI model initialized successfully")

            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [
                            "product introduction:\nAsksia AI Transcribe: The Ultimate AI Assistant for International Students\n\nTransform your classroom experience with Asksia AI Transcribe, the cutting-edge AI tool designed specifically to support international students. This powerful platform effortlessly transcribes class recordings into your preferred language, ensuring you never miss a word.\n\nWith real-time language translation, comprehensive class outlines, and a smart AI classroom assistant, Asksia AI Transcribe makes it easy to stay on top of your lessons, even when language barriers stand in your way. Whether you're reviewing lecture content or seeking a deeper understanding of complex topics, our tool is here to help you seamlessly access class information and succeed in your studies.\n\nKey Features:\n\nMultilingual Transcription: Instantly transcribe class recordings into any language.\nClass Outlines: Get detailed outlines for each lecture, making review and study easier.\nAI Classroom Assistant: Your personal guide to understanding class material with AI-powered support.\nSeamless Learning: Enhance comprehension and stay on track with a smoother learning experience.\nUnlock the full potential of your education with Asksia AI Transcribe—your ultimate academic companion.",
                        ],
                    },
                    {
                        "role": "user",
                        "parts": [syllabus_text],
                    },
                ]
            )
            
            response = chat_session.send_message("INSERT_INPUT_HERE")
            logger.info("Successfully generated SEO content")
            return response.text

        except genai.types.generation_types.BlockedPromptException as e:
            logger.error(f"Content generation blocked: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error during content generation: {str(e)}")
            raise

    except Exception as e:
        logger.error(f"Unexpected error in generate_seo_content: {str(e)}")
        return None
    
def solver_seo_content(api_key: str, syllabus_text: str) -> Optional[str]:
    try:
        # 从环境变量获取API密钥
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("API key not found in environment variables")

        # Configure API
        genai.configure(api_key=api_key)
        logger.info("API configured successfully")

        # Create the model with config
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }

        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="""
You will receive a product introduction and a syllabus. Your task is to help students understand how this product can be used in the classroom based on the course content outlined in the syllabus. Output your response in JSON format. Make sure to reference relevant details from the syllabus to enrich your response.

Please complete the following JSON structure:

```json
{
  "title": "How Asksia AI Qsolver Can Enhance Your Course Study",
  "description": "A brief sentence description of how Asksia AI Qsolver can support students in the course, highlighting its relevance to the syllabus.",
  "coreFeatures": [
    {
      "name": "Explain Deeper",
      "description": "Concise sentence on how the product helps students understand complex concepts in depth, based on syllabus topics."
    },
    {
      "name": "Explain Easier",
      "description": "Concise sentence on how the product simplifies difficult concepts for easier comprehension in line with syllabus content."
    },
    {
      "name": "Check Answer",
      "description": "Concise sentence on how the product helps students verify their answers and understand where they may have gone wrong, linked to specific syllabus exercises or topics."
    },
    {
      "name": "Visualization",
      "description": "Concise sentence on how the product supports visual learning, such as through diagrams or graphs, aligned with syllabus topics."
    }
  ]
}
```

Each description should be:
- A single, concise sentence.
- Directly linked to relevant content from the syllabus and the product features.
"""
                )
            logger.info("AI model initialized successfully")

            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [syllabus_text],
                    },
                ]
            )
            
            response = chat_session.send_message("INSERT_INPUT_HERE")
            logger.info("Successfully generated SEO content")
            return response.text

        except genai.types.generation_types.BlockedPromptException as e:
            logger.error(f"Content generation blocked: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error during content generation: {str(e)}")
            raise

    except Exception as e:
        logger.error(f"Unexpected error in generate_seo_content: {str(e)}")
        return None
    
    
def reading_seo_content(api_key: str, syllabus_text: str) -> Optional[str]:
    try:
        # 从环境变量获取API密钥
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("API key not found in environment variables")

        # Configure API
        genai.configure(api_key=api_key)
        logger.info("API configured successfully")

        # Create the model with config
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }
    

        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="""
You will receive a product introduction and a syllabus. 
Your task is to explain how this product can be effectively used in the classroom based on the course content outlined in the syllabus. 
Output your response in JSON format. 
Ensure that you reference specific details from the syllabus to enhance the response.
Please fill out the following JSON structure:

```json
{
  "title": "How Asksia Reading Can Enhance Your Course Study",
  "description": "A brief overview of how Asksia Reading can support your course, based on the syllabus and product capabilities.",
  "coreFeatures": [
    {
      "name": "Multi-Document Support",
      "description": "A concise explanation of how this feature helps students work with multiple documents in relation to the course content, based on syllabus materials."
    },
    {
      "name": "Language Selection",
      "description": "A concise explanation of how this feature assists students in reading course materials in different languages, tied to relevant syllabus sections."
    },
    {
      "name": "Automated Summaries",
      "description": "A concise explanation of how this feature helps students understand key points from course readings by generating summaries, aligned with specific syllabus topics."
    },
    {
      "name": "Outline Recognition",
      "description": "A concise explanation of how this feature helps students navigate through the structure of course materials, highlighting the relevance to the syllabus."
    }
  ]
}
```

Each description should be:
- A concise sentence.
- Directly connected to specific details from the syllabus or product capabilities, enhancing the understanding of how the product can be used in the classroom.
"""    )
            logger.info("AI model initialized successfully")

            chat_session = model.start_chat(
                history=[   {
                        "role": "user",
                        "parts": [syllabus_text],
                    },
                ]
            )
            
            response = chat_session.send_message("INSERT_INPUT_HERE")
            logger.info("Successfully generated SEO content")
            return response.text

        except genai.types.generation_types.BlockedPromptException as e:
            logger.error(f"Content generation blocked: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error during content generation: {str(e)}")
            raise

    except Exception as e:
        logger.error(f"Unexpected error in generate_seo_content: {str(e)}")
        return None
 

def run_seo_generation_pipeline(syllabus_text: str) -> dict:
    """
    运行完整的SEO内容生成pipeline
    
    Args:
        syllabus_path: 教学大纲PDF文件的路径
        
    Returns:
        dict: 包含所有生成内容的字典
    """
    try:
        # 验证环境变量
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("请设置GEMINI_API_KEY环境变量")
            
        # 依次执行各个生成任务
        results = {}
        generation_tasks = {
            "CourseInfo": course_seo_content,
            "Qsolver": solver_seo_content,
            "Reading": reading_seo_content,  
            "transcribe": transcribe_seo_content
        }
#         export interface AllData {
#   courseInfo: CourseInfo;
#   qsolver: Qsolver;
#   reading: Reading;
#   transcribe: transcribe;
# }
        
        for task_name, task_func in generation_tasks.items():
            try:
                result = task_func(api_key, syllabus_text)
                results[task_name] = json.loads(result) if result else None
                logger.info(f"成功完成任务: {task_name}")
            except Exception as e:
                logger.error(f"任务 {task_name} 执行失败: {str(e)}")
                results[task_name] = None
                
        return results
        
    except Exception as e:
        logger.error(f"Pipeline执行失败: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # 读取文本文件
        syllabus_file_path = "test_syllabus_pdf/Syllabus-What is History-Fall 2023-Version 20230907.txt"
        with open(syllabus_file_path, 'r', encoding='utf-8') as file:
            syllabus_text = file.read()
        
        # 执行pipeline
        results = run_seo_generation_pipeline(syllabus_text)
        
        # 输出结果
        if results:
            print("生成的SEO内容：")
            print("\n```json")
            print(json.dumps(results, indent=2, ensure_ascii=False))
            print("```")
        else:
            print("生成SEO内容失败")
            
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
        print(f"执行过程中出现错误: {str(e)}")
    
    

    