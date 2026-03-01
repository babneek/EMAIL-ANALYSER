import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const analyzeEmails = async (emailsText) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/analyze`, {
            emails_text: emailsText
        });
        return response.data;
    } catch (error) {
        throw error.response?.data?.detail || 'An unexpected error occurred. Please ensure the backend is running.';
    }
};
