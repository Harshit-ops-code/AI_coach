# AI Coding Coach

An intelligent coding education platform that leverages AI to provide personalized feedback, code analysis, and adaptive problem generation for learners of all levels.

## 🎯 Overview

AI Coding Coach is a full-stack application designed to help developers improve their coding skills through:
- **AI-Powered Code Evaluation**: Intelligent analysis of submitted code with constructive feedback
- **Adaptive Problem Generation**: Automatically generated coding challenges tailored to skill level
- **Real-time Code Analysis**: Syntax checking, performance analysis, and best practice suggestions
- **Interactive Learning Dashboard**: Track progress, view statistics, and manage learning paths
- **Live Code Editor**: Built-in IDE with syntax highlighting and real-time evaluation

## 📋 Project Structure

```
ai-coding-coach/
├── backend/                    # Python FastAPI backend
│   ├── main.py                # FastAPI application entry point
│   ├── service.py             # Core business logic and services
│   ├── models.py              # Data models and schemas
│   ├── database.py            # Database configuration and setup
│   ├── config.py              # Configuration management
│   ├── requirements.txt        # Python dependencies
│   ├── data/
│   │   ├── problems.json      # Coding problems database
│   │   └── templates.json     # Code templates
│   ├── utils/
│   │   ├── ai_evaluator.py    # AI-powered code evaluation
│   │   ├── code_analyzer.py   # Code analysis utilities
│   │   └── problem_generator.py # Dynamic problem generation
│   └── tests/
│       └── test_api.py        # API tests
│
├── frontend/                   # React + Vite frontend
│   ├── src/
│   │   ├── main.jsx           # React entry point
│   │   ├── App.jsx            # Main app component
│   │   ├── index.css          # Global styles
│   │   └── components/
│   │       ├── Chat/          # Chat interface
│   │       ├── Dashboard/     # Learning dashboard
│   │       ├── Editor/        # Code editor component
│   │       ├── Evaluation/    # Evaluation display
│   │       ├── Layout/        # Layout components
│   │       ├── Problem/       # Problem display
│   │       └── Stats/         # Statistics and analytics
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md                  # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

5. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 🔧 Key Features

### Backend Components

#### AI Evaluator (`utils/ai_evaluator.py`)
- Evaluates submitted code using AI models
- Provides constructive feedback and suggestions
- Identifies code quality issues and improvements

#### Code Analyzer (`utils/code_analyzer.py`)
- Performs syntax validation
- Checks for code smells and anti-patterns
- Analyzes complexity and performance
- Generates detailed analysis reports

#### Problem Generator (`utils/problem_generator.py`)
- Creates adaptive coding problems
- Adjusts difficulty based on user performance
- Generates diverse problem types
- Maintains problem database

### Frontend Components

#### Editor Component
- Syntax-highlighted code editor
- Real-time code validation
- Language detection and support
- Code execution simulation

#### Dashboard
- User progress tracking
- Statistics and analytics
- Problem history and solutions
- Performance metrics

#### Chat Interface
- AI-powered assistance
- Context-aware suggestions
- Real-time feedback
- Learning guidance

## 📊 API Endpoints

Key endpoints available in the backend:

- `POST /api/evaluate` - Submit code for evaluation
- `GET /api/problems` - Get available problems
- `POST /api/problems/generate` - Generate new problem
- `GET /api/user/stats` - Get user statistics
- `POST /api/chat` - Send message to AI coach

## 🛠️ Development

### Running Tests

```bash
cd backend
python -m pytest tests/
```

### Code Quality

The project follows:
- PEP 8 guidelines for Python code
- ESLint configuration for JavaScript
- Tailwind CSS for consistent styling

## 📦 Dependencies

### Backend
- FastAPI - Modern Python web framework
- Pydantic - Data validation
- SQLAlchemy - ORM
- OpenAI API - AI evaluation
- PyTest - Testing framework

### Frontend
- React 18+ - UI library
- Vite - Build tool
- Tailwind CSS - Utility-first CSS
- Axios - HTTP client

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💡 Roadmap

- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Peer review system
- [ ] Integration with LeetCode and HackerRank
- [ ] Collaborative coding sessions

## 🐛 Bug Reports

Found a bug? Please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details

## 📧 Contact

For questions or suggestions, please open an issue or contact the development team.

---

**Happy Learning! 🚀**
