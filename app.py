from flask import Flask, render_template, request
import hashlib
import requests
import zxcvbn

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        password = request.form.get("password", "")
        
        # 1. Local Mathematical Entropy & Pattern Check (zxcvbn)
        analysis = zxcvbn.zxcvbn(password)
        score = analysis['score'] # Score ranges from 0 (weak) to 4 (strong)
        crack_time = analysis['crack_times_display']['offline_slow_hashing_1e4_per_second']
        feedback = analysis['feedback']['warning'] or "No structural weaknesses detected."
        suggestions = analysis['feedback']['suggestions']

        # 2. Zero-Knowledge K-Anonymity Breach Check
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]
        
        breach_count = 0
        try:
            # We only send the first 5 characters (prefix) to protect user privacy
            response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
            if response.status_code == 200:
                lines = response.text.splitlines()
                for line in lines:
                    parts = line.split(':')
                    if parts[0] == suffix:
                        breach_count = int(parts[1])
                        break
        except Exception:
            breach_count = -1  # API failure indicator

        result = {
            "password": password,
            "score": score,
            "crack_time": crack_time,
            "feedback": feedback,
            "suggestions": suggestions,
            "breach_count": breach_count
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)