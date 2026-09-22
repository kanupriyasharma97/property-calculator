import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Rental Property Calculator",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Rental Property Calculator")
st.caption(
    "Estimate rental yield, EMI, cash surplus, acquisition costs, "
    "tenant brokerage and long-term rental economics."
)


# ============================================================
# CALCULATION FUNCTION
# ============================================================

def calculate_property(
    price,
    rent,
    maintenance,
    vacancy,
    rbi_pct,
    rbi_factor,
    other_factor,
    purchase_brokerage_pct,
    tenant_turnover_years
):

    # Loans
    rbi_loan = price * rbi_pct / 100
    other_loan = price - rbi_loan

    rbi_emi = rbi_loan * rbi_factor / 360
    other_emi = other_loan * other_factor / 360
    total_emi = rbi_emi + other_emi

    # Vacancy
    vacancy_loss = rent * vacancy / 100
    effective_rent = rent - vacancy_loss

    # Rental yields
    gross_yield = rent * 12 / price * 100

    net_yield = (
        (rent - maintenance) * 12 / price * 100
    )

    # Brokerage
    purchase_brokerage = (
        price * purchase_brokerage_pct / 100
    )

    tenant_brokerage = rent

    annual_tenant_brokerage = (
        tenant_brokerage / tenant_turnover_years
    )

    # Monthly cash flow
    monthly_surplus = (
        effective_rent
        - total_emi
        - maintenance
        - annual_tenant_brokerage / 12
    )

    annual_surplus = monthly_surplus * 12

    # Break-even
    break_even_rent = (
        total_emi
        + maintenance
        + annual_tenant_brokerage / 12
    )

    break_even_yield = (
        break_even_rent * 12 / price * 100
    )

    # 10-year tenant brokerage
    ten_year_tenant_brokerage = (
        tenant_brokerage
        * (10 / tenant_turnover_years)
    )

    total_ten_year_brokerage = (
        purchase_brokerage
        + ten_year_tenant_brokerage
    )

    return {
        "price": price,
        "rent": rent,
        "maintenance": maintenance,
        "rbi_loan": rbi_loan,
        "other_loan": other_loan,
        "rbi_emi": rbi_emi,
        "other_emi": other_emi,
        "total_emi": total_emi,
        "gross_yield": gross_yield,
        "net_yield": net_yield,
        "vacancy_loss": vacancy_loss,
        "effective_rent": effective_rent,
        "purchase_brokerage": purchase_brokerage,
        "tenant_brokerage": tenant_brokerage,
        "annual_tenant_brokerage": annual_tenant_brokerage,
        "monthly_surplus": monthly_surplus,
        "annual_surplus": annual_surplus,
        "break_even_rent": break_even_rent,
        "break_even_yield": break_even_yield,
        "ten_year_tenant_brokerage": ten_year_tenant_brokerage,
        "total_ten_year_brokerage": total_ten_year_brokerage
    }


# ============================================================
# SIDEBAR ASSUMPTIONS
# ============================================================

st.sidebar.header("⚙️ Financing & Rental Assumptions")

rbi_pct = st.sidebar.number_input(
    "RBI loan (%)",
    min_value=0.0,
    max_value=100.0,
    value=90.0,
    step=5.0
)

rbi_factor = st.sidebar.number_input(
    "RBI repayment factor",
    value=1.05,
    step=0.001,
    format="%.3f"
)

other_factor = st.sidebar.number_input(
    "Other loan repayment factor",
    value=1.075,
    step=0.001,
    format="%.3f"
)

vacancy = st.sidebar.number_input(
    "Vacancy allowance (%)",
    min_value=0.0,
    max_value=20.0,
    value=5.0,
    step=1.0
)

purchase_brokerage_pct = st.sidebar.number_input(
    "Purchase brokerage (%)",
    min_value=0.0,
    max_value=5.0,
    value=1.0,
    step=0.25
)

tenant_turnover_years = st.sidebar.number_input(
    "Tenant turnover — every X years",
    min_value=0.5,
    max_value=10.0,
    value=2.0,
    step=0.5
)

st.sidebar.markdown("---")

