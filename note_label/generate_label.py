from GeminiClient import GeminiClient
import json
import os
from Utils import load_json_file,group_label
from prompt import label_prompt
import dotenv
import logging

dotenv.load_dotenv()

class LabelGenerator:
    def __init__(self, label_file_path="label.json"):
        self.label_file_path = label_file_path
        self.client = GeminiClient()
    
    def load_labels(self):
        try:
            return load_json_file(self.label_file_path)
        except Exception as e:
            logging.error(f"加载标签文件失败: {str(e)}")
            return {}
    
    def format_system_instruction(self, question, grouped_labels):
        try:
            labels_str = json.dumps(grouped_labels, ensure_ascii=False, indent=2)
            return (
                f"{label_prompt}\n"
                f"this is already exist label, using them first if possible\n"
                f"{labels_str}\n"
                f"this is user question\n"
                f"{question}"
            )
        except Exception as e:
            logging.error(f"格式化系统指令失败: {str(e)}")
            return ""
    
    @staticmethod
    def generate_label_dict(label_1, label_2):
        """
        生成标准格式的标签字典
        
        Args:
            label_1: 第一个标签
            label_2: 第二个标签
            
        Returns:
            Dict[str, Any]: 包含两个标签的字典
        """
        return {
            "label-1": label_1,
            "label-2": label_2
        }
    
    def save_label_to_file(self, response):
        """
        从AI响应中提取标签并保存到文件中
        
        Args:
            response: AI生成的响应
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # 尝试解析响应为JSON格式
            response_dict = json.loads(response)
            
            # 提取 'what to memory' 的值
            if 'what to memory' not in response_dict:
                logging.error("响应中未找到 'what to memory' 字段")
                return False
                
            new_labels = response_dict['what to memory']
            
            # 加载现有标签
            existing_labels = self.load_labels()
            
            # 确保existing_labels是列表
            if not isinstance(existing_labels, list):
                existing_labels = []
            
            # 将新标签添加到列表中
            if isinstance(new_labels, dict):
                existing_labels.append(new_labels)
            elif isinstance(new_labels, list):
                existing_labels.extend(new_labels)
            
            # 保存到文件
            with open(self.label_file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_labels, f, ensure_ascii=False, indent=2)
            print(f"保存标签成功，标签数量: {len(existing_labels)}")
            return True
            
        except json.JSONDecodeError as e:
            logging.error(f"解析响应JSON失败: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"保存标签时发生错误: {str(e)}")
            return False

    def generate_label_for_one_question(self, question: str) -> dict | str:
        """
        为单个问题生成标签。

        Args:
            question: 需要生成标签的问题文本

        Returns:
            dict: 成功时返回AI生成的响应字典
            str: 失败时返回错误信息

        Raises:
            ValueError: 当输入问题为空时
            JSONDecodeError: 当AI响应无法解析为JSON时
        """
        if not question.strip():
            return "问题不能为空"

        try:
            # 加载并处理标签
            label_data = self.load_labels()
            grouped_labels = group_label(label_data)
            
            # 生成系统指令
            system_instruction = self.format_system_instruction(question, grouped_labels)
            if not system_instruction:
                logging.error("系统指令生成失败")
                return "系统指令生成失败"
            
            # 调用AI生成响应
            response = self.client.generate_content(system_instruction)
            
            # 验证响应格式
            try:
                response_dict = json.loads(response)
                print(response_dict)
            except json.JSONDecodeError:
                logging.error("AI响应格式无效，无法解析为JSON")
                return "AI响应格式无效"
            
            # 保存新生成的标签
            if self.save_label_to_file(response):
                return response_dict
            else:
                return "保存标签失败"
            
        except Exception as e:
            logging.error(f"标签生成过程发生错误: {str(e)}")
            return f"生成标签时发生错误: {str(e)}"
    
    def generate_label_for_question_list(self, question_list):
        """
        批量处理问题列表并生成标签
        
        Args:
            question_list: 待处理的问题列表
            
        Returns:
            bool: 处理是否成功
        """
        try:
            all_new_labels = {}  # 存储所有新生成的标签
            
            # 逐个处理问题，收集所有新标签
            for question in question_list:
                label_data = self.load_labels()
                grouped_labels = group_label(label_data)
                
                # 生成系统指令
                system_instruction = self.format_system_instruction(question, grouped_labels)
                if not system_instruction:
                    logging.error(f"问题 '{question}' 的系统指令生成失败")
                    continue
                
                # 调用AI生成响应
                response = self.client.generate_content(system_instruction)
                try:
                    response_dict = json.loads(response)
                    
                    if 'what to memory' not in response_dict:
                        logging.error(f"问题 '{question}' 的响应中未找到 'what to memory' 字段")
                        continue
                        
                    # 收集新标签
                    all_new_labels.update(response_dict['what to memory'])
                    
                except json.JSONDecodeError as e:
                    logging.error(f"解析问题 '{question}' 的响应失败: {str(e)}")
                    continue
            
            # 批量更新所有标签
            if all_new_labels:
                existing_labels = self.load_labels()
                existing_labels.update(all_new_labels)
                
                # 一次性保存所有更新
                with open(self.label_file_path, 'w', encoding='utf-8') as f:
                    json.dump(existing_labels, f, ensure_ascii=False, indent=2)
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"批量处理问题列表时发生错误: {str(e)}")
            return False
        






