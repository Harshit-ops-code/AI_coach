import React, { useState, useEffect } from 'react';
import { 
  Brain, Code2, Trophy, TrendingUp, 
  Clock, Users, Sparkles, Zap,
  Bell, Settings, User, Search,
  Play, CheckCircle, AlertCircle,
  MessageSquare, BarChart3, Target
} from 'lucide-react';
import { Toaster, toast } from 'react-hot-toast';
import { motion, AnimatePresence } from 'framer-motion';

// Components
import Sidebar from './components/Layout/Sidebar';
import Navbar from './components/Layout/Navbar';
import Dashboard from './components/Dashboard/Dashboard';
import ProblemWorkspace from './components/Problem/ProblemWorkspace';
import CodeEditorPanel from './components/Editor/CodeEditorPanel';
import EvaluationPanel from './components/Evaluation/EvaluationPanel';
import ChatPanel from './components/Chat/ChatPanel';
import StatsPanel from './components/Stats/StatsPanel';
import PracticeSession from './components/Session/PracticeSession';
import Leaderboard from './components/Stats/Leaderboard';

// Hooks
import useLocalStorage from './hooks/useLocalStorage';
import { useProblem } from './hooks/useProblem';
import { useEvaluation } from './hooks/useEvaluation';

// API
import { 
  fetchProblem, 
  submitEvaluation, 
  sendChatMessage,
  getUserStats,
  startPracticeSession
} from './utils/api';

