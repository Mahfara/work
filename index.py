@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get data manipulated by the user through buying and selling
    stockInfo = db.execute(
        "SELECT symbol, stock, SUM(shares) AS SHARES, price, SUM(total) AS TOTAL FROM stocks WHERE id = ? GROUP BY symbol",
        session["user_id"])

    # Get the cash of user
    leftCash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    # Get the total amount the user has spent
    totalBought = db.execute("SELECT SUM(total) FROM stocks WHERE id = ?", session["user_id"])

    # Sets the money and renders the html
    try:
        allMoney = float(leftCash[0]["cash"]) + float(totalBought[0]["SUM(total)"])
        return render_template("index.html", stocks=stockInfo, cash=usd(leftCash[0]["cash"]), totalMoney=usd(allMoney))
    except TypeError:
        allMoney = 10000.00
        return render_template("index.html", stocks=stockInfo, cash=usd(leftCash[0]["cash"]), totalMoney=usd(allMoney))
