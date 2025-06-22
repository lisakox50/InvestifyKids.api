import streamlit as st
from datetime import datetime

# -------------- Initialize session state ----------------

def init_state():
    if "registered" not in st.session_state:
        st.session_state.registered = False
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "role" not in st.session_state:
        st.session_state.role = ""
    if "cash" not in st.session_state:
        st.session_state.cash = 10000.0  # Starting cash
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = {}  # symbol -> {"shares": int, "avg_price": float}
    if "transactions" not in st.session_state:
        st.session_state.transactions = []  # list of dict with buy/sell history
    if "quests" not in st.session_state:
        st.session_state.quests = {
            "register": False,
            "buy_stock": False,
            "learn_terms": False,
            "check_price": False,
        }

init_state()

# ---------------- Mock data -----------------

FINANCIAL_TERMS = {
    "stock": "A stock is a share representing ownership in a company.",
    "bond": "A bond is a loan made by an investor to a borrower such as a company or government.",
    "fintech": "Fintech means innovations in financial technology improving services.",
    "dividend": "A dividend is a company's payment to shareholders from profits.",
    "portfolio": "A portfolio is a collection of investments owned by an investor.",
}

MOCK_STOCK_PRICES = {
    "AAPL": 150.12,
    "TSLA": 700.45,
    "GOOG": 2800.99,
    "MSFT": 305.22,
    "AMZN": 3500.50,
}

# -------------- Functions -------------------

def register_user(name: str, role: str):
    st.session_state.name = name.strip()
    st.session_state.role = role
    st.session_state.registered = True
    st.session_state.quests["register"] = True
    st.success(f"Welcome, {st.session_state.name}! You are registered as a {st.session_state.role}.")

def explain_term(term: str) -> str:
    explanation = FINANCIAL_TERMS.get(term.lower())
    if explanation:
        st.session_state.quests["learn_terms"] = True
        return explanation
    return "Sorry, no explanation found for this term."

def get_stock_price(symbol: str):
    return MOCK_STOCK_PRICES.get(symbol.upper())

def buy_stock(symbol: str, shares: int):
    symbol = symbol.upper()
    price = get_stock_price(symbol)
    if price is None:
        return False, "Stock symbol not found."
    cost = shares * price
    if cost > st.session_state.cash:
        return False, f"Insufficient funds: Need ${cost:.2f}, but you have ${st.session_state.cash:.2f}."
    # Update portfolio
    if symbol in st.session_state.portfolio:
        current = st.session_state.portfolio[symbol]
        total_shares = current["shares"] + shares
        avg_price = ((current["avg_price"] * current["shares"]) + cost) / total_shares
        st.session_state.portfolio[symbol] = {"shares": total_shares, "avg_price": avg_price}
    else:
        st.session_state.portfolio[symbol] = {"shares": shares, "avg_price": price}
    st.session_state.cash -= cost
    # Record transaction
    st.session_state.transactions.append({
        "type": "buy",
        "symbol": symbol,
        "shares": shares,
        "price": price,
        "total": cost,
        "datetime": datetime.now(),
    })
    st.session_state.quests["buy_stock"] = True
    return True, f"Bought {shares} shares of {symbol} at ${price:.2f} each for ${cost:.2f}."

def sell_stock(symbol: str, shares: int):
    symbol = symbol.upper()
    if symbol not in st.session_state.portfolio:
        return False, "You do not own this stock."
    current = st.session_state.portfolio[symbol]
    if shares > current["shares"]:
        return False, f"You only own {current['shares']} shares."
    price = get_stock_price(symbol)
    if price is None:
        return False, "Cannot get current stock price."
    revenue = shares * price
    current["shares"] -= shares
    if current["shares"] == 0:
        del st.session_state.portfolio[symbol]
    else:
        st.session_state.portfolio[symbol] = current
    st.session_state.cash += revenue
    # Record transaction
    st.session_state.transactions.append({
        "type": "sell",
        "symbol": symbol,
        "shares": shares,
        "price": price,
        "total": revenue,
        "datetime": datetime.now(),
    })
    return True, f"Sold {shares} shares of {symbol} at ${price:.2f} each for ${revenue:.2f}."

