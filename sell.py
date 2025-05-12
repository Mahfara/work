@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User has reached route via POST
    if request.method == "POST":
        sellSymbol = request.form.get("symbol")
        sellShares = request.form.get("shares")

        sellLookedUp = lookup(sellSymbol)

        # Get number of shares user has
        shareAmount = db.execute("SELECT SUM(shares) FROM stocks WHERE id = ? AND symbol = ?", session["user_id"], sellSymbol)

        # Check for user error
        if not sellSymbol:
            return apology("missing symbol")
        elif sellLookedUp == None:
            return apology("invalid symbol")
        elif not sellShares:
            return apology("missing shares")
        elif not sellShares.isdigit():
            return apology("invalid shares")

        sellShares = int(sellShares)
        if sellShares <= 0 or sellShares > shareAmount[0]["SUM(shares)"]:
            return apology("invalid shares")

        # Set important data to variables
        sellerId = db.execute("SELECT id FROM users WHERE id = ?", session["user_id"])
        sellStock = sellLookedUp["name"]
        sellPrice = sellLookedUp["price"]
        totalSellPrice = sellShares * sellPrice
        sellShares = -abs(sellShares)
        sellTime = datetime.now()

        # Calculate the amount of money returned to user
        cashOfSeller = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        remainingCash = int(cashOfSeller[0]["cash"]) + totalSellPrice
        totalSellPrice = -abs(totalSellPrice)

        # Update database
        db.execute("INSERT INTO stocks (id, stock, symbol, shares, price, total, time) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   sellerId[0]["id"], sellStock, sellSymbol, sellShares, sellPrice, totalSellPrice, sellTime)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", remainingCash, sellerId[0]["id"])
        db.execute("UPDATE stocks SET symbol = UPPER(symbol)")

        flash("Sold!")

        return redirect("/")
    else:
        symbols = db.execute("SELECT SUM(shares) AS SHARES, symbol FROM stocks WHERE id = ? GROUP BY symbol", session["user_id"])
        return render_template("sell.html", symbols=symbols)
