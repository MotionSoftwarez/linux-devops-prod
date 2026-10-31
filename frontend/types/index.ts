export type LearningGoal =
  | "beginner"
  | "administrator"
  | "devops"
  | "troubleshooter"
  | "interview"
  | "advanced";

export interface LearningPath {
  id: number;
  key: string;
  title: string;
  description?: string;
  estimated_hours?: number;
  order: number;
  is_active: boolean;
}

export interface Module {
  id: number;
  key: string;
  title: string;
  description?: string;
  stage?: string;
  order: number;
  estimated_hours?: number;
  is_active: boolean;
}

export interface Lesson {
  id: number;
  module_id: number;
  key: string;
  title: string;
  slug: string;
  order: number;
  difficulty: string;
  estimated_minutes: number;
  summary?: string;
  content?: any;
  has_lab: boolean;
  has_quiz: boolean;
}

export interface Lab {
  id: number;
  lesson_id: number;
  title: string;
  objective: string;
  completion_criteria: any;
  safe_commands?: string[];
}

export interface LabScenario {
  id: number;
  key: string;
  title: string;
  context?: string;
  symptoms?: string;
  evidence?: string;
  root_cause?: string;
  solution?: string;
  verification?: string;
  prevention?: string;
  is_guided: boolean;
}

export interface CheatSheet {
  id: number;
  key: string;
  title: string;
  topic: string;
  category?: string;
  content: any;
}

export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  learning_goal?: LearningGoal;
  is_active: boolean;
  is_guest: boolean;
}

export interface Progress {
  id: number;
  user_id: number;
  lesson_id: number;
  module_id: number;
  status: string;
  quiz_score?: number;
  lab_passed: boolean;
}
