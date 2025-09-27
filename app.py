from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from datetime import datetime
import re

# Rating system added - Force redeploy
app = Flask(__name__)

# Comprehensive profanity filter - English and Hindi
BLOCKED_WORDS = [
    # English profanity
    'fuck', 'shit', 'bitch', 'asshole', 'damn', 'crap', 'bastard', 'hell',
    'piss', 'cock', 'dick', 'pussy', 'whore', 'slut', 'fag', 'nigga', 'nigger',
    # Hindi/Urdu profanity  
    'chutiya', 'madarchod', 'bhenchod', 'bhosdike', 'randi', 'saala', 'saali',
    'kamina', 'harami', 'kutte', 'kutta', 'gandu', 'lawda', 'lund', 'gaand',
    'chodu', 'bhosda', 'behen', 'maa', 'baap', 'teri', 'chut', 'loda',
    # Common variations and leetspeak
    'f*ck', 'sh*t', 'b*tch', 'a$$hole', 'fuk', 'fck', 'sht', 'btch',
    'chutiy@', 'ch0du', 'g@ndu', 'b3nch0d', 'madarch0d',
    # Mild but inappropriate
    'stupid', 'idiot', 'moron', 'dumb', 'ugly', 'fat', 'gay',
    # Your name variations (ULTRA PROTECTION)
    'sagar', 'rathore', 'sagarrathore', 's4g4r', 'r4th0r3', 'r47h0r3'
]

def contains_profanity(text):
    """Advanced AI profanity detection"""
    if not text:
        return False
    
    text_lower = text.lower()
    # Remove special characters for checking
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text_lower)
    
    # Convert leetspeak to normal letters
    leetspeak_text = text_lower.replace('@', 'a').replace('$', 's').replace('4', 'a').replace('0', 'o').replace('3', 'e').replace('1', 'i').replace('7', 't')
    leetspeak_clean = re.sub(r'[^a-zA-Z0-9\s]', '', leetspeak_text)
    
    for word in BLOCKED_WORDS:
        if (word in text_lower or word in clean_text or 
            word in leetspeak_text or word in leetspeak_clean):
            return True
    return False

def contains_profanity_excluding_creator(text):
    """Profanity detection that excludes creator names"""
    if not text:
        return False
    
    # Creator names that should NOT be flagged as profanity
    creator_names = ['sagar', 'rathore', 'sagarrathore', 's4g4r', 'r4th0r3', 'r47h0r3']
    
    # Create a filtered blocked words list (excluding creator names)
    filtered_blocked_words = [word for word in BLOCKED_WORDS if word not in creator_names]
    
    text_lower = text.lower()
    # Remove special characters for checking
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text_lower)
    
    # Convert leetspeak to normal letters
    leetspeak_text = text_lower.replace('@', 'a').replace('$', 's').replace('4', 'a').replace('0', 'o').replace('3', 'e').replace('1', 'i').replace('7', 't')
    leetspeak_clean = re.sub(r'[^a-zA-Z0-9\s]', '', leetspeak_text)
    
    for word in filtered_blocked_words:
        if (word in text_lower or word in clean_text or 
            word in leetspeak_text or word in leetspeak_clean):
            return True
    return False

def is_spam_comment(comment, ip):
    """Detect spam comments"""
    if not comment:
        return False
    
    comment_lower = comment.lower().strip()
    
    # Check for spam patterns
    spam_patterns = [
        r'(.)\1{4,}',  # Repeated characters (aaaaa, 11111)
        r'[!@#$%^&*]{3,}',  # Multiple special characters
        r'\b(click|buy|free|win|money|prize|offer)\b',  # Spam keywords
        r'http[s]?://\S+',  # URLs
        r'\b\w*(.com|.net|.org)\b'  # Domain names
    ]
    
    for pattern in spam_patterns:
        if re.search(pattern, comment_lower):
            return True
    
    # Check for repetitive short comments
    if len(comment.strip()) < 3:
        return True
        
    # Check if comment is just repeated words
    words = comment_lower.split()
    if len(words) > 2 and len(set(words)) == 1:  # All words are the same
        return True
    
    return False

def has_user_commented(ip):
    """Check if IP has already commented"""
    for rating in ratings_data["ratings"]:
        if rating.get("ip") == ip:
            return True
    return False

