import React from 'react';
import { Download, Clock, TrendingUp, TrendingDown, Minus, CheckCircle2, ShieldAlert, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';

const ResultsSection = ({ results, downloadCSV }) => {
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
                    <div className="stat-value">Llama-3.1 8B</div>
                    <div className="stat-label">Model Engine</div>
                </div>
            </div>

            <div className="glass-card">
                <div className="action-bar" style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '1.5rem' }}>
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
    );
};

export default ResultsSection;
