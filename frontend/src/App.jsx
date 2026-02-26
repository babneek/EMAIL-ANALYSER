import React, { useState } from 'react';
import axios from 'axios';
import {
  Send,
  Download,
  ShieldAlert,
  CheckCircle2,
  TrendingUp,
  TrendingDown,
  Minus,
  AlertCircle,
  Clock,
  MessageSquare,
  Database
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const App = () => {
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const loadTestData = () => {
    const testData = `From: Sarah Chen <s.chen@globaltech.com>
To: Mark Stevens <mark.s@cloudsolutions.io>
Subject: Security and Pricing for Enterprise Migration

Hi Mark,

Thanks for the demo earlier today. We are interested in moving forward with CloudSolutions, but my procurement team has a few non-negotiable requirements before we sign:

1. We need a formal SOC2 Type II report for our audit. Can you send that over?
2. We have 1,200 employees. What is the volume discount for a team of this size?
3. We require data residency in Singapore (APAC). Is your local server cluster ready for this?
4. Do you offer 24/7 phone support, or is it just the ticket system?

Looking forward to your quick response.

Best,
Sarah
---
From: Mark Stevens <mark.s@cloudsolutions.io>
To: Sarah Chen <s.chen@globaltech.com>
Subject: Re: Security and Pricing for Enterprise Migration

Hi Sarah!

Great hearing from you. I’m so glad the team loved the demo. 

Regarding your questions—we have a fantastic per-user price of $18/month, which is a great deal compared to the competition. We also have a very robust security framework that meets most global standards. 

I’ll check with my manager on the other details, but I’m ready to send the contract today so we can hit your Q1 deadline. Would you like me to send the Docusign now?

Best,
Mark`;
    setInputText(testData);
  };

  const handleAnalyze = async () => {
    if (!inputText.trim()) return;

    setLoading(true);
    setResults(null);
    setError(null);

    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    try {
      const response = await axios.post(`${API_URL}/analyze`, {
        emails_text: inputText
      });
      setResults(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'An unexpected error occurred. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const downloadCSV = () => {
    if (!results?.csv) return;
    const blob = new Blob([results.csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'sales_intelligence_report.csv';
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const getRiskBadge = (risk) => {
    const riskLower = risk?.toLowerCase();
    if (riskLower === 'high') return <span className="badge badge-high">High Risk</span>;
    if (riskLower === 'medium') return <span className="badge badge-medium">Medium Risk</span>;
    return <span className="badge badge-low">Low Risk</span>;
  };

  const getSentimentIcon = (sentiment) => {
    const s = sentiment?.toLowerCase();
    if (s === 'positive') return <CheckCircle2 className="text-success" size={16} />;
    if (s === 'negative') return <ShieldAlert className="text-error" size={16} />;
    return <AlertCircle className="text-secondary" size={16} />;
  };

  const getTrendIcon = (trend) => {
    const t = trend?.toLowerCase();
    if (t === 'improving') return <TrendingUp className="text-success" size={16} />;
    if (t === 'declining') return <TrendingDown className="text-error" size={16} />;
    return <Minus className="text-secondary" size={16} />;
  };

  return (
    <div className="app-container">
      <header className="header">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          SimplAI Intelligence Agent
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          High-Reasoning Sales Email Analytics Dashboard
        </motion.p>
      </header>

      <main>
        <motion.div
          className="glass-card input-section"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <div className="input-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <MessageSquare size={20} className="text-accent" />
              Input Conversations
            </h3>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Supports JSON or Raw Text</span>
          </div>
          <textarea
            placeholder="Paste your email conversation data here (e.g., from sample_emails.json or copy-pasted text)..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
          <div className="button-group" style={{ gap: '1rem' }}>
            <button
              className="btn-secondary"
              onClick={loadTestData}
              style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', color: 'white', padding: '0.8rem 1.5rem', borderRadius: '12px', cursor: 'pointer' }}
            >
              <Database size={18} />
              Use Test Email
            </button>
            <button
              className="btn-primary"
              onClick={handleAnalyze}
              disabled={loading || !inputText.trim()}
            >
              <Send size={18} />
              {loading ? 'Analyzing with Zero-Mercy Logic...' : 'Analyze Threads'}
            </button>
          </div>
        </motion.div>

        {error && (
          <motion.div
            className="glass-card"
            style={{ borderColor: 'var(--error-color)', marginBottom: '2rem', padding: '1rem' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <p style={{ color: 'var(--error-color)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <AlertCircle size={18} />
              {error}
            </p>
          </motion.div>
        )}

        <AnimatePresence>
          {loading && (
            <motion.div
              className="glass-card loading-overlay"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <div className="spinner"></div>
              <p>Performing "Zero-Mercy" gap analysis on your threads...</p>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Identifying requirements and sales rep performance gaps</p>
            </motion.div>
          )}

          {results && (
            <motion.div
              className="results-section"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-value">{results.threads.length}</div>
                  <div className="stat-label">Identified Threads</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{results.analysis.length}</div>
                  <div className="stat-label">Analyzed Reports</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">Groq Llama 3.3</div>
                  <div className="stat-label">Intelligence Model</div>
                </div>
              </div>

              <div className="glass-card">
                <div className="action-bar">
                  <button className="btn-primary" onClick={downloadCSV}>
                    <Download size={18} />
                    Download CSV Report
                  </button>
                </div>

                <div className="table-container">
                  <table>
                    <thead>
                      <tr>
                        <th>Topic</th>
                        <th>Sentiment</th>
                        <th>Risk</th>
                        <th>Key Gaps Identified</th>
                        <th>Next Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {results.analysis.map((thread, idx) => (
                        <tr key={idx}>
                          <td>
                            <div style={{ fontWeight: 600 }}>{thread.thread_topic}</div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                              <Clock size={12} /> {thread.last_updated?.split('T')[0]}
                            </div>
                          </td>
                          <td>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                              {getSentimentIcon(thread.overall_sentiment)}
                              {getTrendIcon(thread.sentiment_trend)}
                            </div>
                          </td>
                          <td>{getRiskBadge(thread.risk_level)}</td>
                          <td style={{ maxWidth: '300px' }}>
                            <div style={{ fontSize: '0.85rem' }}>
                              {thread.sales_rep_gaps.split(';').map((gap, i) => (
                                <div key={i} style={{ marginBottom: '0.25rem' }}>• {gap.trim()}</div>
                              ))}
                            </div>
                          </td>
                          <td>
                            <div style={{ fontSize: '0.85rem', color: 'var(--accent-color)', fontWeight: 500 }}>
                              {thread.recommended_next_action}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <footer style={{ marginTop: '4rem', textAlign: 'center', color: 'var(--text-secondary)', fontSize: '0.9rem', paddingBottom: '2rem' }}>
        SimplAI Intelligence Systems &copy; 2026 | Built for High-Scale Sales Operations
      </footer>

      <style jsx>{`
        .text-success { color: #10b981; }
        .text-error { color: #ef4444; }
        .text-secondary { color: #94a3b8; }
        .text-accent { color: #3b82f6; }
      `}</style>
    </div>
  );
};

export default App;