st.sidebar.info(
    "RBI repayment = RBI loan × factor ÷ 360\n\n"
    "Other loan repayment = Other loan × factor ÷ 360\n\n"
    "Purchase brokerage = property price × brokerage %\n\n"
    "Tenant brokerage = 1 month's rent whenever a new tenant is found."
)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs([
    "🏠 Single Property",
    "⚖️ Compare 2 Properties",
    "📈 10-Year Projection"
])


# ============================================================
# TAB 1 — SINGLE PROPERTY
# ============================================================

with tab1:

    st.header("Single Property Calculator")

    c1, c2, c3 = st.columns(3)

    with c1:
        price = st.number_input(
            "Property price (₹)",
            min_value=0.0,
            value=15000000.0,
            step=500000.0
        )

    with c2:
        rent = st.number_input(
            "Monthly rent (₹)",
            min_value=0.0,
            value=45000.0,
            step=1000.0
        )

    with c3:
        maintenance = st.number_input(
            "Monthly maintenance (₹)",
            min_value=0.0,
            value=8000.0,
            step=1000.0
        )

    result = calculate_property(
        price,
        rent,
        maintenance,
        vacancy,
        rbi_pct,
        rbi_factor,
        other_factor,
        purchase_brokerage_pct,
        tenant_turnover_years
    )

    st.markdown("---")

    # Key metrics
    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Gross rental yield",
        f"{result['gross_yield']:.2f}%"
    )

    m2.metric(
        "Net yield",
        f"{result['net_yield']:.2f}%"
    )

    m3.metric(
        "Monthly EMI",
        f"₹{result['total_emi']:,.0f}"
    )

    m4.metric(
        "Monthly surplus / deficit",
        f"₹{result['monthly_surplus']:,.0f}"
    )

    # Acquisition cost
    st.markdown("---")
    st.subheader("💰 One-Time Acquisition Cost")

    a1, a2, a3 = st.columns(3)

    a1.metric(
        "Property price",
        f"₹{price / 1e7:.2f} Cr"
    )

    a2.metric(
        f"Purchase brokerage ({purchase_brokerage_pct:.2f}%)",
        f"₹{result['purchase_brokerage']:,.0f}"
    )

    a3.metric(
        "Property + brokerage",
        f"₹{(price + result['purchase_brokerage']) / 1e7:.2f} Cr"
    )

    st.caption(
        "Purchase brokerage is treated as a one-time acquisition cost."
    )

    # Loan structure
    st.markdown("---")
    st.subheader("🏦 Loan Structure")

    loan_df = pd.DataFrame({
        "Component": [
            "RBI loan",
            "Other loan",
            "Total"
        ],
        "Amount": [
            result["rbi_loan"],
            result["other_loan"],
            result["rbi_loan"] + result["other_loan"]
        ],
        "Monthly repayment": [
            result["rbi_emi"],
            result["other_emi"],
            result["total_emi"]
        ]
    })

    loan_df["Amount"] = loan_df["Amount"].map(
        lambda x: f"₹{x:,.0f}"
    )

    loan_df["Monthly repayment"] = loan_df[
        "Monthly repayment"
    ].map(
        lambda x: f"₹{x:,.0f}"
    )

    st.table(loan_df)

    # Rental details
    st.subheader("🏠 Rental Cash Flow")

    rental_df = pd.DataFrame({
        "Item": [
            "Monthly rent",
            "Vacancy loss",
            "Effective monthly rent",
            "Maintenance",
            "Tenant brokerage per turnover",
            "Annualised tenant brokerage"
        ],
        "Amount": [
            f"₹{rent:,.0f}",
            f"₹{result['vacancy_loss']:,.0f}",
            f"₹{result['effective_rent']:,.0f}",
            f"₹{maintenance:,.0f}",
            f"₹{result['tenant_brokerage']:,.0f}",
            f"₹{result['annual_tenant_brokerage']:,.0f}"
        ]
    })

    st.table(rental_df)

    # Break-even
    st.markdown("---")
    st.subheader("🎯 Break-Even Analysis")

    b1, b2, b3 = st.columns(3)

    b1.metric(
        "Break-even monthly rent",
        f"₹{result['break_even_rent']:,.0f}"
    )

    b2.metric(
        "Break-even gross yield",
        f"{result['break_even_yield']:.2f}%"
    )

    b3.metric(
        "Annual surplus / deficit",
        f"₹{result['annual_surplus']:,.0f}"
    )

    # Tenant brokerage
    st.markdown("---")
    st.subheader("🔄 Tenant Turnover Costs")

    t1, t2, t3 = st.columns(3)

    t1.metric(
        "Brokerage per new tenant",
        f"₹{result['tenant_brokerage']:,.0f}"
    )

    t2.metric(
        "Assumed turnover",
        f"Every {tenant_turnover_years:g} years"
    )

    t3.metric(
        "10-year tenant brokerage",
        f"₹{result['ten_year_tenant_brokerage']:,.0f}"
    )

    # Total brokerage
    st.subheader("📋 Total Brokerage — 10 Years")

    brokerage_df = pd.DataFrame({
        "Cost": [
            "Purchase brokerage",
            "Tenant brokerage — 10 years",
            "Total brokerage — 10 years"
        ],
        "Amount": [
            f"₹{result['purchase_brokerage']:,.0f}",
            f"₹{result['ten_year_tenant_brokerage']:,.0f}",
            f"₹{result['total_ten_year_brokerage']:,.0f}"
        ]
    })

    st.table(brokerage_df)

    if result["monthly_surplus"] >= 0:
        st.success(
            f"Positive monthly cash flow of "
            f"₹{result['monthly_surplus']:,.0f} after EMI, "
            f"maintenance, vacancy allowance and tenant brokerage."
        )
    else:
        st.warning(
            f"Monthly cash-flow deficit of "
            f"₹{abs(result['monthly_surplus']):,.0f} after EMI, "
            f"maintenance, vacancy allowance and tenant brokerage."
        )


