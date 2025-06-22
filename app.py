import streamlit as st

# Начинаем с регистрации
if "registered" not in st.session_state:
    st.session_state.registered = False

if not st.session_state.registered:
    st.title("Welcome to InvestifyKids")
    name = st.text_input("Enter your name")
    role = st.selectbox("Choose your role", ["Child", "Parent"])
    if st.button("Register"):
        if name.strip() == "":
            st.error("Please enter your name!")
        else:
            st.session_state.name = name.strip()
            st.session_state.role = role
            st.session_state.registered = True
            st.success(f"Hello {name}, you registered as {role}!")
else:
    st.title(f"Hello, {st.session_state.name}!")

    st.header("Explain financial term")
    term = st.text_input("Enter a term (e.g. stock, bond, fintech)")
    if st.button("Explain"):
        explanations = {
            "stock": "A stock is a share representing ownership in a company.",
            "bond": "A bond is a loan made by an investor to a borrower.",
            "fintech": "Fintech means financial technology innovations.",
        }
        explanation = explanations.get(term.lower(), "Sorry, explanation not found.")
        st.info(explanation)

    st.header("Mock stock price checker")
    symbol = st.text_input("Enter stock symbol (e.g. AAPL)")
    if st.button("Check price"):
        prices = {
            "AAPL": 150.12,
            "TSLA": 700.45,
            "GOOG": 2800.99,
        }
        price = prices.get(symbol.upper())
        if price:
            st.success(f"Current price of {symbol.upper()} is ${price}")
        else:
            st.error("Stock symbol not found.")

    st.header("Simple portfolio (demo)")
    portfolio = {
        "AAPL": 10,
        "TSLA": 5,
    }
    st.write("Your portfolio:")
    for s, shares in portfolio.items():
        st.write(f"{s}: {shares} shares")

    st.write("---")
    st.write("This is a minimal demo app. Expand it as you like!")
