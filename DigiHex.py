import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="DigiHex Price Estimator",
    page_icon=":bar_chart:",
    layout="centered"
)

# Private variable for price adjustment percentage (CONTANT, dont touch imo)
_price_adjustment_percentage = 0  # Adjust prices by this percentage (e.g., 0 for no change, 10 for +10%)

def adjust_price(price):
    """Adjust price by the set percentage."""
    return round(price * (1 + _price_adjustment_percentage / 100), 2)

# Title and description
st.title("DigiHex AI Customer Support Agent Price Estimator (HOSTING)")
st.markdown("""
Welcome to the DigiHex Price Estimator. Customize your AI customer support solution by selecting from the options below. The total cost will update automatically based on your selections.
""")

# --- Select AI Agents / Base Model Usage ---
st.header("Base Model Usage Plan")

ai_agent_option = st.selectbox(
    "Select your AI Agents/Base Model usage plan:",
    (
        "Option 1: 4M monthly AI tokens, roughly 40,000 messages",
        "Option 2: 20M monthly AI tokens, roughly 90,000 messages"
    )
)

# --- Integration with Shopify (Optional) ---
st.header("Shopify Integration Options")

shopify_option = st.radio(
    "Would you like to integrate with Shopify?",
    (
        "No Integration",
        "Option 1: 2,500 Products listed on Shopify",
        "Option 2: 5,000 Products listed on Shopify"
    )
)

# --- Advanced Features (Optional) ---
st.header("Advanced Features (Custom Dashboards, Custom UI, Advanced GPT models)")

advanced_features_option = st.radio(
    "Select an advanced features package:",
    (
        "No Advanced Features",
        "Option 1: 5,000 credits",
        "Option 2: 15,000 credits",
        "Option 3: 50,000 credits"
    )
)

# --- Calculate Total Cost ---
cost_breakdown = {}

# Base Model Usage Cost
if "Option 1" in ai_agent_option:
    cost_breakdown['Base Model Usage'] = adjust_price(50)
else:
    cost_breakdown['Base Model Usage'] = adjust_price(125)

# Shopify Integration Cost
if "No Integration" in shopify_option:
    cost_breakdown['Shopify Integration'] = adjust_price(0)
elif "Option 1" in shopify_option:
    cost_breakdown['Shopify Integration'] = adjust_price(19)
else:
    cost_breakdown['Shopify Integration'] = adjust_price(29)

# Advanced Features Cost
if "No Advanced Features" in advanced_features_option:
    cost_breakdown['Advanced Features'] = adjust_price(0)
elif "Option 1" in advanced_features_option:
    cost_breakdown['Advanced Features'] = adjust_price(19)
elif "Option 2" in advanced_features_option:
    cost_breakdown['Advanced Features'] = adjust_price(49)
else:
    cost_breakdown['Advanced Features'] = adjust_price(149)

# Total Cost before commission
total_cost = sum(cost_breakdown.values())

# Commission tiers
x = 150  # Threshold for 75% commission
y = 300  # Threshold for 50% commission

if total_cost < x:
    commission_percentage = 100
elif total_cost < y:
    commission_percentage = 75
else:
    commission_percentage = 50

commission_amount = total_cost * commission_percentage / 100

# Total cost including commission
total_cost_with_commission = total_cost + commission_amount

# Add commission to cost breakdown
cost_breakdown['Commission'] = round(commission_amount, 2)

# --- Display Total Cost ---
st.header("Estimated Total Monthly Cost")
st.subheader(f"${round(total_cost_with_commission, 2)}/mo")

# --- Display Cost Breakdown Chart ---
with st.expander("View Cost Breakdown Chart"):
    # Exclude 'Commission' from the cost breakdown
    breakdown_df = pd.DataFrame.from_dict(
        {k: v for k, v in cost_breakdown.items() if k != 'Commission'},
        orient='index',
        columns=['Cost']
    )
    breakdown_df = breakdown_df.reset_index().rename(columns={'index': 'Category'})

    fig = px.pie(
        breakdown_df,
        names='Category',
        values='Cost',
        title='Monthly Cost Distribution',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig)

# --- Additional Information ---
st.header("Plan Details")

with st.expander("Base Model Usage Details"):
    st.write("""
    **Option 1:** Suitable for startups and small businesses with moderate customer interaction.

    **Option 2:** Ideal for established businesses handling a high volume of customer queries.
    """)

with st.expander("Shopify Integration Details"):
    st.write("""
    Seamlessly integrate your AI agent with your Shopify store to provide real-time product information to customers.
    """)

with st.expander("Advanced Features Details"):
    st.write("""
    - **Customized Chat UI:** Tailor the chat interface to match your brand identity.
    - **Usage Dashboard:** Monitor AI agent performance and customer interactions.
    - **Advanced Fine-tuned GPT Models:** Enhance responses with specialized models for better customer engagement.
    """)

# --- Footer ---
st.markdown("---")
st.markdown("© 2024 DigiHex. All rights reserved. Annual packages available upon request.")
