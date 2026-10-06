from datetime import date

import pandas as pd
import streamlit as st


def render_treaty() -> None:
    st.markdown('<div class="page-eyebrow">Programme management</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-title">Treaty</h1>', unsafe_allow_html=True)
    st.caption(
        "Sample programme from your reference screen. Edit the fields and layers "
        "to explore the layout. Saving and ALPS integration are not implemented."
    )

    with st.container(border=True):
        columns = st.columns([2, 3, 1.4, 1, 1, 0.6, 1.2])
        with columns[0]:
            st.text_input("Reinsured", value="AEGIS", key="treaty_reinsured")
        with columns[1]:
            st.text_input("Programme Name", value="AEGIS GL 2012", key="treaty_programme")
        with columns[2]:
            st.selectbox("Status", ["Actual", "Estimated", "Projected"], key="treaty_status")
        with columns[3]:
            st.number_input("Y.O.A.", min_value=1900, max_value=2200, value=2012, key="treaty_yoa")
        with columns[4]:
            st.selectbox("Type", ["XOL"], key="treaty_type")
        with columns[5]:
            st.checkbox("RXS", key="treaty_rxs")
        with columns[6]:
            st.selectbox("Mode", ["New"], key="treaty_mode")

        columns = st.columns([1, 1, 1, 1, 1, 1, 1.8])
        with columns[0]:
            st.date_input("Risks From", value=date(2012, 1, 1), key="treaty_risks_from")
        with columns[1]:
            st.date_input("Risks To", value=date(2012, 12, 31), key="treaty_risks_to")
        with columns[2]:
            st.date_input("Losses From", value=None, key="treaty_losses_from")
        with columns[3]:
            st.date_input("Losses To", value=None, key="treaty_losses_to")
        with columns[4]:
            st.date_input("Accepted From", value=None, key="treaty_accepted_from")
        with columns[5]:
            st.date_input("Accepted To", value=None, key="treaty_accepted_to")
        with columns[6]:
            st.selectbox("Casualty Count Basis", ["All Casualties"], key="treaty_casualty_basis")

        columns = st.columns([2.3, 1, 2, 1.4, 0.8, 0.8])
        with columns[0]:
            st.selectbox(
                "Premium-related Amounts are in",
                ["USD", "GBP", "EUR"],
                key="treaty_premium_currency",
            )
        with columns[1]:
            st.number_input("R.O.E.", min_value=0.0001, value=1.6215, format="%.4f", key="treaty_roe")
        with columns[2]:
            st.number_input(
                "Original Premium Income",
                min_value=0.0,
                value=41000000.0,
                step=1000.0,
                format="%.2f",
                key="treaty_original_premium",
            )
        with columns[3]:
            st.selectbox("Premium Status", ["Actual", "Estimated"], key="treaty_premium_status")
        with columns[4]:
            st.button("Lines", disabled=True, help="Line selection is not implemented.")
        with columns[5]:
            st.button("Save", disabled=True, help="Saving is not implemented; no database writes.")

    with st.container(border=True):
        columns = st.columns([1.2, 1.5, 1.6, 1.2, 0.8, 1])
        with columns[0]:
            st.selectbox("Loss Currency", ["USD", "GBP", "EUR"], key="treaty_loss_currency")
        with columns[1]:
            st.number_input(
                "Excess", min_value=0.0, value=7500000.0, format="%.2f", key="treaty_excess"
            )
        with columns[2]:
            st.text_input("or % of", value="<None>", key="treaty_excess_basis")
        with columns[3]:
            st.selectbox("Whichever the", ["Greater", "Lesser"], key="treaty_comparison")
        with columns[4]:
            st.text_input("Amount cap", value="UNL", key="treaty_cap")
        with columns[5]:
            st.selectbox("Limits", ["UNL", "Limited"], key="treaty_limits")

        columns = st.columns([1, 1, 1.2, 1.4, 1.6, 2.7])
        with columns[0]:
            st.number_input("Max. Line %", min_value=0.0, max_value=100.0, value=100.0, key="treaty_max_line")
        with columns[1]:
            st.number_input("Min. Line %", min_value=0.0, max_value=100.0, value=0.0, key="treaty_min_line")
        with columns[2]:
            st.selectbox("per", ["Loss"], key="treaty_per")
        with columns[3]:
            st.selectbox("Interlocking", ["Optional"], key="treaty_interlocking")
        with columns[4]:
            st.text_input("Total Indemnity", value="<As per Layers>", key="treaty_indemnity")
        with columns[5]:
            st.selectbox(
                "Market Loss Definition",
                ["Losses Attaching to Questionnaire"],
                key="treaty_market_loss",
            )

    tabs = st.tabs(["Layers", "Currencies", "Types", "Locales", "Benefit", "Retro"])
    with tabs[0]:
        layers = pd.DataFrame(
            [
                {
                    "No": 1, "Type": "Core", "Limit": 7500000.0,
                    "Prem Basis": "Income", "Premium": 0.0, "Pr. Rate": 4.5,
                    "Min Prem": 0.0, "Max Prem": "Unlimited", "Brokerage": 10.0,
                    "%": 0.0, "Max Brok": None, "PP": "", "CP": "", "Backup": "",
                    "Stretch": 45000000.0,
                },
                {
                    "No": 2, "Type": "Core", "Limit": 10000000.0,
                    "Prem Basis": "Flat", "Premium": 53317.0, "Pr. Rate": 0.0,
                    "Min Prem": 0.0, "Max Prem": "Unlimited", "Brokerage": 10.0,
                    "%": 0.0, "Max Brok": None, "PP": "", "CP": "", "Backup": "",
                    "Stretch": 20000000.0,
                },
            ]
        )
        st.data_editor(
            layers,
            hide_index=True,
            num_rows="dynamic",
            use_container_width=True,
            height=270,
            key="treaty_layers",
            column_config={
                "No": st.column_config.NumberColumn("No", min_value=1, step=1),
                "Type": st.column_config.SelectboxColumn("Type", options=["Core"]),
                "Prem Basis": st.column_config.SelectboxColumn("Prem Basis", options=["Income", "Flat"]),
                **{
                    column: st.column_config.NumberColumn(column, min_value=0.0, format="localized")
                    for column in ("Limit", "Premium", "Pr. Rate", "Min Prem", "Brokerage", "%", "Max Brok", "Stretch")
                },
            },
        )
        st.caption(
            "Add, edit, or remove sample layers in the grid. Changes are for this "
            "browser session only; advanced layer terms are not implemented."
        )
    for tab, name in zip(tabs[1:], ["Currencies", "Types", "Locales", "Benefit", "Retro"]):
        with tab:
            st.info(f"{name} settings are not implemented yet.")
