
import streamlit as st
from math import pow
import matplotlib.pyplot as plt
from fpdf import FPDF

st.set_page_config(page_title="Simulateur EP / ELT / Non-Fiscal", layout="centered")

def future_value_annuity(P, r, n):
    return P * ((pow(1 + r, n) - 1) / r)

def calculateur(montant, duree, frais_entree, frais_courant, taux_interet, taxe_60=None):
    montant_net = montant * (1 - frais_entree / 100)
    r = (taux_interet - frais_courant) / 12 / 100
    n1 = min(duree, 37) * 12
    capital_60 = future_value_annuity(montant_net, r, n1)
    if taxe_60 is not None:
        capital_apres_taxe = capital_60 * (1 - taxe_60 / 100)
    else:
        capital_apres_taxe = capital_60
    if duree > 37:
        n2 = (duree - 37) * 12
        capital_67 = capital_apres_taxe * pow(1 + r, n2)
    else:
        capital_67 = capital_apres_taxe
    return round(capital_60, 2), round(capital_67, 2)

def plot_evolution(mensualite, duree, frais_entree, frais_courant, taux, taxe=None):
    mensualite_net = mensualite * (1 - frais_entree / 100)
    r = (taux - frais_courant) / 12 / 100
    capitals = []
    total = 0
    for mois in range(1, duree * 12 + 1):
        total = total * (1 + r) + mensualite_net
        if taxe and mois == 37 * 12:
            total *= (1 - taxe / 100)
        capitals.append(total)
    return capitals

st.title("🧮 Simulateur Épargne Pension / Long Terme / Non-Fiscal")

st.markdown("Ce simulateur vous permet d’estimer les gains d’une stratégie d’épargne à long terme, avec ou sans avantage fiscal.")

# EP
st.header("🔹 Épargne Pension (EP)")
col1, col2 = st.columns(2)
with col1:
    montant_ep = st.slider("Montant mensuel EP (€)", 30.0, 112.5, 87.5, step=2.5)
with col2:
    taux_ep = st.number_input("Taux d’intérêt EP (%)", min_value=0.0, max_value=25.0, value=5.0, step=0.1)

col3, col4 = st.columns(2)
with col3:
    frais_entree_ep = st.number_input("Frais d'entrée EP (%)", 0.0, 5.0, 3.0, step=0.1)
with col4:
    frais_gestion_ep = st.number_input("Frais de gestion EP (%)", 0.0, 5.0, 1.9, step=0.1)

age = st.slider("Âge actuel", 18, 60, 23)
duree_ep = 67 - age

def calc_avantage_ep(montant):
    if montant <= 87.5:
        return round(montant * 12 * 0.30, 2)
    elif montant <= 112.5:
        return round(montant * 12 * 0.25, 2)
    return 0.0

avantage_ep = calc_avantage_ep(montant_ep)
cout_net_ep = round(montant_ep * 12 - avantage_ep, 2)
cap_60_ep, cap_67_ep = calculateur(montant_ep, duree_ep, frais_entree_ep, frais_gestion_ep, taux_ep, taxe_60=8)

st.markdown(f"""
- 🧾 Avantage fiscal : {avantage_ep} €
- 💸 Coût net annuel : {cout_net_ep} €
- 📈 Capital à 60 ans : {cap_60_ep:,.2f} €
- 🏁 Capital à 67 ans : **{cap_67_ep:,.2f} €**
""")

# ELT
st.header("🔸 Épargne à Long Terme (ELT)")
col5, col6 = st.columns(2)
with col5:
    montant_elt = st.slider("Montant mensuel ELT (€)", 30.0, 210.83, 100.0, step=2.5)
with col6:
    taux_elt = st.number_input("Taux d’intérêt ELT (%)", min_value=0.0, max_value=25.0, value=5.0, step=0.1)

col7, col8 = st.columns(2)
with col7:
    frais_entree_elt = st.number_input("Frais d'entrée ELT (%)", 0.0, 5.0, 3.0, step=0.1)
with col8:
    frais_gestion_elt = st.number_input("Frais de gestion ELT (%)", 0.0, 5.0, 1.0, step=0.1)

avantage_elt = round(montant_elt * 12 * 0.30, 2)
cout_net_elt = round(montant_elt * 12 - avantage_elt, 2)
cap_60_elt, cap_67_elt = calculateur(montant_elt, duree_ep, frais_entree_elt, frais_gestion_elt, taux_elt, taxe_60=10)

st.markdown(f"""
- 🧾 Avantage fiscal : {avantage_elt} €
- 💸 Coût net annuel : {cout_net_elt} €
- 📈 Capital à 60 ans : {cap_60_elt:,.2f} €
- 🏁 Capital à 67 ans : **{cap_67_elt:,.2f} €**
""")

# Non fiscal
st.header("🟠 Épargne Non-Fiscale")
col9, col10 = st.columns(2)
with col9:
    montant_nf = st.slider("Montant mensuel (€)", 10.0, 5000.0, 150.0, step=10.0)
with col10:
    duree_nf = st.slider("Durée en années", 1, 99, 10)

col11, col12, col13 = st.columns(3)
with col11:
    taux_nf = st.number_input("Taux d’intérêt (%)", 0.0, 25.0, 8.0, step=0.1)
with col12:
    frais_entree_nf = st.number_input("Frais d'entrée (%)", 0.0, 5.0, 3.0, step=0.1)
with col13:
    frais_gestion_nf = st.number_input("Frais de gestion (%)", 0.0, 5.0, 1.25, step=0.1)

_, cap_nf = calculateur(montant_nf, duree_nf, frais_entree_nf, frais_gestion_nf, taux_nf, taxe_60=None)

st.markdown(f"""
- 💰 Capital estimé après {duree_nf} ans : **{cap_nf:,.2f} €**
""")
