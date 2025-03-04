import streamlit as st  # type: ignore
from forex_python.converter import CurrencyRates  # type: ignore
from pint import UnitRegistry  # type: ignore

# Initialize unit registry
ureg = UnitRegistry()

# Streamlit UI
st.set_page_config(page_title="🔢 Advanced Unit Converter & Calculator", layout="wide")

# Styling
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #4facfe, #00f2fe);
        color: white;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: #222222 !important;
        font-weight: bold;
    }
    .stButton > button {
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
        background-color: #3498db;
        color: white;
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }
    .footer {
        position: fixed;
        bottom: 10px;
        width: 100%;
        text-align: center;
        font-weight: bold;
        color: #222222;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔢 Advanced Unit Converter & Calculator")

# Sidebar for navigation
conversion_type = st.sidebar.radio("Select Option", [
    "📏 Length", "🌡 Temperature", "📐 Area", "📦 Volume", "⚖ Weight", "⏳ Time", "💲 Currency", "🖩 Simple Calculator"
])

# Simple Calculator
if conversion_type == "🖩 Simple Calculator":
    st.header("🖩 Simple Calculator")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        num1 = st.number_input("First Number", format="%.4f")
    with col2:
        operation = st.selectbox("Operation", ["+", "-", "×", "÷"])
    with col3:
        num2 = st.number_input("Second Number", format="%.4f")

    if st.button("Calculate"):
        try:
            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "×":
                result = num1 * num2
            elif operation == "÷":
                result = num1 / num2 if num2 != 0 else "Error (division by zero)"
            st.success(f"Result: {result}")
        except:
            st.error("Invalid input. Please check your numbers.")

else:
    units = {
        "📏 Length": ["meter", "kilometer", "centimeter", "millimeter", "mile", "yard", "foot", "inch"],
        "🌡 Temperature": ["celsius", "fahrenheit", "kelvin"],
        "📐 Area": ["square meter", "square kilometer", "square mile", "acre", "hectare"],
        "📦 Volume": ["liter", "milliliter", "cubic meter", "gallon", "pint"],
        "⚖ Weight": ["gram", "kilogram", "pound", "ounce", "ton"],
        "⏳ Time": ["second", "minute", "hour", "day", "week"],
        "💲 Currency": ["USD", "EUR", "GBP", "INR", "PKR", "AUD", "CAD"]
    }

    Enter_value = st.selectbox("Enter Value :", units[conversion_type])
    from_unit = st.selectbox("From :", units[conversion_type])
    value = st.number_input("To :", min_value=0.0, format="%.4f")

    if st.button("Convert"):
        if conversion_type == "💲 Currency":
            c = CurrencyRates()
            try:
                result = c.convert(from_unit, Enter_value, value)
                st.success(f"{value} {from_unit} = {result:.4f} {Enter_value}")
            except Exception:
                st.error("Error fetching currency rates. Try again later.")
        elif conversion_type == "🌡 Temperature":
            conversions = {
                ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32,
                ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
                ("celsius", "kelvin"): lambda x: x + 273.15,
                ("kelvin", "celsius"): lambda x: x - 273.15
            }
            result = conversions.get((from_unit, Enter_value), lambda x: x)(value)
            st.success(f"{value} {from_unit} = {result:.4f} {Enter_value}")
        else:
            try:
                result = (value * ureg(from_unit)).to(Enter_value)
                st.success(f"{value} {from_unit} = {result:.4f} {Enter_value}")
            except:
                st.error("Invalid conversion.")

# Footer
st.markdown('<p class="footer">❤️ Created by Shan-E-Zehra</p>', unsafe_allow_html=True)