# ============================================================
# TAB 2 — COMPARE TWO PROPERTIES
# ============================================================

with tab2:

    st.header("⚖️ Compare Two Properties")

    st.info(
        "Useful for comparing combinations such as NCP + Thane "
        "or NCP + Kharghar."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Property 1")

        p1 = st.number_input(
            "Property 1 price (₹)",
            min_value=0.0,
            value=17000000.0,
            step=500000.0,
            key="p1"
        )

        r1 = st.number_input(
            "Property 1 rent / month (₹)",
            min_value=0.0,
            value=80000.0,
            step=1000.0,
            key="r1"
        )

        m1 = st.number_input(
            "Property 1 maintenance / month (₹)",
            min_value=0.0,
            value=10000.0,
            step=1000.0,
            key="m1"
        )

    with col2:

        st.subheader("Property 2")

        p2 = st.number_input(
            "Property 2 price (₹)",
            min_value=0.0,
            value=11000000.0,
            step=500000.0,
            key="p2"
        )

        r2 = st.number_input(
            "Property 2 rent / month (₹)",
            min_value=0.0,
            value=43000.0,
            step=1000.0,
            key="r2"
        )

        m2 = st.number_input(
            "Property 2 maintenance / month (₹)",
            min_value=0.0,
            value=8000.0,
            step=1000.0,
            key="m2"
        )

    a = calculate_property(
        p1, r1, m1,
        vacancy,
        rbi_pct,
        rbi_factor,
        other_factor,
        purchase_brokerage_pct,
        tenant_turnover_years
    )

    b = calculate_property(
        p2, r2, m2,
        vacancy,
        rbi_pct,
        rbi_factor,
        other_factor,
        purchase_brokerage_pct,
        tenant_turnover_years
    )

    total_price = p1 + p2
    total_rent = r1 + r2
    total_maintenance = m1 + m2
    total_emi = a["total_emi"] + b["total_emi"]

    total_purchase_brokerage = (
        a["purchase_brokerage"] +
        b["purchase_brokerage"]
    )

    total_tenant_brokerage = (
        a["ten_year_tenant_brokerage"] +
        b["ten_year_tenant_brokerage"]
    )

    portfolio_gross_yield = (
        total_rent * 12 / total_price * 100
    )

    portfolio_surplus = (
        total_rent * (1 - vacancy / 100)
        - total_maintenance
        - total_emi
        - (
            a["annual_tenant_brokerage"] +
            b["annual_tenant_brokerage"]
        ) / 12
    )

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Combined property value",
        f"₹{total_price / 1e7:.2f} Cr"
    )

    c2.metric(
        "Portfolio gross yield",
        f"{portfolio_gross_yield:.2f}%"
    )

    c3.metric(
        "Total monthly EMI",
        f"₹{total_emi:,.0f}"
    )

    c4.metric(
        "Portfolio monthly surplus",
        f"₹{portfolio_surplus:,.0f}"
    )

    st.markdown("---")

    comparison = pd.DataFrame({
        "Metric": [
            "Property value",
            "Purchase brokerage",
            "Monthly rent",
            "Monthly maintenance",
            "Gross rental yield",
            "Monthly EMI",
            "Tenant brokerage / turnover",
            "10-year tenant brokerage",
            "Monthly surplus / deficit"
        ],
        "Property 1": [
            f"₹{p1:,.0f}",
            f"₹{a['purchase_brokerage']:,.0f}",
            f"₹{r1:,.0f}",
            f"₹{m1:,.0f}",
            f"{a['gross_yield']:.2f}%",
            f"₹{a['total_emi']:,.0f}",
            f"₹{a['tenant_brokerage']:,.0f}",
            f"₹{a['ten_year_tenant_brokerage']:,.0f}",
            f"₹{a['monthly_surplus']:,.0f}"
        ],
        "Property 2": [
            f"₹{p2:,.0f}",
            f"₹{b['purchase_brokerage']:,.0f}",
            f"₹{r2:,.0f}",
            f"₹{m2:,.0f}",
            f"{b['gross_yield']:.2f}%",
            f"₹{b['total_emi']:,.0f}",
            f"₹{b['tenant_brokerage']:,.0f}",
            f"₹{b['ten_year_tenant_brokerage']:,.0f}",
            f"₹{b['monthly_surplus']:,.0f}"
        ]
    })

    st.table(comparison)

    st.subheader("📋 Combined Brokerage Costs — 10 Years")

    portfolio_brokerage = pd.DataFrame({
        "Cost": [
            "Purchase brokerage — both properties",
            "Tenant brokerage — 10 years",
            "Total brokerage — 10 years"
        ],
        "Amount": [
            f"₹{total_purchase_brokerage:,.0f}",
            f"₹{total_tenant_brokerage:,.0f}",
            f"₹{total_purchase_brokerage + total_tenant_brokerage:,.0f}"
        ]
    })

    st.table(portfolio_brokerage)

    if portfolio_surplus >= 0:
        st.success(
            f"Combined portfolio generates approximately "
            f"₹{portfolio_surplus:,.0f} surplus per month."
        )
    else:
        st.warning(
            f"Combined portfolio has approximately "
            f"₹{abs(portfolio_surplus):,.0f} monthly deficit."
        )