# Simple in-memory storage for ratings (in production, use a database)
ratings_data = {
    "total_ratings": 0,
    "total_score": 0,
    "average": 0,
    "ratings": [],
    "blocked_attempts": [],  # Store blocked profanity attempts
    "spam_attempts": [],     # Store spam attempts
    "duplicate_attempts": []  # Store duplicate comment attempts
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
    """Handle name submission with ULTRA AI PROTECTION"""
    user_name = request.form.get('name')
    if user_name:
        # FIRST: Check for creator name protection (BEFORE profanity check!)
        blocked_names = [
            'sagar', 'rathore', 'sagar rathore', 'sagarrathore',
            'SAGAR', 'RATHORE', 'SAGAR RATHORE', 'SAGARRATHORE',
            'Sagar', 'Rathore', 'Sagar Rathore', 'SagarRathore'
        ]
        
        # Remove ALL special characters, spaces, and numbers for ultra-smart checking
        clean_name = re.sub(r'[^a-zA-Z]', '', user_name.lower())
        user_name_lower = user_name.lower().strip()
        
        # Also check for leetspeak replacements
        leetspeak_clean = user_name_lower.replace('@', 'a').replace('$', 's').replace('4', 'a').replace('0', 'o').replace('3', 'e').replace('1', 'i').replace('7', 't')
        leetspeak_clean = re.sub(r'[^a-zA-Z]', '', leetspeak_clean)
        
        # Check original name, cleaned name, AND leetspeak version
        for blocked in blocked_names:
            blocked_clean = re.sub(r'[^a-zA-Z]', '', blocked.lower())
            if (blocked.lower() in user_name_lower or 
                blocked_clean in clean_name or
                blocked.lower() in clean_name or
                blocked_clean in leetspeak_clean or
                blocked.lower() in leetspeak_clean):
                return render_template('blocked.html', title='Access Denied', attempted_name=user_name, reason="creator_protection")
        
        # SECOND: Check for profanity AFTER name protection (excluding creator names)
        if contains_profanity_excluding_creator(user_name):
            blocked_attempt = {
                "name": user_name,
                "ip": request.remote_addr,
                "timestamp": datetime.now().isoformat(),
                "reason": "profanity_in_name"
            }
            ratings_data["blocked_attempts"].append(blocked_attempt)
            return render_template('blocked.html', title='Name Blocked', attempted_name=user_name, reason="profanity")
        
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
    """Handle rating submission with ULTIMATE PROTECTION"""
    try:
        rating = int(request.json.get('rating'))
        comment = request.json.get('comment', '')
        user_ip = request.remote_addr
        
        if 1 <= rating <= 5:
            # Check if user has already commented (ONE COMMENT PER PERSON!)
            if has_user_commented(user_ip):
                duplicate_attempt = {
                    "comment": comment,
                    "ip": user_ip,
                    "timestamp": datetime.now().isoformat(),
                    "rating": rating
                }
                ratings_data["duplicate_attempts"].append(duplicate_attempt)
                
                return jsonify({
                    "success": False, 
                    "message": "🚫 One comment per person only! You've already rated! 🛡️",
                    "duplicate": True
                })
            
            # Check for spam comments
            if comment and is_spam_comment(comment, user_ip):
                spam_attempt = {
                    "comment": comment,
                    "ip": user_ip,
                    "timestamp": datetime.now().isoformat(),
                    "rating": rating,
                    "reason": "spam_detected"
                }
                ratings_data["spam_attempts"].append(spam_attempt)
                
                return jsonify({
                    "success": False, 
                    "message": "🚫 Spam detected! Keep it real and meaningful! 🤖",
                    "spam": True
                })
            
            # Check for profanity in comment (ENHANCED)
            if comment and contains_profanity(comment):
                # Log the blocked attempt
                blocked_attempt = {
                    "comment": comment,
                    "ip": user_ip,
                    "timestamp": datetime.now().isoformat(),
                    "rating": rating,
                    "reason": "profanity"
                }
                ratings_data["blocked_attempts"].append(blocked_attempt)
                
                return jsonify({
                    "success": False, 
                    "message": "❌ Bad language detected! AI blocked your comment! Keep it clean! 🧼🤖",
                    "blocked": True
                })
            
            # Add rating to storage (clean comment or no comment)
            ratings_data["ratings"].append({
                "rating": rating,
                "comment": comment,
                "timestamp": datetime.now().isoformat(),
                "ip": user_ip,
                "id": len(ratings_data["ratings"]) + 1  # Simple ID for deletion
            })
            
            # Update totals
            ratings_data["total_ratings"] += 1
            ratings_data["total_score"] += rating
            ratings_data["average"] = round(ratings_data["total_score"] / ratings_data["total_ratings"], 1)
            
            return jsonify({
                "success": True, 
                "message": "Thanks for your rating! ⭐ (Protected by AI)",
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

@app.route('/delete_comment', methods=['POST'])
def delete_comment():
    """Delete a comment by ID - Admin only"""
    try:
        comment_id = int(request.json.get('comment_id'))
        
        # Find and remove the comment
        for i, rating in enumerate(ratings_data["ratings"]):
            if rating.get("id") == comment_id:
                # Adjust totals
                ratings_data["total_ratings"] -= 1
                ratings_data["total_score"] -= rating["rating"]
                ratings_data["average"] = round(ratings_data["total_score"] / ratings_data["total_ratings"], 1) if ratings_data["total_ratings"] > 0 else 0
                
                # Remove the rating
                del ratings_data["ratings"][i]
                
                return jsonify({"success": True, "message": "Comment deleted!"})
        
        return jsonify({"success": False, "message": "Comment not found"})
    except Exception as e:
        return jsonify({"success": False, "message": "Error deleting comment"})

@app.route('/blocked_comments')
def view_blocked_comments():
    """View all blocked attempts - Admin only"""
    all_blocks = {
        "profanity": ratings_data["blocked_attempts"],
        "spam": ratings_data["spam_attempts"], 
        "duplicates": ratings_data["duplicate_attempts"]
    }
    return render_template('blocked.html', 
                         title='All Blocked Attempts', 
                         blocked_data=all_blocks,
                         show_admin_panel=True)

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
