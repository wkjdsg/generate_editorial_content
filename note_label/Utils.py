# {already exist label, using them first if possible}
# {Student's question will be placed here}
import os

import json

def load_json_file(file_path):
    """
    加载JSON文件
    
    Args:
        file_path: JSON文件路径
        
    Returns:
        dict/list: JSON数据
        
    Raises:
        FileNotFoundError: 文件不存在时
        json.JSONDecodeError: JSON格式错误时
    """
    try:
        # 获取脚本所在目录的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建完整的文件路径
        full_path = os.path.join(current_dir, file_path)
        
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：找不到文件 '{file_path}'")
        print(f"当前搜索路径: {full_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"错误：JSON格式无效 - {str(e)}")
        return []

#该函数用于聚类整合label后返回内容，给入一个json，去除重复值后返回关于label-1和label-2的聚类结果
def group_label(json_data):
    """
    从JSON数据中提取并去重label-1和label-2
    
    Args:
        json_data: 包含label数据的列表或可迭代对象
        
    Returns:
        dict: 包含去重后的label-1和label-2列表的字典
        
    Raises:
        TypeError: 当输入数据类型不正确时
        KeyError: 当数据中缺少必要的键时
        ValueError: 当输入数据为空时
    """
    # 输入验证
    if not json_data:
        raise ValueError("输入数据不能为空")
    
    if not isinstance(json_data, (list, tuple)):
        raise TypeError("输入数据必须是列表或元组类型")

    # 初始化存储列表
    labels_1 = []
    labels_2 = []
    
    # 提取标签并进行错误处理
    for idx, item in enumerate(json_data):
        if not isinstance(item, dict):
            raise TypeError(f"第{idx}个元素必须是字典类型")
            
        try:
            label1 = item['label-1']
            label2 = item['label-2']
            
            # 确保标签值不为None
            if label1 is not None:
                labels_1.append(label1)
            if label2 is not None:
                labels_2.append(label2)
                
        except KeyError as e:
            raise KeyError(f"第{idx}个元素缺少必要的键: {str(e)}")
    
    # 去重并过滤空值
    unique_labels = {
        "label-1": sorted(list(set(filter(None, labels_1)))),
        "label-2": sorted(list(set(filter(None, labels_2))))
    }
    
    return unique_labels

