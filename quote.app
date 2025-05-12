@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User has reached route via POST
    if request.method == "POST":
        symbolFromUser = request.form.get("symbol")
        lookedUp = lookup(symbolFromUser)

        # Check if stock exist
        if lookedUp == None:
            return apology("stock symbol does not exist")
        else:
            stock = lookedUp["name"]
            price = usd(lookedUp["price"])
            symbol = lookedUp["symbol"]
            return render_template("quoted.html", name=stock, price=price, symbol=symbol)
    else:
        return render_template("quote.html")