# ============================================================
# TAB 3 — 10 YEAR PROJECTION
# ============================================================

with tab3:

    st.header("📈 10-Year Property Projection")

    c1, c2, c3 = st.columns(3)

    with c1:

        start_price = st.number_input(
            "Starting property value (₹)",
            min_value=0.0,
            value=15000000.0,
            step=500000.0,
            key="start_price"
        )

        appreciation = st.number_input(
            "Annual appreciation (%)",
            min_value=-10.0,
            max_value=30.0,
            value=8.0,
            step=0.5
        )

    with c2:

        start_rent = st.number_input(
            "Starting monthly rent (₹)",
            min_value=0.0,
            value=45000.0,
            step=1000.0,
            key="start_rent"
        )

        rent_growth = st.number_input(
            "Annual rent escalation (%)",
            min_value=-10.0,
            max_value=30.0,
            value=5.0,
            step=0.5
        )

    with c3:

        start_maintenance = st.number_input(
            "Starting monthly maintenance (₹)",
            min_value=0.0,
            value=8000.0,
            step=1000.0,
            key="start_maintenance"
        )

        maintenance_growth = st.number_input(
            "Annual maintenance escalation (%)",
            min_value=-10.0,
            max_value=30.0,
            value=5.0,
            step=0.5
        )

    rows = []
    cumulative_net_rent = 0

    for year in range(1, 11):

        property_value = (
            start_price *
            (1 + appreciation / 100) ** year
        )

        monthly_rent = (
            start_rent *
            (1 + rent_growth / 100) ** year
        )

        monthly_maintenance = (
            start_maintenance *
            (1 + maintenance_growth / 100) ** year
        )

        annual_rent = monthly_rent * 12

        vacancy_loss = annual_rent * vacancy / 100

        effective_annual_rent = (
            annual_rent - vacancy_loss
        )

        annual_maintenance = (
            monthly_maintenance * 12
        )

        annual_tenant_brokerage = (
            monthly_rent / tenant_turnover_years
        )

        annual_net_rent = (
            effective_annual_rent
            - annual_maintenance
            - annual_tenant_brokerage
        )

        cumulative_net_rent += annual_net_rent

        rows.append({
            "Year": year,
            "Property value": property_value,
            "Monthly rent": monthly_rent,
            "Annual rent": annual_rent,
            "Vacancy loss": vacancy_loss,
            "Annual maintenance": annual_maintenance,
            "Tenant brokerage": annual_tenant_brokerage,
            "Net rental cash flow": annual_net_rent,
            "Cumulative net rental cash flow":
                cumulative_net_rent
        })

    projection = pd.DataFrame(rows)

    final_value = projection.iloc[-1]["Property value"]

    appreciation_gain = final_value - start_price

    cumulative_rent = projection["Annual rent"].sum()
    cumulative_vacancy = projection["Vacancy loss"].sum()
    cumulative_maintenance = projection["Annual maintenance"].sum()
    cumulative_tenant_brokerage = projection["Tenant brokerage"].sum()

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Value after 10 years",
        f"₹{final_value / 1e7:.2f} Cr"
    )

    c2.metric(
        "Capital appreciation",
        f"₹{appreciation_gain / 1e7:.2f} Cr"
    )

    c3.metric(
        "Gross rental income",
        f"₹{cumulative_rent / 1e7:.2f} Cr"
    )

    c4.metric(
        "Net rental cash flow",
        f"₹{cumulative_net_rent / 1e7:.2f} Cr"
    )

    st.markdown("---")

    st.subheader("10-Year Rental Cost Breakdown")

    ten_year_costs = pd.DataFrame({
        "Item": [
            "Gross rental income",
            "Vacancy loss",
            "Maintenance",
            "Tenant brokerage",
            "Net rental cash flow"
        ],
        "Amount": [
            f"₹{cumulative_rent:,.0f}",
            f"₹{cumulative_vacancy:,.0f}",
            f"₹{cumulative_maintenance:,.0f}",
            f"₹{cumulative_tenant_brokerage:,.0f}",
            f"₹{cumulative_net_rent:,.0f}"
        ]
    })

    st.table(ten_year_costs)

    st.markdown("---")

    st.subheader("Year-by-Year Projection")

    display_projection = projection.copy()

    display_projection["Property value"] = \
        display_projection["Property value"].map(
            lambda x: f"₹{x / 1e7:.2f} Cr"
        )

    display_projection["Monthly rent"] = \
        display_projection["Monthly rent"].map(
            lambda x: f"₹{x:,.0f}"
        )

    display_projection["Annual rent"] = \
        display_projection["Annual rent"].map(
            lambda x: f"₹{x:,.0f}"
        )

    display_projection["Vacancy loss"] = \
        display_projection["Vacancy loss"].map(
            lambda x: f"₹{x:,.0f}"
        )

    display_projection["Annual maintenance"] = \
        display_projection["Annual maintenance"].map(
            lambda x: f"₹{x:,.0f}"
        )

    display_projection["Tenant brokerage"] = \
        display_projection["Tenant brokerage"].map(
            lambda x: f"₹{x:,.0f}"
        )

    display_projection["Net rental cash flow"] = \
        display_projection["Net rental cash flow"].map(
            lambda x: f"₹{x:,.0f}"
        )

    display_projection["Cumulative net rental cash flow"] = \
        display_projection["Cumulative net rental cash flow"].map(
            lambda x: f"₹{x:,.0f}"
        )

    st.table(display_projection)

    st.info(
        "Purchase brokerage is a one-time acquisition cost and is "
        "shown separately. Tenant brokerage is annualised based on "
        "the assumed tenant turnover period."
    )
