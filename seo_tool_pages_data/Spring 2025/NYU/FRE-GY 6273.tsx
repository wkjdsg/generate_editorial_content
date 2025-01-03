import type { CourseInfo, Qsolver, Reading, transcribe } from './types';

export const courseInfo: CourseInfo = {
  "courseBasicInfo": {
    "courseTitle": "Corporate Valuation",
    "school": "NYU",
    "courseCode": "FRE-GY 6273",
    "credits": "not mentioned in the syllabus",
    "semester": "Spring 2025",
    "department": "not mentioned in the syllabus"
  },
  "instructorInfo": {
    "instructorName": "Professor Philips",
    "titlePosition": "not mentioned in the syllabus",
    "officeAddress": "not mentioned in the syllabus",
    "officeHours": "Flexible office hours, held online via Zoom",
    "contactInfo": {
      "email": "tp55@nyu.edu",
      "phone": "not mentioned in the syllabus"
    }
  },
  "assessmentAndGradingPolicy": {
    "weightings": {
      "assignments": "35%",
      "quizzes": "not mentioned in the syllabus",
      "midterm": "not mentioned in the syllabus",
      "final": "25%",
      "projects": "20%",
      "attendance": "-1% per absence or lateness"
    },
    "assessmentMethods": [
      "Homework",
      "Final exam",
      "VC valuations",
      "Group Project"
    ]
  }
};

export const productUsingInCourse: Qsolver = {
  "title": "How Asksia AI Qsolver Can Enhance Your Course Study",
  "description": "Asksia AI Qsolver can help you master corporate valuation techniques by providing in-depth explanations of complex concepts like the Edwards-Bell-Ohlson equation and robust statistical methods, crucial for the final exam and project.",
  "coreFeatures": [
    {
      "name": "Explain Deeper",
      "description": "Asksia AI Qsolver can provide deeper explanations of complex valuation models, such as the Fama-French and Hou-Mo-Xue-Zhang models, enhancing your understanding of Module 4 topics."
    },
    {
      "name": "Explain Easier",
      "description": "Asksia AI Qsolver simplifies challenging concepts like building financial models (Module 2) and the Modigliani-Cohn framework (Module 7), making them easier to grasp."
    },
    {
      "name": "Check Answer",
      "description": "Asksia AI Qsolver helps verify your answers for weekly homework assignments, ensuring you understand the application of valuation methods before the final exam."
    },
    {
      "name": "Visualization",
      "description": "Asksia AI Qsolver can generate visual aids to help understand complex financial statements and models, supporting your work on the group project and VC valuations."
    }
  ]
};

export const productUsingInCoursereading: Reading = {
  "title": "How Asksia Reading Can Enhance Your Course Study",
  "description": "Asksia Reading can significantly improve your learning experience in FRE-GY 6273 by efficiently handling course readings and materials, supporting various tasks from weekly homework to the final valuation project.",
  "coreFeatures": [
    {
      "name": "Multi-Document Support",
      "description": "This feature allows you to simultaneously analyze multiple financial statements from sources like Calcbench and TracXn, crucial for the valuation project and homework assignments."
    },
    {
      "name": "Language Selection",
      "description": "While not explicitly mentioned in the syllabus, this feature is beneficial if any supplementary readings or entrepreneur communications are in languages other than English."
    },
    {
      "name": "Automated Summaries",
      "description": "Asksia's automated summaries efficiently condense lengthy readings from Holthausen and Zmijewski (2020) and Sommers, Easton and Drake (2021), enabling better preparation for lectures and the final exam."
    },
    {
      "name": "Outline Recognition",
      "description": "This feature helps in navigating the complex modules of the course, such as Module 4 on robust statistics, allowing for better comprehension and organization of study materials."
    }
  ]
};

export const productUsingInCoursetranscribe: transcribe = {
  "title": "What can you do using Asksia AI Transcribe for your course study?",
  "description": "Asksia AI Transcribe helps international students in FRE-GY 6273 overcome language barriers and improve comprehension of course materials.",
  "coreFeatures": "- Access lecture recordings in your native language, regardless of the instructor's language, which is especially helpful given the global nature of the course and interactions with entrepreneurs and VCs in various time zones.\n- Create comprehensive class outlines from lecture recordings, simplifying review and preparation for weekly homework assignments, the final exam, and the valuation project.\n- Use the AI assistant to clarify confusing concepts discussed during the two one-hour lecture segments each week, enhancing understanding of topics such as financial modeling, robust statistics, and valuation techniques for mature and startup firms.\n- Easily review lecture content in your native language for each of the seven modules which cover topics such as accounting, valuation, and the cost of capital, thereby improving performance on weekly homework assignments (35% of the grade).\n- Prepare effectively for the final exam (25% of the grade) by reviewing the transcribed lectures from each module.\n- Improve collaboration with team members on the equity research report and accompanying valuation model for the group project (20% of the grade) by ensuring everyone understands the project\u2019s details.\n- Enhance your participation in the VC valuations (20% of the grade) by fully understanding discussions with entrepreneurs and VCs, regardless of the language spoken during these Zoom sessions."
};
