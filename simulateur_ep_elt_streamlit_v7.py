
import streamlit as st
from math import pow
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulateur EP / ELT / Non-Fiscal", layout="wide")

def future_value_annuity(P, r, n):
    return P * ((pow(1 + r, n) - 1) / r)

def calculateur(mensuel, duree, frais_entree, frais_gestion, taux_interet, montant_initial=0.0):
    P_net = mensuel * (1 - frais_entree / 100)
    r = (taux_interet - frais_gestion) / 12 / 100
    n = duree * 12
    capital = montant_initial * pow(1 + r, n) + future_value_annuity(P_net, r, n)
    return round(capital, 2)

def plot_evolution(mensuel, duree, frais_entree, frais_gestion, taux, montant_initial=0.0):
    mensualite_net = mensuel * (1 - frais_entree / 100)
    r = (taux - frais_gestion) / 12 / 100
    total = montant_initial
    capitals = []
    for mois in range(1, duree * 12 + 1):
        total = total * (1 + r) + mensualite_net
        capitals.append(total)
    return capitals

st.markdown("<h1 style='text-align: center; color: #0B6E4F;'>📊 Simulateur Financier – EP, ELT & Non-Fiscal</h1>", unsafe_allow_html=True)
st.markdown("---")

age = st.slider("👤 Âge actuel", 18, 60, 23)
duree = 67 - age

st.markdown("## 🔹 Épargne Pension & Long Terme")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 💼 Épargne Pension (EP)")
    montant_ep = st.number_input("Montant mensuel (€)", 30.0, 112.5, 87.5, step=2.5, key="ep_montant")
    taux_ep = st.slider("Taux d’intérêt (%)", 0.0, 25.0, 5.0, step=0.1, key="ep_taux")
    frais_entree_ep = st.slider("Frais d'entrée (%)", 0.0, 5.0, 3.0, step=0.1, key="ep_entree")
    frais_gestion_ep = st.slider("Frais gestion (%)", 0.0, 5.0, 1.9, step=0.1, key="ep_gestion")
    deduction_ep_pct = st.slider("Taux de déduction fiscale (%)", 0.0, 100.0, 30.0, step=1.0, key="ep_deduction")

    avantage_ep = round(montant_ep * 12 * deduction_ep_pct / 100, 2)
    total_avantage_ep = round(avantage_ep * duree, 2)
    net_mensuel_ep = round(montant_ep * (1 - deduction_ep_pct / 100), 2)
    net_annuel_ep = round(net_mensuel_ep * 12, 2)
    cap_ep = calculateur(montant_ep, duree, frais_entree_ep, frais_gestion_ep, taux_ep)

    with st.container():
        st.success(f"📌 Capital estimé à 67 ans : {cap_ep:,.2f} €")
        st.info(f"💸 Net mensuel : {net_mensuel_ep} € | Net annuel : {net_annuel_ep} €")
        st.warning(f"🧾 Avantage fiscal annuel : {avantage_ep} € | Total : {total_avantage_ep} €")

    st.line_chart(plot_evolution(montant_ep, duree, frais_entree_ep, frais_gestion_ep, taux_ep))

with col2:
    st.markdown("### 📘 Épargne Long Terme (ELT)")
    montant_elt = st.number_input("Montant mensuel (€)", 30.0, 210.83, 100.0, step=2.5, key="elt_montant")
    taux_elt = st.slider("Taux d’intérêt (%)", 0.0, 25.0, 5.0, step=0.1, key="elt_taux")
    frais_entree_elt = st.slider("Frais d'entrée (%)", 0.0, 5.0, 3.0, step=0.1, key="elt_entree")
    frais_gestion_elt = st.slider("Frais gestion (%)", 0.0, 5.0, 1.0, step=0.1, key="elt_gestion")
    deduction_elt_pct = st.slider("Taux de déduction fiscale (%)", 0.0, 100.0, 30.0, step=1.0, key="elt_deduction")

    avantage_elt = round(montant_elt * 12 * deduction_elt_pct / 100, 2)
    total_avantage_elt = round(avantage_elt * duree, 2)
    net_mensuel_elt = round(montant_elt * (1 - deduction_elt_pct / 100), 2)
    net_annuel_elt = round(net_mensuel_elt * 12, 2)
    cap_elt = calculateur(montant_elt, duree, frais_entree_elt, frais_gestion_elt, taux_elt)

    with st.container():
        st.success(f"📌 Capital estimé à 67 ans : {cap_elt:,.2f} €")
        st.info(f"💸 Net mensuel : {net_mensuel_elt} € | Net annuel : {net_annuel_elt} €")
        st.warning(f"🧾 Avantage fiscal annuel : {avantage_elt} € | Total : {total_avantage_elt} €")

    st.line_chart(plot_evolution(montant_elt, duree, frais_entree_elt, frais_gestion_elt, taux_elt))

st.markdown("---")
st.markdown("## 🟠 Épargne Non-Fiscale")

col3, col4 = st.columns(2)
with col3:
    montant_nf = st.number_input("Montant mensuel (€)", 10.0, 5000.0, 150.0, step=10.0)
    duree_nf = st.slider("Durée d'investissement (années)", 1, 99, 10)
with col4:
    montant_initial_nf = st.number_input("Montant initial (€)", 0.0, 100000.0, 0.0, step=100.0)
    taux_nf = st.slider("Taux d’intérêt (%)", 0.0, 25.0, 8.0, step=0.1)
    frais_entree_nf = st.slider("Frais d'entrée (%)", 0.0, 5.0, 3.0, step=0.1)
    frais_gestion_nf = st.slider("Frais gestion (%)", 0.0, 5.0, 1.25, step=0.1)

cap_nf = calculateur(montant_nf, duree_nf, frais_entree_nf, frais_gestion_nf, taux_nf, montant_initial_nf)
total_investi_nf = montant_nf * 12 * duree_nf + montant_initial_nf
profit_nf = round(cap_nf - total_investi_nf, 2)

with st.container():
    st.success(f"📌 Capital final après {duree_nf} ans : {cap_nf:,.2f} €")
    st.info(f"💰 Total investi : {total_investi_nf:,.2f} €")
    st.warning(f"📈 Profit net estimé : {profit_nf:,.2f} €")

st.line_chart(plot_evolution(montant_nf, duree_nf, frais_entree_nf, frais_gestion_nf, taux_nf, montant_initial_nf))
