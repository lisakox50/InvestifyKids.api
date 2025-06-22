import streamlit as st

# Initialize session state variables
if "registered" not in st.session_state:
    st.session_state.registered = False
if "name" not in st.session_state:
    st.session_state.name = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "cash" not in st.session_state:
    st.session_state.cash = 10000.0  # virtual starting cash
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}  # stock symbol -> {"shares": int, "avg_price": float}
if "quests" not in st.session_state:
    st.session_state.quests = {
        "register": False,
        "buy_first_stock": False,
        "learn_terms": False,
        "check_price": False,
    }

# Mock data
FINANCIAL_TERMS = {
    "stock": "A stock is a share representing ownership in a company.",
    "bond": "A bond is a loan made by an investor to a borrower, like a company or government.",
    "fintech": "Fintech means financial technology innovations that improve financial services.",
    "dividend": "A dividend is a payment made by a company to its shareholders from profits.",
    "portfolio": "A portfolio is a collection of investments owned by an investor.",
}

MOCK_STOCK_PRICES = {
    "AAPL": 150.12,
    "TSLA": 700.45,
    "GOOG": 2800.99,
    "MSFT": 305.22,
    "AMZN": 3500.50,
}

# Functions
def register_user(name, role):
    st.session_state.name = name.strip()
    st.session_state.role = role
    st.session_state.registered = True
    st.session_state.quests["register"] = True
    st.success(f"Welcome, {st.session_state.name}! You registered as a {st.session_state.role}.")

def explain_term(term):
    return FINANCIAL_TERMS.get(term.lower(), "Sorry, no explanation found for this term.")

def get_stock_price(symbol):
    return MOCK_STOCK_PRICES.get(symbol.upper())

def buy_stock(symbol, shares):
    symbol = symbol.upper()
    price = get_stock_price(symbol)
    if price is None:
        return False, "Stock symbol not found."
    cost = shares * price
    if cost > st.session_state.cash:
        return False, f"Not enough cash. You need ${cost:.2f} but have only ${st.session_state.cash:.2f}."
    # Update portfolio
    if symbol in st.session_state.portfolio:
        current = st.session_state.portfolio[symbol]
        total_shares = current["shares"] + shares
        avg_price = ((current["avg_price"] * current["shares"]) + cost) / total_shares
        st.session_state.portfolio[symbol] = {"shares": total_shares, "avg_price": avg_price}
    else:
        st.session_state.portfolio[symbol] = {"shares": shares, "avg_price": price}
    st.session_state.cash -= cost
    if not st.session_state.quests["buy_first_stock"]:
        st.session_state.quests["buy_first_stock"] = True
    return True, f"Bought {shares} shares of {symbol} at ${price:.2f} each for ${cost:.2f}."

def sell_stock(symbol, shares):
    symbol = symbol.upper()
    if symbol not in st.session_state.portfolio:
        return False, "You do not own this stock."
    current = st.session_state.portfolio[symbol]
    if shares > current["shares"]:
        return False, f"You only own {current['shares']} shares."
    price = get_stock_price(symbol)
    if price is None:
        return False, "Cannot get stock price."
    revenue = shares * price
    current["shares"] -= shares
    if current["shares"] == 0:
        del st.session_state.portfolio[symbol]
    else:
        st.session_state.portfolio[symbol] = current
    st.session_state.cash += revenue
    return True, f"Sold {shares} shares of {symbol} at ${price:.2f} each for ${revenue:.2f}."

def portfolio_summary():
    total_value = 0.0
    summary_lines = []
    for symbol, data in st.session_state.portfolio.items():
        price = get_stock_price(symbol)
        value = price * data["shares"] if price else 0
        total_value += value
        summary_lines.append(f"{symbol}: {data['shares']} shares | Avg Price: ${data['avg_price']:.2f} | Current Price: ${price if price else 'N/A'} | Value: ${value:.2f}")
    return summary_lines, total_value

def show_quests():
    quests = {
        "register": "Complete registration",
        "buy_first_stock": "Buy your first stock",
        "learn_terms": "Learn financial terms",
        "check_price": "Check a stock price",
    }
    for key, desc in quests.items():
        status = "✅ Completed" if st.session_state.quests.get(key) else "❌ Incomplete"
        st.write(f"{desc}: {status}")

# Main app

st.title("InvestifyKids - FinTech Learning & Portfolio")

if not st.session_state.registered:
    st.header("Register")
    name = st.text_input("Enter your name")
    role = st.selectbox("Choose your role", ["Child", "Parent"])
    if st.button("Register"):
        if not name.strip():
            st.error("Please enter your name.")
        else:
            register_user(name, role)
else:
    st.sidebar.write(f"👋 Hello, {st.session_state.name} ({st.session_state.role})")
    st.sidebar.write(f"💰 Cash balance: ${st.session_state.cash:.2f}")

    st.header("Learn Financial Terms")
    term = st.text_input("Enter financial term to learn")
    if st.button("Explain Term"):
        explanation = explain_term(term)
        st.info(explanation)
        if term.lower() in FINANCIAL_TERMS:
            st.session_state.quests["learn_terms"] = True

    st.header("Check Stock Price")
    symbol = st.text_input("Enter stock symbol")
    if st.button("Check Price"):
        price = get_stock_price(symbol)
        if price:
            st.success(f"Current price of {symbol.upper()} is ${price:.2f}")
            st.session_state.quests["check_price"] = True
        else:
            st.error("Stock symbol not found.")

    st.header("Buy Stocks")
    buy_symbol = st.text_input("Stock symbol to buy", key="buy_symbol")
    buy_shares = st.number_input("Number of shares to buy", min_value=1, step=1, key="buy_shares")
    if st.button("Buy"):
        if not buy_symbol.strip():
            st.error("Please enter stock symbol.")
        else:
            success, msg = buy_stock(buy_symbol, buy_shares)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    st.header("Sell Stocks")
    sell_symbol = st.text_input("Stock symbol to sell", key="sell_symbol")
    sell_shares = st.number_input("Number of shares to sell", min_value=1, step=1, key="sell_shares")
    if st.button("Sell"):
        if not sell_symbol.strip():
            st.error("Please enter stock symbol.")
        else:
            success, msg = sell_stock(sell_symbol, sell_shares)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    st.header("Portfolio Summary")
    if len(st.session_state.portfolio) == 0:
        st.write("Your portfolio is empty.")
    else:
        lines, total_val = portfolio_summary()
        for line in lines:
            st.write(line)
        st.write(f"Total portfolio value: ${total_val:.2f}")
        st.write(f"Available cash: ${st.session_state.cash:.2f}")

    st.header("Your Quests & Achievements")
    show_quests()
