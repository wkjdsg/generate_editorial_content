#添加函数读取json文件并返回json文件变量

import json
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

#输入json和要修改的key，和对应的动作，返回修改后的json，暂定action只有delete
def modify_json_file(json_data, key, action):
    if action == 'delete':
        del json_data[key]
    return json_data
#统计json文件中key的个数
def count_key_in_json(json_data, key):
    count = 0
    for item in json_data:
        if key in item:
            count += 1
    return count
def check_json_structure(json_data):
    """
    核实json文件中的每一个dict是否包含相同的key结构，并检查每个key对应的数据结构是否一致
    
    Args:
        json_data: JSON数据列表，每个元素为字典
        
    Returns:
        dict: 包含以下键:
            - 'all_keys': 所有出现的键列表
            - 'is_consistent': 布尔值，表示所有字典是否具有相同的键
            - 'missing_keys': 字典，键为索引，值为该索引处字典缺少的键
            - 'structure_consistent': 布尔值，表示所有字典中相同键的数据结构是否一致
            - 'structure_issues': 字典，记录数据结构不一致的问题
    """
    if not json_data or not isinstance(json_data, list):
        return {"error": "输入数据必须是非空列表"}
    
    # 获取所有唯一键
    all_keys = set()
    for item in json_data:
        if isinstance(item, dict):
            for key in item.keys():
                all_keys.add(key)
    
    all_keys = list(all_keys)
    
    # 检查每个字典是否包含所有键
    is_consistent = True
    missing_keys = {}
    
    for idx, item in enumerate(json_data):
        if not isinstance(item, dict):
            missing_keys[idx] = f"项目不是字典: {type(item)}"
            is_consistent = False
            continue
            
        item_keys = set(item.keys())
        if item_keys != set(all_keys):
            is_consistent = False
            missing = set(all_keys) - item_keys
            if missing:
                missing_keys[idx] = list(missing)
    
    # 检查每个键的数据结构是否一致
    structure_consistent = True
    structure_issues = {}
    
    # 为每个键创建一个类型映射
    key_type_maps = {}
    
    for key in all_keys:
        key_type_maps[key] = {}
        
        for idx, item in enumerate(json_data):
            if not isinstance(item, dict) or key not in item:
                continue
                
            value = item[key]
            value_type = type(value).__name__
            
            # 对于列表和字典，进一步检查其内部结构
            if isinstance(value, list) and value:
                inner_type = type(value[0]).__name__
                value_type = f"list[{inner_type}]"
                
                # 检查列表中的所有元素类型是否一致
                if not all(isinstance(x, type(value[0])) for x in value):
                    value_type = "list[mixed]"
                    
            elif isinstance(value, dict) and value:
                dict_keys = sorted(list(value.keys()))
                value_type = f"dict{dict_keys}"
            
            if value_type not in key_type_maps[key]:
                key_type_maps[key][value_type] = []
            
            key_type_maps[key][value_type].append(idx)
    
    # 检查每个键是否有多种数据结构
    for key, type_map in key_type_maps.items():
        if len(type_map) > 1:
            structure_consistent = False
            structure_issues[key] = {
                "types": list(type_map.keys()),
                "counts": {t: len(idxs) for t, idxs in type_map.items()}
            }
    
    return {
        "all_keys": all_keys,
        "is_consistent": is_consistent,
        "missing_keys": missing_keys,
        "structure_consistent": structure_consistent,
        "structure_issues": structure_issues
    }
#核实json文件中的每一个dict是否包含的key数据结构一样，我要所有的key的名称，并返回一个列表，基于列表核实是否所有的key的名称都一样，数据结构是否一样

def print_json_structure_log(json_data):
    """
    打印JSON结构检查的日志信息
    
    Args:
        json_data: JSON数据列表，每个元素为字典
    """
    result = check_json_structure(json_data)
    
    if "error" in result:
        print(f"错误: {result['error']}")
        return
    
    print(f"JSON文件中共有 {len(json_data)} 个项目")
    print(f"所有键: {', '.join(result['all_keys'])}")
    print(f"键一致性: {'一致' if result['is_consistent'] else '不一致'}")
    
    if not result['is_consistent']:
        print("\n键不一致项目详情:")
        for idx, missing in result['missing_keys'].items():
            print(f"  项目 #{idx}: {missing}")
    
    print(f"\n数据结构一致性: {'一致' if result['structure_consistent'] else '不一致'}")
    
    if not result['structure_consistent']:
        print("\n数据结构不一致详情:")
        for key, issues in result['structure_issues'].items():
            print(f"  键 '{key}' 有多种数据结构:")
            for type_name, count in issues['counts'].items():
                print(f"    - {type_name}: {count}个项目")
    
    print("\n键出现频率统计:")
    for key in result['all_keys']:
        count = count_key_in_json(json_data, key)
        percentage = (count / len(json_data)) * 100
        print(f"  {key}: {count}/{len(json_data)} ({percentage:.1f}%)")

if __name__ == '__main__':
    json_data = read_json_file('transcribe/implement/seo_content_results_modified.json')
    print_json_structure_log(json_data)

