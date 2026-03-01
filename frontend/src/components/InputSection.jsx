import React from 'react';
import { Send, Database, MessageSquare } from 'lucide-react';
import { motion } from 'framer-motion';

const InputSection = ({ inputText, setInputText, handleAnalyze, loadTestData, loading }) => {
    return (
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
            <div className="button-group" style={{ gap: '1rem', display: 'flex' }}>
                <button
                    className="btn-secondary"
                    onClick={loadTestData}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem',
                        background: 'rgba(255, 255, 255, 0.05)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        color: 'white',
                        padding: '0.8rem 1.5rem',
                        borderRadius: '12px',
                        cursor: 'pointer'
                    }}
                >
                    <Database size={18} />
                    Use Test Email
                </button>
                <button
                    className="btn-primary"
                    onClick={handleAnalyze}
                    disabled={loading || !inputText.trim()}
                    style={{ flex: 1 }}
                >
                    <Send size={18} />
                    {loading ? 'Analyzing with Zero-Mercy Logic...' : 'Analyze Threads'}
                </button>
            </div>
        </motion.div>
    );
};

export default InputSection;
