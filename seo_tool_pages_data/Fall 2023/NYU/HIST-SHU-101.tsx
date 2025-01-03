import type { CourseInfo, Qsolver, Reading, transcribe } from './types';

export const courseInfo: CourseInfo = {
  "courseBasicInfo": {
    "courseTitle": "FOUNDATIONS IN THE HUMANITIES What is History?",
    "school": "NYU",
    "courseCode": "HIST-SHU-101",
    "credits": "not mentioned in the syllabus",
    "semester": "Fall 2023",
    "department": "Humanities and History"
  },
  "instructorInfo": {
    "instructorName": "Duane Corpis",
    "titlePosition": "Associate Professor of Humanities and History",
    "officeAddress": "W810",
    "officeHours": "Tuesdays, 11:00 am-1:00 pm or by appointment",
    "contactInfo": {
      "email": "duane.corpis@nyu.edu",
      "phone": "not mentioned in the syllabus"
    }
  },
  "assessmentAndGradingPolicy": {
    "weightings": {
      "assignments": "30%",
      "quizzes": "not mentioned in the syllabus",
      "midterm": "not mentioned in the syllabus",
      "final": "not mentioned in the syllabus",
      "projects": "not mentioned in the syllabus",
      "attendance": "15%"
    },
    "assessmentMethods": [
      "5 writing activities",
      "in-class presentation",
      "overall course participation"
    ]
  }
};

export const productUsingInCourse: Qsolver = {
  "title": "How Asksia AI Qsolver Can Enhance Your Course Study",
  "description": "Asksia AI Qsolver can help History students at NYU Shanghai master complex concepts, check their understanding of historical methods and interpretations, and prepare for essay assignments.",
  "coreFeatures": [
    {
      "name": "Explain Deeper",
      "description": "Asksia AI Qsolver can provide in-depth explanations of complex historical concepts like periodization, temporality, and historiography, as discussed in the course readings by Hunt, Thompson, and Trouillot."
    },
    {
      "name": "Explain Easier",
      "description": "The tool simplifies challenging topics such as microhistory (Natalie Zemon Davis) and world-systems analysis (Immanuel Wallerstein), making them easier to grasp for essay writing."
    },
    {
      "name": "Check Answer",
      "description": "Students can verify their understanding of historical interpretations and arguments presented in assigned readings (e.g., Maza, Trouillot) and writing assignments (Writing Activities 1-5)."
    },
    {
      "name": "Visualization",
      "description": "While Asksia AI Qsolver may not directly provide visual aids, it can help students process complex information from the course readings (e.g., Braudel's model of the Mediterranean) to create their own visualizations."
    }
  ]
};

export const productUsingInCoursereading: Reading = {
  "title": "How Asksia Reading Can Enhance Your Course Study",
  "description": "Asksia Reading can significantly improve your reading comprehension and research skills for HIST-SHU-101, Foundations in the Humanities.",
  "coreFeatures": [
    {
      "name": "Multi-Document Support",
      "description": "Asksia Reading's multi-document support helps you synthesize information from multiple sources, such as the required books (Davis, Dessalles, Maza, Trouillot) and online articles, crucial for writing assignments like Writing Activity 3 and Writing Activity 5."
    },
    {
      "name": "Language Selection",
      "description": "While not explicitly needed for this syllabus, Asksia Reading's language support could benefit students needing to access materials in languages other than English, potentially expanding research options beyond the provided NYU Bobst Library resources."
    },
    {
      "name": "Automated Summaries",
      "description": "Asksia Reading's automated summaries efficiently condense lengthy readings like Braudel's *The Mediterranean* or Wallerstein's *World-Systems Analysis*, saving time and improving comprehension, thereby better preparing for in-class discussions and essay writing (e.g., Writing Activity 3 and 4)."
    },
    {
      "name": "Outline Recognition",
      "description": "Asksia Reading's outline recognition helps you navigate complex texts, such as those required for the course, improving your ability to extract key arguments and evidence for your writing assignments (e.g., Writing Activity 1, 2, 4, and 5) and presentations."
    }
  ]
};

export const productUsingInCoursetranscribe: transcribe = {
  "title": "What can you do using Asksia AI Transcribe for your course study?",
  "description": "Asksia AI Transcribe helps international students overcome language barriers and improve comprehension in the HIST-SHU-101 course.",
  "coreFeatures": [
    "Multilingual transcription of class recordings (Tuesdays and Thursdays, 1:45-3:00 pm sessions) allows for review in your native language, facilitating better understanding of complex topics discussed by Professor Duane Corpis.",
    "Detailed class outlines generated from the transcriptions help in organizing study materials and reviewing lecture content, aligning with the course's focus on research methods, approaches to writing history, and historiography.",
    "AI assistance can be used to clarify complex terms, concepts, and arguments related to historical research, source analysis, and historiographical debates, thereby aiding in achieving the course learning outcomes.",
    "The tool's real-time translation feature helps students actively participate in discussions, which counts towards 15% of the final grade, and enhances engaged learning by allowing them to quickly grasp and respond to ideas expressed during class.",
    "Asksia AI Transcribe assists in understanding the assigned readings, including those from authors like Natalie Zemon Davis, Pierre Dessalles, Sarah Maza, and Michel-Rolph Trouillot, improving comprehension and written assignment quality (5%, 5%, 15%, 15%, and 30% of the final grade, respectively).",
    "The transcriptions and outlines can be used to effectively prepare for the in-class presentation (15% of final grade), helping to organize thoughts and understand discussion points."
  ]
};
