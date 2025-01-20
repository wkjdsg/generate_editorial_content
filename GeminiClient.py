import os
from dotenv import load_dotenv
import logging
import google.generativeai as genai
from google.api_core import retry
from typing import Optional, Dict, Any, List
import json

    
class GeminiClient:
    """Gemini API 客户端封装类
    
    处理与 Gemini API 相关的所有操作，包括初始化、配置和API调用。
    
    Attributes:
        MODEL_CONFIGS: 预定义的模型配置字典
        DEFAULT_MODEL: 默认使用的模型名称
    """
    
    MODEL_CONFIGS = {
        "standard_response_json": {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        },
        "standard_response_text": {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        },
        "creative": {
            "temperature": 1.0,
            "top_p": 0.99,
            "top_k": 50,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }
    }
    
    DEFAULT_MODEL = "gemini-1.5-flash"
    
    def __init__(self, 
                 model_name: str = None, 
                 config_preset: str = "standard_response_json",
                 custom_config: Dict[str, Any] = None):
        """初始化 Gemini 客户端
        
        Args:
            model_name: 可选，模型名称
            config_preset: 可选，预设配置名称 ("standard" 或 "creative")
            custom_config: 可选，自定义配置，会覆盖预设配置
        """
        self.model_name = model_name or self.DEFAULT_MODEL
        
        # 获取预设配置
        if config_preset not in self.MODEL_CONFIGS:
            raise ValueError(f"Invalid config_preset: {config_preset}. Available presets: {list(self.MODEL_CONFIGS.keys())}")
        
        self.generation_config = self.MODEL_CONFIGS[config_preset].copy()
        
        # 如果有自定义配置，更新配置
        if custom_config:
            self.generation_config.update(custom_config)
            
        self.model = None
        self.logger = logging.getLogger(__name__)
        self._initialize_api()
        
    def _get_api_key(self) -> str:
        """获取 API 密钥
        
        Returns:
            str: API 密钥
            
        Raises:
            ValueError: 当环境变量中未找到 API 密钥时
        """
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("API key not found in environment variables")
        return api_key
        
    def _initialize_api(self) -> None:
        """初始化 Gemini API 和模型"""
        try:
            load_dotenv()
            api_key = self._get_api_key()
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config
            )
            self.logger.info("Gemini API and model initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini API: {str(e)}")
            raise

    def generate_content(self, input_text: str, system_instruction: str = None) -> Optional[str]:
        """生成内容
        
        Args:
            input_text: 输入文本
            system_instruction: 可选，系统指令，用于设置模型的行为
            
        Returns:
            Optional[str]: 生成的内容，如果发生错误则返回 None
            
        Raises:
            genai.types.generation_types.BlockedPromptException: 当内容被阻止时
            Exception: 其他可能的错误
        """
        try:
            model_params = {
                "model_name": self.model_name,
                "generation_config": self.generation_config
            }
            
            if system_instruction:
                model_params["system_instruction"] = system_instruction
                
            model = genai.GenerativeModel(**model_params)
            
            chat_session = model.start_chat(
                history=[
                ]
            )
            
            response = chat_session.send_message(input_text)
            self.logger.info("Successfully generated content")
            return response.text
            
        except genai.types.generation_types.BlockedPromptException as e:
            self.logger.error(f"Content generation blocked: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error during content generation: {str(e)}")
            raise

    def generate_with_history(self, history: List[Dict[str, Any]], system_instruction: str = None) -> Optional[str]:
        """使用历史对话记录生成内容
        
        Args:
            history: 对话历史记录列表，每个记录包含 role 和 parts
                格式: [{"role": "user"/"model", "parts": ["消息内容"]}]
            system_instruction: 可选，系统指令，用于设置模型的行为
            
        Returns:
            Optional[str]: 生成的内容，如果发生错误则返回 None
            
        Raises:
            genai.types.generation_types.BlockedPromptException: 当内容被阻止时
            ValueError: 当历史记录格式不正确时
            Exception: 其他可能的错误
        """
        try:
            # 验证历史记录格式
            if not isinstance(history, list):
                raise ValueError("History must be a list of messages")
            
            for msg in history:
                if not isinstance(msg, dict) or "role" not in msg or "parts" not in msg:
                    raise ValueError("Invalid message format in history")
                
            model_params = {
                "model_name": self.model_name,
                "generation_config": self.generation_config
            }
            
            if system_instruction:
                model_params["system_instruction"] = system_instruction
                
            model = genai.GenerativeModel(**model_params)
            
            # 创建聊天会话并添加历史记录
            chat_session = model.start_chat(history=history)
            
            # 获取最后一条消息的响应
            last_message = history[-1]["parts"][0]
            response = chat_session.send_message(last_message)
            
            self.logger.info("Successfully generated content with history")
            return response.text
            
        except genai.types.generation_types.BlockedPromptException as e:
            self.logger.error(f"Content generation blocked: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error during content generation: {str(e)}")
            raise

if __name__ == "__main__":
    # 创建 GeminiClient 实例
    client = GeminiClient()
    
    # 准备对话历史记录
    conversation_history = [
        {
            "role": "user",
            "parts": ["你好，我想学习Python编程"]
        },
        {
            "role": "model",
            "parts": ["很高兴听到你想学习Python！Python是一个非常适合初学者的编程语言。我可以帮你从基础开始。你之前有任何编程经验吗？"]
        },
        {
            "role": "user",
            "parts": ["我完全是个新手，请给我一些学习建议"]
        }
    ]
    
    try:
        # 设置系统指令（可选）
        system_instruction = "你是一个专业的Python编程教师，用简单易懂的方式回答问题"
        
        # 使用历史记录生成回复
        response = client.generate_with_history(
            history=conversation_history,
            system_instruction=system_instruction
        )
        
        print("AI回复：")
        print(response)
        
    except Exception as e:
        print(f"发生错误：{str(e)}")


