@app.route("/user", methods=["GET", "POST"])
@login_required
def user():
    """Change password of user"""

    # User has reached route via POST
    if request.method == "POST":

        # Prompt user for old and new password, and confirmation
        oldPassword = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])
        currentPassword = request.form.get("current_password")
        newPassword = request.form.get("new_password")
        newConfirmation = request.form.get("new_confirmation")

        # Check for user error
        if not currentPassword or not newPassword or not newConfirmation:
            return apology("missing fields")
        elif not check_password_hash(oldPassword[0]["hash"], currentPassword):
            return apology("invalid current password")
        elif newPassword != newConfirmation:
            return apology("passwords do not match")

        # Generate new password hash
        newPasswordHash = generate_password_hash(newPassword)

        # Update password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", newPasswordHash, session["user_id"])

        flash("Password Changed!")

        return redirect("/user")
    else:
        userName = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        return render_template("user.html", userName=userName[0]["username"])
