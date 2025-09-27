from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from datetime import datetime

# Rating system added - Force redeploy
app = Flask(__name__)

# Simple in-memory storage for ratings (in production, use a database)
ratings_data = {
    "total_ratings": 0,
    "total_score": 0,
    "average": 0,
    "ratings": []
}

# Visitor tracking storage
visitors_data = {
    "total_visitors": 0,
    "unique_visitors": set(),
    "visitor_log": [],
    "roast_count": 0
}

@app.route('/')
def home():
    """Home page route - asks for user's name"""
    # Track visitor
    visitor_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Log the visit
    visit_info = {
        "ip": visitor_ip,
        "user_agent": user_agent,
        "timestamp": datetime.now().isoformat(),
        "page": "home"
    }
    visitors_data["visitor_log"].append(visit_info)
    
    # Count unique visitors
    if visitor_ip not in visitors_data["unique_visitors"]:
        visitors_data["unique_visitors"].add(visitor_ip)
    
    visitors_data["total_visitors"] += 1
    
    return render_template('index.html', title='Enter Your Name')

@app.route('/submit', methods=['POST'])
def submit_name():
    """Handle name submission"""
    user_name = request.form.get('name')
    if user_name:
        # Blocked names - protect the creator! 
        blocked_names = [
            'sagar', 'rathore', 'sagar rathore', 'sagarrathore',
            'SAGAR', 'RATHORE', 'SAGAR RATHORE', 'SAGARRATHORE',
            'Sagar', 'Rathore', 'Sagar Rathore', 'SagarRathore'
        ]
        
        # Check if the name contains any blocked terms
        user_name_lower = user_name.lower().strip()
        for blocked in blocked_names:
            if blocked.lower() in user_name_lower:
                return render_template('blocked.html', title='Access Denied', attempted_name=user_name)
        
        return redirect(url_for('show_message', name=user_name))
    return redirect(url_for('home'))

@app.route('/message/<name>')
def show_message(name):
    """Show the message with user's name"""
    # Track roasting event
    visitor_ip = request.remote_addr
    roast_info = {
        "ip": visitor_ip,
        "name": name,
        "timestamp": datetime.now().isoformat()
    }
    visitors_data["visitor_log"].append({**roast_info, "page": "roast"})
    visitors_data["roast_count"] += 1
    
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

@app.route('/visitors')
def view_visitors():
    """View visitor statistics - Admin only"""
    # Convert set to list for template rendering
    unique_count = len(visitors_data["unique_visitors"])
    
    # Get recent visitors (last 50)
    recent_visitors = visitors_data["visitor_log"][-50:]
    
    stats = {
        "total_visits": visitors_data["total_visitors"],
        "unique_visitors": unique_count,
        "total_roasts": visitors_data["roast_count"],
        "recent_visitors": recent_visitors
    }
    
    return render_template('visitors.html', title='Visitor Stats', stats=stats)

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
