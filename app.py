from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# Simple in-memory storage for ratings (in production, use a database)
ratings_data = {
    "total_ratings": 0,
    "total_score": 0,
    "average": 0,
    "ratings": []
}

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
    return render_template('message.html', title='Your Message', message=message, name=name, average_rating=ratings_data["average"], total_ratings=ratings_data["total_ratings"])

@app.route('/rate', methods=['POST'])
def submit_rating():
    """Handle rating submission"""
    try:
        rating = int(request.json.get('rating'))
        comment = request.json.get('comment', '')
        
        if 1 <= rating <= 5:
            # Add rating to storage
            ratings_data["ratings"].append({
                "rating": rating,
                "comment": comment,
                "timestamp": datetime.now().isoformat()
            })
            
            # Update totals
            ratings_data["total_ratings"] += 1
            ratings_data["total_score"] += rating
            ratings_data["average"] = round(ratings_data["total_score"] / ratings_data["total_ratings"], 1)
            
            return jsonify({
                "success": True, 
                "message": "Thanks for rating!",
                "new_average": ratings_data["average"],
                "total_ratings": ratings_data["total_ratings"]
            })
        else:
            return jsonify({"success": False, "message": "Invalid rating"})
    except Exception as e:
        return jsonify({"success": False, "message": "Error submitting rating"})

@app.route('/ratings')
def view_ratings():
    """View all ratings"""
    return render_template('ratings.html', title='All Ratings', ratings_data=ratings_data)

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
