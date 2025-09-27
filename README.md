# My Python Website

A Flask web application that showcases Python code in an interactive, shareable format.

## 🚀 Quick Start

### Local Development

1. **Install Python** (3.7 or higher)
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser** and go to: `http://localhost:5000`

## 📁 Project Structure

```
1st website/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── about.html        # About page
│   └── demo.html         # Demo page
└── static/               # Static files (CSS, JS, images)
    └── css/
        └── style.css     # Custom styles
```

## ✨ Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Demo**: Show your Python code running live
- **Easy Sharing**: Deploy and share with friends
- **Modern UI**: Clean, professional design with Bootstrap

## 🔧 Customization

### Adding Your Python Code

1. Open `app.py`
2. Find the `demo()` function
3. Replace the placeholder code with your Python logic
4. The output will be displayed on the demo page

### Styling

- Modify `static/css/style.css` for custom styles
- Edit templates in the `templates/` folder
- Bootstrap classes are available for quick styling

## 🌐 Deployment Options

### Option 1: Railway (Recommended)
1. Sign up at [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway will automatically deploy your app
4. Share the generated URL with friends

### Option 2: Heroku
1. Install Heroku CLI
2. Create a `Procfile` with: `web: gunicorn app:app`
3. Deploy using Heroku CLI commands

### Option 3: PythonAnywhere
1. Sign up for a free account at [PythonAnywhere.com](https://pythonanywhere.com)
2. Upload your files
3. Configure a web app in the dashboard

## 📱 Sharing with Friends

Once deployed, your friends can:
- Visit your website URL from any device
- No installation required - just a web browser
- Works on phones, tablets, and computers
- Share the link on social media or messaging apps

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Deployment**: Gunicorn WSGI server
- **Styling**: Bootstrap 5 + Custom CSS

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

**Made with ❤️ using Python and Flask**
