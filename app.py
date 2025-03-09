import streamlit as st  # type: ignore
from forex_python.converter import CurrencyRates  # type: ignore
from pint import UnitRegistry  # type: ignore

# Initialize unit registry
ureg = UnitRegistry()

# Streamlit UI
st.set_page_config(page_title="🔢 Smart Unit Converter", layout="wide")

# Styling for dark mode
st.markdown(
    """
    <style>
    .stApp {
        background: #121212;
        color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: #ffffff !important;
        font-weight: bold;
    }
    .stSelectbox, .stNumber_input, .stButton > button {
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        background-color: #333333;
        color: #ffffff;
        border: 1px solid #ffffff;
    }
    .stButton > button:hover {
        background-color: #ff9800;
        color: black;
    }
    .footer {
        text-align: center;
        font-weight: bold;
        margin-top: 20px;
        color: #bbbbbb;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
    }
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] div {
        color: #ffffff !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("✨ Smart Unit Converter ✨")

# Sidebar for unit selection with icons
conversion_type = st.sidebar.radio("📌 Select Conversion Type", [
    "📏 Length", "🌡 Temperature", "📐 Area", "📦 Volume", "⚖ Weight", "⏳ Time", "💲 Currency"
])

# Units dictionary
units = {
    "📏 Length": ["meter", "kilometer", "centimeter", "millimeter", "mile", "yard", "foot", "inch"],
    "🌡 Temperature": ["celsius", "fahrenheit", "kelvin"],
    "📐 Area": ["square meter", "square kilometer", "square mile", "acre", "hectare"],
    "📦 Volume": ["liter", "milliliter", "cubic meter", "gallon", "pint"],
    "⚖ Weight": ["gram", "kilogram", "pound", "ounce", "ton"],
    "⏳ Time": ["second", "minute", "hour", "day", "week"],
    "💲 Currency": ["USD", "EUR", "GBP", "INR", "PKR", "AUD", "CAD"]
}

col1, col2, col3 = st.columns(3)
with col1:
    value = st.number_input("🔢 Enter Value:", min_value=0.0, format="%.4f")
with col2:
    from_unit = st.selectbox("🔄 From:", units[conversion_type])
with col3:
    to_unit = st.selectbox("➡️ To:", units[conversion_type])

if st.button("🚀 Convert"):
    if conversion_type == "💲 Currency":
        c = CurrencyRates()
        try:
            result = c.convert(from_unit, to_unit, value)
            st.success(f"{value} {from_unit} = {result:.4f} {to_unit} 💰")
        except Exception:
            st.error("⚠️ Error fetching currency rates. Try again later.")
    elif conversion_type == "🌡 Temperature":
        conversions = {
            ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32,
            ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
            ("celsius", "kelvin"): lambda x: x + 273.15,
            ("kelvin", "celsius"): lambda x: x - 273.15
        }
        result = conversions.get((from_unit, to_unit), lambda x: x)(value)
        st.success(f"{value} {from_unit} = {result:.4f} {to_unit} 🌡")
    else:
        try:
            result = (value * ureg(from_unit)).to(to_unit)
            st.success(f"{value} {from_unit} = {result:.4f} {to_unit} ✅")
        except:
            st.error("⚠️ Invalid conversion.")

# Footer
st.markdown('<p class="footer">❤️ Created by Shan-E-Zehra 🚀</p>', unsafe_allow_html=True)
