@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check for user error
        checkUsername = db.execute("SELECT COUNT(*) FROM users WHERE username = ?", username)
        if not username:
            return apology("missing username")
        elif not password:
            return apology("missing password")
        elif not confirmation:
            return apology("missing confirmation")
        elif checkUsername[0]["COUNT(*)"] == 1:
            return apology("username already exist")
        elif password != confirmation:
            return apology("passwords doesn't match")

        # Put new user inside the database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        # Log the user in after registering
        login = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = login[0]["id"]

        return redirect("/")
    else:
        return render_template("register.html")
