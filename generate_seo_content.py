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

def transcribe_seo_content(api_key: str, syllabus_path: str) -> Optional[str]:
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

        # 验证文件是否存在
        if not os.path.exists(syllabus_path):
            raise FileNotFoundError(f"Syllabus file not found at: {syllabus_path}")

        # Read syllabus content with error handling
        try:
            syllabus_text = extract_pdf_content.extract_pdf_text(syllabus_path)
            if not syllabus_text:
                raise ValueError("Extracted syllabus text is empty")
            logger.info("Successfully extracted syllabus content")
        except Exception as e:
            logger.error(f"Failed to extract PDF content: {str(e)}")
            raise

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
    
def solver_seo_content(api_key: str, syllabus_path: str) -> Optional[str]:
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

        # 验证文件是否存在
        if not os.path.exists(syllabus_path):
            raise FileNotFoundError(f"Syllabus file not found at: {syllabus_path}")

        # Read syllabus content with error handling
        try:
            syllabus_text = extract_pdf_content.extract_pdf_text(syllabus_path)
            if not syllabus_text:
                raise ValueError("Extracted syllabus text is empty")
            logger.info("Successfully extracted syllabus content")
        except Exception as e:
            logger.error(f"Failed to extract PDF content: {str(e)}")
            raise

        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="You will receive a product introduction and a syllabus. In order to better help students in this class understand how this product can be utilized in the classroom. Output in JSON format.You should reference as much classroom information and details from the syllabus as possible to supplement the json.\n\nfill this json:\n{\n  title: what can you do using Asksia AI Reading for your course study?;\n  description: string in a sentence;\n  coreFeatures: string ,in bullted points, each point should be concise and just in a setence(you need to find detailed information from the syllabus and interpret it in conjunction with the product introduction. );\n} \n",
            )
            logger.info("AI model initialized successfully")

            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": ["""**Unlock Your Learning Potential with Asksia AI Reading – The Ultimate Tool for International Students**

Welcome to **Asksia AI Reading**, your go-to AI-powered assistant designed to elevate your academic journey. Whether you're studying abroad or managing a heavy workload, our cutting-edge features will transform the way you read, understand, and analyze academic materials.

### Why Choose Asksia AI Reading?

- **Multi-Document Upload Support**: Say goodbye to tedious manual handling of documents. Upload multiple documents at once and let Asksia do the hard work for you, streamlining your reading experience and saving you valuable time.

- **Language Flexibility**: Study materials in different languages? No problem! Choose from a wide range of languages and read seamlessly without the language barriers.

- **Automatic Summarization**: Need to grasp the key points quickly? Asksia automatically summarizes your documents, highlighting the most important information so you can focus on what truly matters.

- **Article Structure Recognition**: Struggling to identify the core structure of lengthy texts? Our AI accurately detects the structure of any article, making it easier to navigate through complex academic papers and research articles.

### Boost Your Productivity & Focus on What Matters

Asksia AI Reading is not just an ordinary reading tool. It’s a powerful academic assistant tailored to meet the needs of international students. With enhanced reading support, you can now read smarter, not harder. Whether it's for research, class assignments, or exam preparation, let Asksia help you achieve your academic goals with ease.

**Experience the future of reading and learning today – try Asksia AI Reading and unlock your academic potential!**""" ]},
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
    
    
def solver_seo_content(api_key: str, syllabus_path: str) -> Optional[str]:
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

        # 验证文件是否存在
        if not os.path.exists(syllabus_path):
            raise FileNotFoundError(f"Syllabus file not found at: {syllabus_path}")

        # Read syllabus content with error handling
        try:
            syllabus_text = extract_pdf_content.extract_pdf_text(syllabus_path)
            if not syllabus_text:
                raise ValueError("Extracted syllabus text is empty")
            logger.info("Successfully extracted syllabus content")
        except Exception as e:
            logger.error(f"Failed to extract PDF content: {str(e)}")
            raise

        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="You will receive a product introduction and a syllabus. In order to better help students in this class understand how this product can be utilized in the classroom. Output in JSON format.You should reference as much classroom information and details from the syllabus as possible to supplement the json.\n\nfill this json:\n{\n  title: what can you do using Asksia AI Reading for your course study?;\n  description: string in a sentence;\n  coreFeatures: string ,in bullted points, each point should be concise and just in a setence(you need to find detailed information from the syllabus and interpret it in conjunction with the product introduction. );\n} \n",
            )
            logger.info("AI model initialized successfully")

            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": ["""
Introducing Asksia AI Solver – Your Ultimate AI Assistant for International Students!

Unlock two powerful response modes tailored to your needs:

- **Fast Mode**: Get lightning-fast, concise answers when you’re on the go. Perfect for quick insights and time-sensitive queries.
- **Thoughtful Mode**: Dive deeper with comprehensive, detailed explanations. While it may take a bit longer, you’ll enjoy enhanced accuracy and a richer understanding.

Whether you need to **explain complex concepts** with precision or **simplify ideas** for quick comprehension, Asksia AI Solver is your trusted partner. 

**Check answers** with confidence, **visualize** your learning journey, and elevate your academic experience to new heights!""" ]},
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
 

def run_seo_generation_pipeline(syllabus_path: str) -> dict:
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
            
        # 验证文件路径
        if not os.path.exists(syllabus_path):
            raise FileNotFoundError(f"未找到教学大纲文件: {syllabus_path}")
            
        # 依次执行各个生成任务
        results = {}
        generation_tasks = {
            "solver_seo_content": solver_seo_content,
            "reading_seo_content": solver_seo_content,  # 注意：这里可能需要改名
            "transcribe_seo_content": transcribe_seo_content
        }
        
        for task_name, task_func in generation_tasks.items():
            try:
                result = task_func(api_key, syllabus_path)
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
        # 设置文件路径
        syllabus_path = os.path.join("test_syllabus_pdf", "FRE GY6273ValuationTheorySpring2025Syllabus.pdf")
        
        # 执行pipeline
        results = run_seo_generation_pipeline(syllabus_path)
        
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
    

    