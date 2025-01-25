import json

# 读取文件
with open(r"D:\generate_editorial_content\ai-generator\generate_seo_data\seo_content_results.json", "r", encoding="utf-8") as file:
    contents = json.load(file)

# 定义需要检查的字段和其对应的数据类型
format_configs = {
    "productUsingInCourse": dict,
    "productUsingInCoursereading": dict,
    "productUsingInCoursetranscribe": dict,
    "courseInfo": dict,
    "FAQ": list
}

print("Starting validation checks...")
errors = []

# 检查每个content对象
for index, content in enumerate(contents, 1):
    content_errors = []
    
    # 1. 检查是否具备所有必要字段
    missing_fields = []
    for field in format_configs.keys():
        if field not in content:
            missing_fields.append(field)
    
    if missing_fields:
        content_errors.append(f"Missing required fields: {', '.join(missing_fields)}")
    
    # 2. 检查数据类型是否正确
    wrong_types = []
    for field, expected_type in format_configs.items():
        if field in content and not isinstance(content[field], expected_type):
            wrong_types.append(f"{field} (expected {expected_type.__name__}, got {type(content[field]).__name__})")
    
    if wrong_types:
        content_errors.append(f"Incorrect data types found: {', '.join(wrong_types)}")
    
    if content_errors:
        errors.append({
            "index": index,
            "errors": content_errors
        })

# 打印错误汇总
if errors:
    print("\nValidation Errors Found:")
    for error in errors:
        print(f"\nIndex #{error['index']}:")
        for err_msg in error['errors']:
            print(f"- {err_msg}")
else:
    print("\nNo errors found in validation.")

print("\nValidation complete!")

