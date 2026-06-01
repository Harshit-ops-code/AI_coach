from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class Difficulty(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class Language(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CPP = "cpp"
    GO = "go"

class ProblemRequest(BaseModel):
    topic: str = "Arrays"
    difficulty: Optional[Difficulty] = None
    generate_new: bool = False
    user_level: Optional[str] = "intermediate"
    user_id: Optional[str] = None

class ProblemResponse(BaseModel):
    id: str
    topic: str
    difficulty: str
    statement: str
    constraints: str
    examples: List[Dict[str, Any]] = []
    test_cases: List[Dict[str, Any]] = []
    hints: List[str] = []
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    estimated_time: int = 30  # minutes

class EvaluationRequest(BaseModel):
    problem_id: str
    code: str
    language: Language = Language.PYTHON
    user_id: Optional[str] = None

class EvaluationResponse(BaseModel):
    correctness: str
    score: Optional[int] = None
    issues: List[str]
    time_complexity: str
    space_complexity: str
    one_improvement: str
    one_follow_up_question: str
    test_results: List[Dict[str, Any]] = []
    suggestions: List[str] = []
    execution_time: Optional[float] = None
    memory_usage: Optional[float] = None
    formatted_code: Optional[str] = None

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    problem_subject: str
    current_code: Optional[str] = None
    evaluation_result: Optional[EvaluationResponse] = None
    chat_history: Optional[List[Dict]] = None

class ChatResponse(BaseModel):
    reply: str
    suggestions: Optional[List[str]] = None
    resources: Optional[List[Dict[str, str]]] = None
    confidence: Optional[float] = None

class UserStats(BaseModel):
    user_id: str
    total_problems_solved: int = 0
    easy_solved: int = 0
    medium_solved: int = 0
    hard_solved: int = 0
    average_score: float = 0.0
    total_time_spent: int = 0  # minutes
    streak_days: int = 0
    topics_strength: Dict[str, float] = {}
    weaknesses: List[str] = []
    rank: Optional[int] = None
    percentile: Optional[float] = None

class LeaderboardEntry(BaseModel):
    user_id: str
    username: str
    score: int
    problems_solved: int
    rank: int
    avatar_url: Optional[str] = None

class Session(BaseModel):
    session_id: str
    user_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    problems_attempted: List[str] = []
    total_score: int = 0
    duration: Optional[int] = None  # in seconds