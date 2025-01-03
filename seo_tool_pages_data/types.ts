export interface CourseInfo {
  courseBasicInfo: {
    courseTitle: string;
    school: string;
    courseCode: string;
    credits: string;
    semester: string;
    department: string;
  };
  instructorInfo: {
    instructorName: string;
    titlePosition: string;
    officeAddress: string;
    officeHours: string;
    contactInfo: {
      email: string;
      phone: string;
    };
  };
  assessmentAndGradingPolicy: {
    weightings: {
      assignments: string;
      quizzes: string;
      midterm: string;
      final: string;
      projects: string;
      attendance: string;
    };
    assessmentMethods: string[];
  };
}

export interface Qsolver {
  title: string;
  description: string;
  coreFeatures: {
    name: string;
    description: string;
  }[];
} 

export interface Reading {
  title: string;
  description: string;
  coreFeatures: {
    name: string;
    description: string;
  }[];
} 

export interface transcribe {
  title: string;
  description: string;
  coreFeatures: string;
} 

export interface OtherSyllabus {
  courseCode: string;
  courseTitle: string;
  school: string;
  semester: string;
  link: string;
}