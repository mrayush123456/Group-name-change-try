from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagrapi import Client

app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Auto Comment</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333333;
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
            color: #333333;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #007bff;
            color: #ffffff;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Auto Comment</h1>
        <form action="/" method="POST">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="post_url">Target Post URL:</label>
            <input type="text" id="post_url" name="post_url" placeholder="Enter target post URL" required>

            <label for="comment">Comment:</label>
            <input type="text" id="comment" name="comment" placeholder="Enter your comment" required>

            <button type="submit">Send Comment</button>
        </form>
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def auto_comment():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        post_url = request.form["post_url"]
        comment = request.form["comment"]

        try:
            # Instagram Login
            cl = Client()
            print("[INFO] Logging in...")
            cl.login(username, password)
            print("[SUCCESS] Logged in!")

            # Extract Post Media ID from URL
            media_id = cl.media_id(cl.media_pk_from_url(post_url))
            print(f"[INFO] Media ID fetched: {media_id}")

            # Send Comment
            cl.media_comment(media_id, comment)
            print(f"[SUCCESS] Comment sent: {comment}")

            flash("Comment sent successfully!", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "error")

        return redirect(url_for("auto_comment"))

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
