import os
from dotenv import load_dotenv
import logging
import google.generativeai as genai
from google.api_core import retry
from typing import Optional, Dict, Any, List
import json

# 加载环境变量
load_dotenv()

class GeminiClient:
    """Gemini API 客户端封装类
    
    该类提供了与 Google Gemini API 交互的完整功能封装，支持基础内容生成和多轮对话。
    包含预设的模型配置，支持自定义配置，并提供完整的错误处理和日志记录。
    
    Attributes:
        MODEL_CONFIGS (Dict[str, Dict]): 预定义的模型配置字典，包含以下预设：
            - standard_response_json: 标准JSON响应配置
            - standard_response_text: 标准文本响应配置
            - creative: 创意型响应配置
            每个配置包含 temperature, top_p, top_k, max_output_tokens 等参数
            
        DEFAULT_MODEL (str): 默认使用的模型名称，当前为 "gemini-1.5-flash"
        model_name (str): 当前使用的模型名称
        generation_config (Dict): 当前使用的生成配置
        model: Gemini API 模型实例
        logger: 日志记录器实例

    Methods:
        __init__(model_name: str = None, config_preset: str = "standard_response_json", 
                 custom_config: Dict[str, Any] = None):
            初始化客户端，设置模型和配置参数
            
        _get_api_key() -> str:
            从环境变量获取 API 密钥
            
        _initialize_api() -> None:
            初始化 Gemini API 和模型实例
            
        generate_content(input_text: str, system_instruction: str = None) -> Optional[str]:
            生成单轮对话内容，支持系统指令
            
        generate_with_history(history: List[Dict[str, Any]], 
                            system_instruction: str = None) -> Optional[str]:
            使用历史对话记录生成多轮对话内容，支持系统指令
            
    Raises:
        ValueError: 当配置预设无效或 API 密钥未找到时
        BlockedPromptException: 当内容生成被阻止时
        Exception: 其他 API 调用相关错误
        
    Example:
        >>> client = GeminiClient()
        >>> response = client.generate_content("你好，请介绍下Python")
        >>> print(response)
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
    
    try:  
        # 示例使用 generate_with_history
        print("\n=== 多轮对话示例 ===")
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
        
        response = client.generate_with_history(
            history=conversation_history,
            system_instruction="你是一个专业的Python编程教师，用简单易懂的方式回答问题"
        )
        
        print("AI回复（多轮对话）：")
        print(response)
        
    except Exception as e:
        print(f"发生错误：{str(e)}")
