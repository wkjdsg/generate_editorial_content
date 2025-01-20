from PyPDF2 import PdfReader

def extract_pdf_text(pdf_path: str) -> str:
    """
    从PDF文件中提取文本内容
    
    Args:
        pdf_path (str): PDF文件的路径
        
    Returns:
        str: 提取的文本内容
        
    Raises:
        FileNotFoundError: 当PDF文件不存在时
        PyPDFError: 当PDF文件损坏或无法读取时
    """
    try:
        # 创建PDF阅读器对象
        reader = PdfReader(pdf_path)
        
        # 存储所有页面的文本
        text_content = []
        
        # 遍历所有页面并提取文本
        for page in reader.pages:
            text_content.append(page.extract_text())
            
        # 将所有页面的文本合并，用换行符分隔
        return '\n'.join(text_content)
        
    except FileNotFoundError:
        raise FileNotFoundError(f"找不到PDF文件: {pdf_path}")
    except Exception as e:
        raise Exception(f"读取PDF文件时发生错误: {str(e)}")

# 使用示例
if __name__ == "__main__":
    try:
        pdf_path = r"test_syllabus_pdf\Syllabus-What is History-Fall 2023-Version 20230907.pdf"
        text = extract_pdf_text(pdf_path)
        
        # 生成输出文件名（使用原PDF文件名，但改为.txt后缀）
        output_path = pdf_path.rsplit('.', 1)[0] + '.txt'
        
        # 将文本保存到文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
            
        print(f"文本已保存到: {output_path}")
    except Exception as e:
        print(f"错误: {str(e)}")
