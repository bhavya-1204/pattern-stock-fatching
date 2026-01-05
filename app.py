import streamlit as st

# ---------- Page config ----------
st.set_page_config(
    page_title="Stock Selection Dashboard",
    page_icon="📈",
    layout="centered"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 10px;
}
.sub-title {
    text-align: center;
    color: #6c757d;
    margin-bottom: 40px;
}
.card {
    background: #ffffff;
    border-radius: 16px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    transition: transform 0.2s ease-in-out;
}
.card:hover {
    transform: translateY(-5px);
}
.card-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 10px;
}
.card-desc {
    color: #6c757d;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="main-title">📈 STOCK SELECTION DASHBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Technical pattern & F&O stock screening</div>', unsafe_allow_html=True)

# ---------- Cards ----------
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">📊 Pattern Stocks</div>
        <div class="card-desc">
            Detect high-probability chart patterns using EMA & price action.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/pattern_app.py",
        label="Open Pattern Scanner",
        icon="➡️"
    )

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">⚡ Futures & Options</div>
        <div class="card-desc">
            Identify momentum-based F&O stocks with EMA & volume logic.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/app_future.py",
        label="Open F&O Scanner",
        icon="➡️"
    )

# ---------- Footer ----------
st.markdown("---")
st.caption("🚀 Built with Streamlit | Market analysis dashboard")
