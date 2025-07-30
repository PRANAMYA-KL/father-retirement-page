from flask import Flask, render_template, request, redirect, jsonify, url_for
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

WISHES_FILE = "wishes.json"
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load existing wishes or start with an empty list
def load_wishes():
    if os.path.exists(WISHES_FILE):
        try:
            with open(WISHES_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:  # Check if file is not empty
                    return json.loads(content)
                else:
                    return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

# Save a new wish
def save_wish(wish):
    wishes = load_wishes()
    wishes.append(wish)
    with open(WISHES_FILE, "w", encoding="utf-8") as f:
        json.dump(wishes, f, indent=4, ensure_ascii=False)

# Delete a wish by index
def delete_wish(wish_index):
    wishes = load_wishes()
    if 0 <= wish_index < len(wishes):
        deleted_wish = wishes.pop(wish_index)
        with open(WISHES_FILE, "w", encoding="utf-8") as f:
            json.dump(wishes, f, indent=4, ensure_ascii=False)
        return True, deleted_wish
    return False, None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        wish = {
            "name": request.form["name"],
            "place": request.form["place"],
            "school": request.form["school"],
            "message": request.form["message"]
        }
        
        # Add batch if provided
        if request.form.get("batch"):
            wish["batch"] = request.form["batch"]
        
        # Handle photo upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid filename conflicts
                import time
                timestamp = str(int(time.time()))
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{timestamp}{ext}"
                
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                wish["photo"] = url_for('static', filename=f'uploads/{filename}')
        
        save_wish(wish)
        return redirect("/")
    
    wishes = load_wishes()
    return render_template("index.html", wishes=wishes)

@app.route("/delete_wish", methods=["POST"])
def delete_wish_route():
    try:
        data = request.get_json()
        wish_id = data.get("wish_id")
        
        if wish_id is not None:
            success, deleted_wish = delete_wish(wish_id)
            if success:
                return jsonify({"success": True, "message": "Wish deleted successfully"})
            else:
                return jsonify({"success": False, "message": "Wish not found"})
        else:
            return jsonify({"success": False, "message": "Invalid wish ID"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
