import json

# 读取JSON文件
with open('guide_pdf/generate_seo_data/seo_content_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


# 遍历列表中的每个字典,删除'keyword'键值对
for item in data:
    if 'keyword' in item:
        del item['keyword']

# 将修改后的数据写回文件
with open('guide_pdf/generate_seo_data/seo_content_results.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)