# Web Deployment Guide

## Deploy to the Web (Get a Shareable Link)

### Option 1: GitHub Pages (Free)

1. Create GitHub account: https://github.com
2. Create new repository: "vegetation-management-agent"
3. Upload files to the repository
4. Go to Settings > Pages
5. Select source: "Deploy from a branch"
6. Choose branch: "main"
7. Save - get URL like: https://yourusername.github.io/vegetation-management-agent

### Option 2: Netlify Drop (Instant)

1. Go to: https://app.netlify.com/drop
2. Drag & drop the entire deployment folder
3. Get instant URL: https://random-name.netlify.app
4. Customize domain if desired

### Option 3: Vercel (Professional)

1. Go to: https://vercel.com
2. Sign up with GitHub account
3. Import repository or upload files
4. Get custom domain: https://your-project.vercel.app

### Option 4: Render (Free Backend)

1. Go to: https://render.com
2. Create new Web Service
3. Connect GitHub repository
4. Set build command: `pip install -r requirements_render.txt`
5. Set start command: `python simple_backend.py`
6. Set environment variable: `PYTHON_VERSION=3.12.0`
7. Get backend URL: https://your-service.onrender.com

## Frontend + Backend Integration

For full functionality, you need both:
- Frontend: HTML dashboard (deploy to GitHub Pages/Netlify)
- Backend: Python API (deploy to Render/Railway)

### Complete Setup Example:

1. Deploy frontend to GitHub Pages
2. Deploy backend to Render
3. Update frontend to use backend URL
4. Share the frontend URL - it will connect to your backend

## Mobile Access

Once deployed, your agent will be accessible from:
- Desktop computers
- Laptops
- Tablets
- Smartphones
- Any device with a web browser

## Security Notes

- The backend includes CORS settings for web access
- Consider adding authentication for production use
- API endpoints are designed for public access
- Monitor usage and implement rate limiting if needed

---
Your vegetation management agent will be accessible worldwide!
