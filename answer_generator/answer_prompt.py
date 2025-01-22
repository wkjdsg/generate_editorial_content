import json
with open('dataformat.json', 'r') as f:
        data = json.load(f)

course_info = data["courseInfo"]
product_using = data["productUsingInCourse"]
product_reading = data["productUsingInCoursereading"]
product_transcribe = data["productUsingInCoursetranscribe"]
faq = data["FAQ"]

        # Args:
        #     history: 对话历史记录列表，每个记录包含 role 和 parts
        #         格式: [{"role": "user"/"model", "parts": ["消息内容"]}]
        #     system_instruction: 可选，系统指令，用于设置模型的行为
solver = """
AI Answer Generator - Your Intelligent Academic Assistant

Core Purpose:
An advanced AI-powered answer generation system that helps students and educators create comprehensive, accurate, and pedagogically sound responses to academic questions.

Key Features:

1. SMART ANSWER GENERATION
- Generates detailed, well-structured answers across multiple academic disciplines
- Utilizes context-aware understanding to provide relevant and accurate responses
- Maintains academic integrity while providing explanatory content
- Supports multiple answer formats: text, equations, code snippets, and diagrams

2. ADAPTIVE EXPLANATION LEVELS
- Intelligent depth adjustment based on question complexity
- Progressive disclosure: starts with core concepts, then builds to advanced details
- Multiple perspective approaches: theoretical foundations, practical applications, and real-world examples
- Customizable complexity levels to match user's understanding

3. ANSWER VALIDATION & ENHANCEMENT
- Real-time accuracy verification of mathematical calculations
- Logical consistency checking in argumentative responses
- Completeness assessment to ensure all aspects of the question are addressed
- Citation suggestions for academic credibility
- Auto-detection of potential misconceptions or gaps

4. INTERACTIVE VISUALIZATION
- Dynamic generation of supporting visuals for complex concepts
- Automatic creation of diagrams for scientific and technical explanations
- Step-by-step visual breakdowns of problem-solving processes
- Interactive graphs and charts for data representation

5. LEARNING OPTIMIZATION
- Includes relevant examples and practice questions
- Provides step-by-step solution breakdowns
- Offers alternative solution methods when applicable
- Suggests related concepts for deeper understanding
"""
reading = """
AI Reading Assistant - Enhanced Academic Text Analysis

Core Purpose:
An intelligent reading support system that helps users comprehend, analyze, and extract key information from academic materials efficiently and effectively.

Key Features:

1. ADVANCED DOCUMENT PROCESSING)
- Batch processing of up to 5 documents simultaneously
- Maximum file size: 20MB per document
- Efficient handling of documents up to 500 pages

2. SMART CONTENT NAVIGATION
- Automatic table of contents generation
- Quick jump to relevant sections
- Intelligent keyword search and highlighting
- Cross-reference linking between documents

3. AUTOMATED COMPREHENSION AIDS
- Real-time text simplification
- Key concept identification and explanation
- Technical term definitions and contextual usage
- Background information integration

4. INTERACTIVE SUMMARIZATION
- Multi-level summary generation (brief, detailed, comprehensive)
- Chapter-by-chapter breakdown
- Key points extraction
- Research findings highlight
- Methodology and conclusion focus

5. ENHANCED STUDY TOOLS
- Automatic citation generation
- Note-taking assistance
- Important quote extraction
- Study guide creation
- Concept relationship mapping
"""
transcribe = """
Transcribe Classroom Recordings
features:
1.Upload local audio files, and Asksia will transcribe the audio into multilingual subtitles, providing services such as intelligent summary, ChatBox Q&A, Assistant analysis, and Chinese translation to help students review classroom content more effectively.
2.Local File Upload
Supports uploading mainstream audio and video formats such as MP4, WAV, etc. It also enables multilingual transcription and translation. Once processed, the files will be stored in the "My Records" section.
3.Smart Outline
After the transcription is complete, the outline will automatically display detailed information, including keywords, main content, and key sentences from the classroom recording.
4.Dual-Screen Interaction
On the left side of the transcription page, the original content and translated content are displayed side by side. The recorded audio can be played simultaneously, with subtitles following the progress bar. On the right side, the Assistant AI will automatically generate relevant questions and answers based on the classroom content.
"""
system_instruction_header = """
You're an expert in SEO for a product called Asksia. You will receive a product introduction(here is the website of the product: https://www.asksia.ai/) and a {keyword}. Your task is to help students understand how this product can be used in the classroom based on the keyword. Output your response in JSON format. 
This content will be used for SEO to introduce the product to browsing users.
"""
