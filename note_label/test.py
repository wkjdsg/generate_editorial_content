#该脚本引入test.xlsx文件，读取文件中的数据，并调用generate_label类，进行测试，观测label.json最后的结果
import os
from generate_label import LabelGenerator
import pandas as pd
import time
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('label_generation.log'),
        logging.StreamHandler()
    ]
)

# 读取test.xlsx文件
df = pd.read_excel(r'D:\generate_editorial_content\note_label\test.xlsx')
#将第一列的数据存到一个question_list列表中
question_list = df.iloc[:, 0].tolist()

# 创建LabelGenerator实例
generator = LabelGenerator()

# 批量处理问题列表  ,添加计数时间，每一分钟处理15个问题，到了就休息一分钟。
#添加相关的报错和日志
count = 0
for question in question_list:
    try:
        print(f"正在处理第{count+1}个问题")
        print(f"问题内容: {question}")
        generator.generate_label_for_one_question(question)
        count += 1
        if count % 15 == 0:
            time.sleep(60)
            print(f"休息一分钟")
    except Exception as e:
        logging.error(f"处理问题时发生错误: {str(e)}")