def portfolio_summary():
    total_value = 0.0
    lines = []
    for symbol, data in st.session_state.portfolio.items():
        price = get_stock_price(symbol)
        value = price * data["shares"] if price else 0.0
        total_value += value
        lines.append(f"{symbol}: {data['shares']} shares, Avg Price: ${data['avg_price']:.2f}, Current Price: ${price if price else 'N/A'}, Value: ${value:.2f}")
    return lines, total_value

def display_transactions():
    if not st.session_state.transactions:
        st.write("No transactions yet.")
        return
    for tx in reversed(st.session_state.transactions[-10:]):
        time_str = tx["datetime"].strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"{time_str}: {tx['type'].capitalize()} {tx['shares']} shares of {tx['symbol']} at ${tx['price']:.2f} totaling ${tx['total']:.2f}")

def show_quests():
    quests = {
        "register": "Complete Registration",
        "buy_stock": "Buy your first stock",
        "learn_terms": "Learn financial terms",
        "check_price": "Check stock price",
    }
    for key, desc in quests.items():
        status = "✅ Completed" if st.session_state.quests.get(key) else "❌ Incomplete"
        st.write(f"{desc}: {status}")

# ---------------- UI ----------------------

st.title("InvestifyKids - FinTech Learning & Portfolio Manager")

if not st.session_state.registered:
    st.header("Register")
    name = st.text_input("Enter your name")
    role = st.selectbox("Select your role", ["Child", "Parent"])
    if st.button("Register"):
        if name.strip() == "":
            st.error("Please enter your name.")
        else:
            register_user(name, role)
else:
    st.sidebar.write(f"👋 Hello, {st.session_state.name} ({st.session_state.role})")
    st.sidebar.write(f"💵 Cash Balance: ${st.session_state.cash:.2f}")

    st.header("Learn Financial Terms")
    term = st.text_input("Enter financial term")
    if st.button("Explain Term"):
        explanation = explain_term(term)
        st.info(explanation)

    st.header("Check Stock Price")
    symbol = st.text_input("Enter stock symbol (e.g. AAPL)")
    if st.button("Check Price"):
        price = get_stock_price(symbol)
        if price:
            st.success(f"Current price of {symbol.upper()} is ${price:.2f}")
            st.session_state.quests["check_price"] = True
        else:
            st.error("Stock symbol not found.")

    st.header("Buy Stocks")
    buy_symbol = st.text_input("Stock symbol to buy", key="buy_symbol")
    buy_shares = st.number_input("Number of shares", min_value=1, step=1, key="buy_shares")
    if st.button("Buy"):
        if buy_symbol.strip() == "":
            st.error("Please enter a stock symbol.")
        else:
            success, message = buy_stock(buy_symbol, buy_shares)
            if success:
                st.success(message)
            else:
                st.error(message)

    st.header("Sell Stocks")
    sell_symbol = st.text_input("Stock symbol to sell", key="sell_symbol")
    sell_shares = st.number_input("Number of shares to sell", min_value=1, step=1, key="sell_shares")
    if st.button("Sell"):
        if sell_symbol.strip() == "":
            st.error("Please enter a stock symbol.")
        else:
            success, message = sell_stock(sell_symbol, sell_shares)
            if success:
                st.success(message)
            else:
                st.error(message)

    st.header("Portfolio Summary")
    if not st.session_state.portfolio:
        st.write("Your portfolio is empty.")
    else:
        lines, total_value = portfolio_summary()
        for line in lines:
            st.write(line)
        st.write(f"Total portfolio value: ${total_value:.2f}")
        st.write(f"Available cash: ${st.session_state.cash:.2f}")

    st.header("Recent Transactions")
    display_transactions()

    st.header("Your Quests & Achievements")
    show_quests()