// Theme
import { ThemeProvider } from './context/ThemeContext';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentProblem, setCurrentProblem] = useState(null);
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [evaluation, setEvaluation] = useState(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [sessionActive, setSessionActive] = useState(false);
  const [sessionTime, setSessionTime] = useState(0);
  const [userStats, setUserStats] = useState(null);
  const [theme, setTheme] = useLocalStorage('theme', 'dark');
  const [notifications, setNotifications] = useState([]);
  
  // Initialize
  useEffect(() => {
    loadUserStats();
    checkForNotifications();
  }, []);
  
  const loadUserStats = async () => {
    try {
      const stats = await getUserStats('user-123');
      setUserStats(stats);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };
  
  const handleProblemSelect = async (topic, difficulty) => {
    toast.loading('Loading problem...');
    try {
      const problem = await fetchProblem({
        topic,
        difficulty,
        generate_new: false
      });
      setCurrentProblem(problem);
      setActiveTab('workspace');
      toast.dismiss();
      toast.success(`Loaded ${difficulty} ${topic} problem`);
      
      // Set template code
      const template = getCodeTemplate(language, topic);
      setCode(template);
    } catch (error) {
      toast.error('Failed to load problem');
    }
  };
  
  const handleEvaluate = async () => {
    if (!currentProblem || !code.trim()) {
      toast.error('Write some code first!');
      return;
    }
    
    setIsEvaluating(true);
    toast.loading('Evaluating your solution...');
    
    try {
      const result = await submitEvaluation({
        problem_id: currentProblem.id,
        code,
        language,
        user_id: 'user-123'
      });
      
      setEvaluation(result);
      
      if (result.correctness === 'Correct') {
        toast.success('🎉 Excellent! Your solution is correct!');
      } else if (result.correctness === 'Partial') {
        toast('⚠️ Solution needs improvement', {
          icon: '⚠️'
        });
      } else {
        toast.error('❌ Solution has issues');
      }
    } catch (error) {
      toast.error('Evaluation failed. Try again.');
    } finally {
      setIsEvaluating(false);
      toast.dismiss();
    }
  };
  
  const handleStartSession = async () => {
    try {
      const session = await startPracticeSession('user-123');
      setSessionActive(true);
      setSessionTime(0);
      toast.success('Practice session started! Timer: 45:00');
    } catch (error) {
      toast.error('Failed to start session');
    }
  };
  
  const getCodeTemplate = (lang, topic) => {
    const templates = {
      python: {
        Arrays: `def solution(nums, target):
    """
    Problem: Two Sum
    Input: List of integers, target integer
    Return: Indices of two numbers that add to target
    """
    # Your code here
    pass`,
        Trees: `class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def solution(root):
    # Your code here
    pass`
      }
    };
    return templates[lang]?.[topic] || '# Start coding here...';
  };
  
  return (
    <ThemeProvider value={{ theme, setTheme }}>
      <div className={`min-h-screen transition-colors duration-300
        ${theme === 'dark' 
          ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-gray-100'
          : 'bg-gradient-to-br from-gray-50 via-white to-blue-50 text-gray-800'
        }`}>
        
        <Toaster 
          position="top-right"
          toastOptions={{
            style: {
              background: theme === 'dark' ? '#1f2937' : '#ffffff',
              color: theme === 'dark' ? '#f9fafb' : '#111827',
              border: `1px solid ${theme === 'dark' ? '#374151' : '#e5e7eb'}`,
            },
          }}
        />
        
        {/* Navbar */}
        <Navbar 
          theme={theme}
          setTheme={setTheme}
          notifications={notifications}
          userStats={userStats}
        />
        
        <div className="flex h-screen pt-16">
          {/* Sidebar */}
          <Sidebar 
            activeTab={activeTab}
            setActiveTab={setActiveTab}
            userStats={userStats}
          />
          
          {/* Main Content */}
          <main className="flex-1 overflow-hidden p-6">
            <AnimatePresence mode="wait">
              {activeTab === 'dashboard' && (
                <motion.div
                  key="dashboard"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.3 }}
                >
                  <Dashboard 
                    onSelectProblem={handleProblemSelect}
                    userStats={userStats}
                    onStartSession={handleStartSession}
                  />
                </motion.div>
              )}
              
              {activeTab === 'workspace' && currentProblem && (
                <motion.div
                  key="workspace"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="h-full"
                >
                  <div className="grid grid-cols-12 gap-6 h-full">
                    {/* Problem Panel */}
                    <div className="col-span-3">
                      <ProblemWorkspace 
                        problem={currentProblem}
                        onBack={() => setActiveTab('dashboard')}
                        theme={theme}
                      />
                    </div>
                    
                    {/* Editor Panel */}
                    <div className="col-span-6 flex flex-col gap-4">
                      <CodeEditorPanel
                        code={code}
                        setCode={setCode}
                        language={language}
                        setLanguage={setLanguage}
                        theme={theme}
                        onRun={handleEvaluate}
                        isRunning={isEvaluating}
                        problem={currentProblem}
                      />
                      
                      {evaluation && (
                        <EvaluationPanel 
                          evaluation={evaluation}
                          theme={theme}
                        />
                      )}
                    </div>
                    
                    {/* Chat & Stats Panel */}
                    <div className="col-span-3 flex flex-col gap-4">
                      <ChatPanel
                        problem={currentProblem}
                        currentCode={code}
                        evaluation={evaluation}
                        theme={theme}
                      />
                      
                      <StatsPanel 
                        userStats={userStats}
                        problem={currentProblem}
                        theme={theme}
                      />
                    </div>
                  </div>
                </motion.div>
              )}
              
              {activeTab === 'stats' && (
                <motion.div
                  key="stats"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <div className="grid grid-cols-3 gap-6">
                    <Leaderboard />
                    <div className="col-span-2">
                      <div className="glass-card p-6">
                        <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                          <TrendingUp className="text-blue-500" />
                          Performance Analytics
                        </h2>
                        {/* Charts and analytics */}
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}
              
              {activeTab === 'practice' && (
                <motion.div
                  key="practice"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <PracticeSession 
                    isActive={sessionActive}
                    time={sessionTime}
                    onStart={handleStartSession}
                    onStop={() => setSessionActive(false)}
                  />
                </motion.div>
              )}
            </AnimatePresence>
          </main>
        </div>
        
        {/* Session Timer */}
        {sessionActive && (
          <div className="fixed bottom-4 right-4 glass-card p-4 rounded-xl shadow-2xl">
            <div className="flex items-center gap-3">
              <Clock className="text-green-500 animate-pulse" />
              <div>
                <div className="text-sm text-gray-400">Practice Session</div>
                <div className="text-2xl font-mono font-bold">
                  {Math.floor((2700 - sessionTime) / 60)}:
                  {String((2700 - sessionTime) % 60).padStart(2, '0')}
                </div>
              </div>
              <button
                onClick={() => setSessionActive(false)}
                className="ml-4 px-3 py-1 bg-red-500/20 text-red-400 rounded-lg hover:bg-red-500/30"
              >
                End
              </button>
            </div>
          </div>
        )}
        
        {/* Quick Action Button */}
        <button
          onClick={() => setActiveTab('workspace')}
          className="fixed bottom-6 left-6 p-4 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full shadow-2xl hover:shadow-purple-500/30 transition-all hover:scale-110"
        >
          <Sparkles className="text-white" size={24} />
        </button>
      </div>
    </ThemeProvider>
  );
}

export default App;