import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

import { analyzeEmails } from './services/api';
import InputSection from './components/InputSection';
import ResultsSection from './components/ResultsSection';

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

    try {
      const data = await analyzeEmails(inputText);
      setResults(data);
    } catch (err) {
      console.error(err);
      setError(err);
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
        <InputSection
          inputText={inputText}
          setInputText={setInputText}
          handleAnalyze={handleAnalyze}
          loadTestData={loadTestData}
          loading={loading}
        />

        {error && (
          <motion.div
            className="glass-card"
            style={{ borderColor: '#ef4444', marginBottom: '2rem', padding: '1rem' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <p style={{ color: '#ef4444', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
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
              <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Identifying requirements and sales rep performance gaps</p>
            </motion.div>
          )}

          {results && !loading && (
            <ResultsSection
              results={results}
              downloadCSV={downloadCSV}
            />
          )}
        </AnimatePresence>
      </main>

      <footer style={{ marginTop: '4rem', textAlign: 'center', color: '#94a3b8', fontSize: '0.9rem', paddingBottom: '2rem' }}>
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
