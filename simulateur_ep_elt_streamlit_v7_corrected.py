
import streamlit as st
from math import pow
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulateur EP / ELT / Non-Fiscal", layout="wide")

def future_value_annuity(P, r, n):
    return P * ((pow(1 + r, n) - 1) / r)

def calculateur(mensuel, duree, frais_entree, frais_gestion, taux_interet, taxe_lib=None, taxe_versement=0.0, montant_initial=0.0, split_60=True):
    P_net = mensualite_nettoyee(mensuel, frais_entree, taxe_versement)
    r = (taux_interet - frais_gestion) / 12 / 100
    n_total = duree * 12

    if split_60 and duree > 37:
        n1 = 37 * 12
        n2 = (duree - 37) * 12
        cap_60 = montant_initial * pow(1 + r, n1) + future_value_annuity(P_net, r, n1)
        if taxe_lib:
            cap_60 *= (1 - taxe_lib / 100)
        capital_final = cap_60 * pow(1 + r, n2)
    else:
        capital_final = montant_initial * pow(1 + r, n_total) + future_value_annuity(P_net, r, n_total)
    return round(capital_final, 2)

def mensualite_nettoyee(P, frais_entree, taxe_versement):
    return P * (1 - frais_entree / 100) * (1 - taxe_versement / 100)

def plot_evolution(mensuel, duree, frais_entree, frais_gestion, taux, taxe_lib=None, taxe_versement=0.0, montant_initial=0.0, split_60=True):
    P_net = mensualite_nettoyee(mensuel, frais_entree, taxe_versement)
    r = (taux - frais_gestion) / 12 / 100
    total = montant_initial
    capitals = []
    for mois in range(1, duree * 12 + 1):
        total = total * (1 + r) + P_net
        if split_60 and mois == 37 * 12 and taxe_lib:
            total *= (1 - taxe_lib / 100)
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
    montant_ep = st.number_input("Montant mensuel (€)", 30.00, 112.50, 87.50, step=0.01, key="ep_montant")
    taux_ep = st.number_input("Taux d’intérêt (%)", 0.00, 25.00, 5.00, step=0.01, key="ep_taux")
    frais_entree_ep = st.number_input("Frais d'entrée (%)", 0.00, 5.00, 3.00, step=0.01, key="ep_entree")
    frais_gestion_ep = st.number_input("Frais gestion (%)", 0.00, 5.00, 1.90, step=0.01, key="ep_gestion")
    deduction_ep_pct = st.number_input("Taux de déduction fiscale (%)", 0.00, 100.00, 30.00, step=0.01, key="ep_deduction")

    avantage_ep = round(montant_ep * 12 * deduction_ep_pct / 100, 2)
    total_avantage_ep = round(avantage_ep * duree, 2)
    net_mensuel_ep = round(montant_ep * (1 - deduction_ep_pct / 100), 2)
    net_annuel_ep = round(net_mensuel_ep * 12, 2)
    cap_ep = calculateur(montant_ep, duree, frais_entree_ep, frais_gestion_ep, taux_ep, taxe_lib=8.0)

    st.success(f"📌 Capital estimé à 67 ans : {cap_ep:,.2f} €")
    st.info(f"💸 Net mensuel : {net_mensuel_ep:.2f} € | Net annuel : {net_annuel_ep:.2f} €")
    st.warning(f"🧾 Avantage fiscal annuel : {avantage_ep:.2f} € | Total : {total_avantage_ep:.2f} €")

    st.line_chart(plot_evolution(montant_ep, duree, frais_entree_ep, frais_gestion_ep, taux_ep, taxe_lib=8.0))

with col2:
    st.markdown("### 📘 Épargne Long Terme (ELT)")
    montant_elt = st.number_input("Montant mensuel (€)", 30.00, 210.83, 100.00, step=0.01, key="elt_montant")
    taux_elt = st.number_input("Taux d’intérêt (%)", 0.00, 25.00, 5.00, step=0.01, key="elt_taux")
    frais_entree_elt = st.number_input("Frais d'entrée (%)", 0.00, 5.00, 3.00, step=0.01, key="elt_entree")
    frais_gestion_elt = st.number_input("Frais gestion (%)", 0.00, 5.00, 1.00, step=0.01, key="elt_gestion")
    deduction_elt_pct = st.number_input("Taux de déduction fiscale (%)", 0.00, 100.00, 30.00, step=0.01, key="elt_deduction")

    avantage_elt = round(montant_elt * 12 * deduction_elt_pct / 100, 2)
    total_avantage_elt = round(avantage_elt * duree, 2)
    net_mensuel_elt = round(montant_elt * (1 - deduction_elt_pct / 100), 2)
    net_annuel_elt = round(net_mensuel_elt * 12, 2)
    cap_elt = calculateur(montant_elt, duree, frais_entree_elt, frais_gestion_elt, taux_elt, taxe_lib=10.0, taxe_versement=2.0)

    st.success(f"📌 Capital estimé à 67 ans : {cap_elt:,.2f} €")
    st.info(f"💸 Net mensuel : {net_mensuel_elt:.2f} € | Net annuel : {net_annuel_elt:.2f} €")
    st.warning(f"🧾 Avantage fiscal annuel : {avantage_elt:.2f} € | Total : {total_avantage_elt:.2f} €")

    st.line_chart(plot_evolution(montant_elt, duree, frais_entree_elt, frais_gestion_elt, taux_elt, taxe_lib=10.0, taxe_versement=2.0))

st.markdown("---")
st.markdown("## 🟠 Épargne Non-Fiscale")

col3, col4 = st.columns(2)
with col3:
    montant_nf = st.number_input("Montant mensuel (€)", 10.00, 5000.00, 150.00, step=1.00)
    duree_nf = st.slider("Durée d'investissement (années)", 1, 99, 10)
with col4:
    montant_initial_nf = st.number_input("Montant initial (€)", 0.00, 100000.00, 0.00, step=100.00)
    taux_nf = st.number_input("Taux d’intérêt (%)", 0.00, 25.00, 8.00, step=0.01)
    frais_entree_nf = st.number_input("Frais d'entrée (%)", 0.00, 5.00, 3.00, step=0.01)
    frais_gestion_nf = st.number_input("Frais gestion (%)", 0.00, 5.00, 1.25, step=0.01)

cap_nf = calculateur(montant_nf, duree_nf, frais_entree_nf, frais_gestion_nf, taux_nf, montant_initial_nf, taxe_versement=2.0, split_60=False)
total_investi_nf = montant_nf * 12 * duree_nf + montant_initial_nf
profit_nf = round(cap_nf - total_investi_nf, 2)

st.success(f"📌 Capital final après {duree_nf} ans : {cap_nf:,.2f} €")
st.info(f"💰 Total investi : {total_investi_nf:,.2f} €")
st.warning(f"📈 Profit net estimé : {profit_nf:,.2f} €")

st.line_chart(plot_evolution(montant_nf, duree_nf, frais_entree_nf, frais_gestion_nf, taux_nf, montant_initial_nf, taxe_versement=2.0, split_60=False))
