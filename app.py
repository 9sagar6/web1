from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def home():
    """Home page route - asks for user's name"""
    return render_template('index.html', title='Enter Your Name')

@app.route('/submit', methods=['POST'])
def submit_name():
    """Handle name submission"""
    user_name = request.form.get('name')
    if user_name:
        return redirect(url_for('show_message', name=user_name))
    return redirect(url_for('home'))

@app.route('/message/<name>')
def show_message(name):
    """Show the message with user's name"""
    message = f"FUCK YOU {name.upper()}!"
    return render_template('message.html', title='Your Message', message=message, name=name)

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html', title='About - My Python Website')

@app.route('/demo')
def demo():
    """Demo page showing your Python code functionality"""
    # Your Python code logic will go here
    result = "Hello from Python! This is where your code output will be displayed."
    return render_template('demo.html', title='Demo - My Python Website', result=result)

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
