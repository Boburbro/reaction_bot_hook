from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from scr.database.database import Database

index = Blueprint('index', __name__, template_folder='../templates')

@index.route("/")
@login_required
def home():
    db = Database()
    print(db.is_initialized())
    if not db.is_initialized(): db.init_database()

    bots_count = len(db.fetch_bots())
    recent_activities = db.get_recent_activities(limit=100)
    
    # Format timestamps for display
    for activity in recent_activities:
        if isinstance(activity['timestamp'], str):
            # If it's already a string, leave it as is
            pass
        else:
            # Convert datetime to string format
            activity['timestamp'] = activity['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template("index.html", bots_count=bots_count, recent_activities=recent_activities)

@index.route("/api/activities", methods=["GET"])
@login_required
def get_activities():
    db = Database()
    limit = request.args.get('limit', default=100, type=int)
    activities = db.get_recent_activities(limit=limit)
    
    # Format timestamps for JSON response
    for activity in activities:
        if isinstance(activity['timestamp'], str):
            # If it's already a string, leave it as is
            pass
        else:
            # Convert datetime to string format
            activity['timestamp'] = activity['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    
    return jsonify({"success": True, "activities": activities})

@index.route("/api/activities", methods=["POST"])
@login_required
def add_activity():
    db = Database()
    data = request.json
    
    if not data or 'activity_type' not in data or 'description' not in data:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    
    # Get client information
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    username = current_user.username if current_user else None
    
    result = db.add_activity_log(
        activity_type=data['activity_type'],
        description=data['description'],
        ip_address=ip_address,
        user_agent=user_agent,
        username=username
    )
    
    if result:
        return jsonify({"success": True, "message": "Activity log added successfully"})
    else:
        return jsonify({"success": False, "message": "Failed to add activity log"}), 500

