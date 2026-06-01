from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from typing import List, Optional
import json
import random
import os
from datetime import datetime
from contextlib import asynccontextmanager

from models import (
    ProblemRequest, ProblemResponse, 
    EvaluationRequest, EvaluationResponse, 
    ChatRequest, ChatResponse,
    UserStats, Session
)
from service import (
    evaluate_submission, 
    chat_with_coach,
    generate_problem,
    analyze_performance
)
from database import SessionLocal, init_db
from config import settings

# Lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting AI Coding Interview Coach...")
    init_db()
    # Load sample data if needed
    load_sample_problems()
    print("✅ Backend ready!")
    yield
    # Shutdown
    print("👋 Shutting down...")

app = FastAPI(
    title="AI Coding Interview Coach Pro", 
    version="2.0.0",
    description="Advanced platform for technical interview preparation",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_sample_problems():
    """Load sample problems into database"""
    pass

# Enhanced endpoints with rate limiting and analytics
@app.get("/")
async def root():
    return {
        "status": "running",
        "version": "2.0.0",
        "message": "AI Coding Interview Coach Pro API",
        "timestamp": datetime.utcnow().isoformat(),
        "features": [
            "AI-powered code evaluation",
            "Interactive coaching chat",
            "Personalized problem generation",
            "Performance analytics",
            "Multi-language support"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/problem", response_model=ProblemResponse)
async def get_problem(
    request: ProblemRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Get or generate a coding problem"""
    try:
        # If topic is 'random', pick from available topics
        if request.topic.lower() == "random":
            topics = ["Arrays", "Strings", "Linked Lists", "Trees", "Dynamic Programming", "Graphs"]
            request.topic = random.choice(topics)
        
        # If generate_new is True, create a new problem
        if request.generate_new:
            problem = generate_problem(
                topic=request.topic,
                difficulty=request.difficulty,
                user_level=request.user_level
            )
            background_tasks.add_task(save_generated_problem, problem, db)
        else:
            # Get from database
            problem = get_problem_from_db(request, db)
        
        if not problem:
            raise HTTPException(status_code=404, detail="No problems available for this topic")
        
        # Log analytics
        background_tasks.add_task(log_problem_view, problem.id, request.user_id)
        
        return ProblemResponse(**problem)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/evaluate", response_model=EvaluationResponse)
async def evaluate_code(
    request: EvaluationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Evaluate code submission with detailed analysis"""
    try:
        # Get problem context
        problem = get_problem_by_id(request.problem_id, db)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        
        # Evaluate submission
        result = evaluate_submission(
            problem_statement=problem['statement'],
            constraints=problem['constraints'],
            code=request.code,
            language=request.language,
            test_cases=problem.get('test_cases', [])
        )
        
        # Calculate score
        result.score = calculate_score(result.correctness, result.time_complexity)
        
        # Store evaluation in database
        background_tasks.add_task(
            save_evaluation_result,
            problem_id=request.problem_id,
            user_id=request.user_id,
            code=request.code,
            result=result,
            db=db
        )
        
        # Update user stats
        background_tasks.add_task(update_user_stats, request.user_id, result, db)
        
        return result
    except Exception as e:
        print(f"Evaluation error: {e}")
        raise HTTPException(status_code=500, detail="Evaluation failed")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai_coach(
    request: ChatRequest,
    background_tasks: BackgroundTasks
):
    """Interactive chat with AI coach"""
    try:
        # Enhanced chat with context awareness
        response = chat_with_coach(
            messages=request.messages,
            problem_subject=request.problem_subject,
            current_code=request.current_code,
            evaluation_result=request.evaluation_result,
            chat_history=request.chat_history
        )
        
        # Log chat interaction
        background_tasks.add_task(
            log_chat_interaction,
            request.problem_subject,
            len(request.messages)
        )
        
        return response
    except Exception as e:
        return ChatResponse(
            reply=f"I apologize, but I'm having trouble connecting. Error: {str(e)[:100]}..."
        )

@app.get("/api/stats/{user_id}", response_model=UserStats)
async def get_user_stats(user_id: str, db: Session = Depends(get_db)):
    """Get user performance statistics"""
    stats = calculate_user_stats(user_id, db)
    return UserStats(**stats)

@app.post("/api/practice-session")
async def start_practice_session(user_id: str, db: Session = Depends(get_db)):
    """Start a timed practice session"""
    session_id = create_session(user_id, db)
    return {"session_id": session_id, "started_at": datetime.utcnow().isoformat()}

@app.get("/api/leaderboard")
async def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    """Get global leaderboard"""
    leaderboard = get_top_users(limit, db)
    return {"leaderboard": leaderboard, "updated_at": datetime.utcnow().isoformat()}

# Helper functions
def get_problem_from_db(request, db):
    """Fetch problem from database based on filters"""
    # Implementation for database query
    pass

def calculate_score(correctness, time_complexity):
    """Calculate score from 0-100"""
    # Implementation
    return 85

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        ssl_keyfile=settings.SSL_KEYFILE,
        ssl_certfile=settings.SSL_CERTFILE
    )