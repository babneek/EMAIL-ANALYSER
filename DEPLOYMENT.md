# Deployment Guide: Sales Intelligence Agent

Follow these steps to deploy your application to the cloud for free using **Render**.

## Step 1: Push to GitHub
1. Create a new repository on GitHub.
2. Push your project to GitHub:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

---

## Step 2: Deploy the Backend (API)
1. Go to [Render](https://render.com/) and log in.
2. Click **New +** > **Web Service**.
3. Connect your GitHub repository.
4. **Configuration**:
   - **Name**: `email-analytics-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.api:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**:
   - Click **Advanced** > **Add Environment Variable**:
     - `GROQ_API_KEY`: *(Your Groq API Key)*
     - `GROQ_MODEL_NAME`: `llama-3.3-70b-versatile`
6. Click **Create Web Service**.
7. **Copy the URL** (e.g., `https://email-analytics-api.onrender.com`).

---

## Step 3: Deploy the Frontend (Vite/React)
1. In Render, click **New +** > **Static Site**.
2. Connect the same GitHub repository.
3. **Configuration**:
   - **Name**: `email-analytics-dashboard`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. **Environment Variables**:
   - `VITE_API_URL`: *(The URL you copied in Step 2)*
5. Click **Create Static Site**.

---

## Step 4: Verification
- Once both are deployed, open your **Static Site URL**.
- Paste an email thread and click **Analyze Threads**.
- The frontend will now communicate with your live Groq-powered backend!
