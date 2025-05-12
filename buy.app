@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST
    if request.method == "POST":

        # Put input of user in variables
        buySymbol = request.form.get("symbol")
        buyShares = request.form.get("shares")

        # Use the lookup() function
        buyLookedUp = lookup(buySymbol)

        # Check for user error
        if not buySymbol:
            return apology("missing symbol")
        elif buyLookedUp == None:
            return apology("invalid symbol")
        elif not buyShares:
            return apology("missing shares")
        elif not buyShares.isdigit():
            return apology("invalid shares")

        buyShares = int(buyShares)
        if buyShares <= 0:
            return apology("invalid shares")

        # Set important data to variables
        buyerId = db.execute("SELECT id FROM users WHERE id = ?", session["user_id"])
        buyStock = buyLookedUp["name"]
        buyPrice = buyLookedUp["price"]
        buyTime = datetime.now()

        # Calculate total money spent and set cash of user in a variable
        totalBuyPrice = buyShares * buyPrice
        cashOfBuyer = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        # Check if user can afford the stock
        if cashOfBuyer[0]["cash"] < totalBuyPrice:
            return apology("can't afford")
        else:
            remainingCash = int(cashOfBuyer[0]["cash"]) - totalBuyPrice

            # Update database
            db.execute("INSERT INTO stocks (id, stock, symbol, shares, price, total, time) VALUES(?, ?, ?, ?, ?, ?, ?)",
                       buyerId[0]["id"], buyStock, buySymbol, buyShares, buyPrice, totalBuyPrice, buyTime)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", remainingCash, buyerId[0]["id"])
            db.execute("UPDATE stocks SET symbol = UPPER(symbol)")

            flash("Bought!")

            return redirect("/")
    else:
        return render_template("buy.html")
