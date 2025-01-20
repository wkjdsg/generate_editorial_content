def solver_seo_content(api_key: str, syllabus_text: str) -> Optional[str]:
    try:
        # 从环境变量获取API密钥
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("API key not found in environment variables")

        # Configure API
        genai.configure(api_key=api_key)
        logger.info("API configured successfully")

        # Create the model with config
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }

        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="""
You will receive a product introduction and a syllabus. Your task is to help students understand how this product can be used in the classroom based on the course content outlined in the syllabus. Output your response in JSON format. Make sure to reference relevant details from the syllabus to enrich your response.

Please complete the following JSON structure:

```json
{
  "title": "How Asksia AI Qsolver Can Enhance Your Course Study",
  "description": "A brief sentence description of how Asksia AI Qsolver can support students in the course, highlighting its relevance to the syllabus.",
  "coreFeatures": [
    {
      "name": "Explain Deeper",
      "description": "Concise sentence on how the product helps students understand complex concepts in depth, based on syllabus topics."
    },
    {
      "name": "Explain Easier",
      "description": "Concise sentence on how the product simplifies difficult concepts for easier comprehension in line with syllabus content."
    },
    {
      "name": "Check Answer",
      "description": "Concise sentence on how the product helps students verify their answers and understand where they may have gone wrong, linked to specific syllabus exercises or topics."
    },
    {
      "name": "Visualization",
      "description": "Concise sentence on how the product supports visual learning, such as through diagrams or graphs, aligned with syllabus topics."
    }
  ]
}
```

Each description should be:
- A single, concise sentence.
- Directly linked to relevant content from the syllabus and the product features.
"""
                )
            logger.info("AI model initialized successfully")

            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [syllabus_text],
                    },
                ]
            )
            
            response = chat_session.send_message("INSERT_INPUT_HERE")
            logger.info("Successfully generated SEO content")
            return response.text

        except genai.types.generation_types.BlockedPromptException as e:
            logger.error(f"Content generation blocked: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error during content generation: {str(e)}")
            raise

    except Exception as e:
        logger.error(f"Unexpected error in generate_seo_content: {str(e)}")
        return None