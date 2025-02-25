import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
dataformat_path = os.path.join(current_dir, 'dataformat.json')

with open(dataformat_path, 'r') as f:
    data = json.load(f)

title = data["title"]
transcribe_content = data["TranscribePageContent"]
faq = data["FAQ"]

system_instruction_header = """You are an AI assistant specialized in generating SEO-optimized content for transcription services.
Your task is to create engaging, informative content that highlights the benefits and features of our transcription service.
Focus on the following aspects:
1. Clear value proposition
2. Key features and benefits
3. Target audience needs
4. SEO optimization
5. Natural, persuasive language"""

# Transcribe prompt
transcribe = """Please generate content for AskSia's transcription service. The content should be informative, engaging, and optimized for SEO.
Focus on naturally incorporating the provided keyword while highlighting our core features and benefits.

For each feature below, create a compelling description that:
1. Naturally includes the keyword where appropriate
2. Emphasizes the specific benefits for the user
3. Uses engaging, persuasive language
4. Maintains SEO optimization
5. Connects with the user's needs and pain points

Core Features:
1. Real-time Transcription
[Describe how our real-time transcription technology transforms audio/video into text instantly. Emphasize speed, convenience, and supported formats. Connect this to the keyword and user needs.]

2. High-Accuracy Transcription Engine
[Explain our AI-powered accuracy, mentioning specific accuracy rates and how we handle different speaking conditions. Show how this relates to the keyword and solves user problems.]

3. Multi-language Support & Translation
[Detail our language capabilities, translation features, and how they break down communication barriers. Tie this back to the keyword and international use cases.]

Example format for each feature:
"[Feature Name]: [Engaging description that naturally incorporates the keyword and highlights user benefits]"

Remember to:
- Maintain a professional yet approachable tone
- Focus on practical benefits rather than technical details
- Use natural language that resonates with users
- Keep the keyword integration smooth and contextual
"""

# 添加固定的FAQ问题模板
faq_template = [
    {
        "question": "What file formats do you support for transcription?",
        "answer": "We support a wide range of audio and video formats including MP3, WAV, MP4, MOV, and many more. Our system can handle most common media formats."
    },
    {
        "question": "How accurate is the transcription?",
        "answer": "Our AI-powered transcription service achieves high accuracy rates, typically above 95% for clear audio. The accuracy may vary depending on factors like audio quality, background noise, and speaker clarity."
    },
    {
        "question": "How long does it take to transcribe my file?",
        "answer": "Our real-time transcription system processes files quickly. For most audio files, you'll receive your transcription within minutes. The exact time depends on the file length and complexity."
    }
]

        # Args:
        #     history: 对话历史记录列表，每个记录包含 role 和 parts
        #         格式: [{"role": "user"/"model", "parts": ["消息内容"]}]
        #     system_instruction: 可选，系统指令，用于设置模型的行为
