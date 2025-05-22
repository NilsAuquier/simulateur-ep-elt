
import streamlit as st
from math import pow
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Simulateur EP / ELT / Non-Fiscal", layout="centered")

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

st.title("🧮 Simulateur Épargne Pension / Long Terme / Non-Fiscal")

age = st.slider("Âge actuel", 18, 60, 23)
duree = 67 - age

# EP + ELT Section
st.header("🔹 Épargne Pension & Long Terme")

deduction_ep_pct = st.slider("Taux de déduction EP (%)", 0.0, 100.0, 30.0, step=0.5)
deduction_elt_pct = st.slider("Taux de déduction ELT (%)", 0.0, 100.0, 30.0, step=0.5)

col1, col2 = st.columns(2)
with col1:
    montant_ep = st.number_input("Montant EP (€)", 30.0, 112.5, 87.5, step=2.5)
    taux_ep = st.number_input("Taux EP (%)", 0.0, 25.0, 5.0, step=0.1)
    frais_entree_ep = st.number_input("Frais d'entrée EP (%)", 0.0, 5.0, 3.0, step=0.1)
    frais_gestion_ep = st.number_input("Frais de gestion EP (%)", 0.0, 5.0, 1.9, step=0.1)
with col2:
    montant_elt = st.number_input("Montant ELT (€)", 30.0, 210.83, 100.0, step=2.5)
    taux_elt = st.number_input("Taux ELT (%)", 0.0, 25.0, 5.0, step=0.1)
    frais_entree_elt = st.number_input("Frais d'entrée ELT (%)", 0.0, 5.0, 3.0, step=0.1)
    frais_gestion_elt = st.number_input("Frais de gestion ELT (%)", 0.0, 5.0, 1.0, step=0.1)

# Résumés
nb_annees = duree
avantage_ep = round(montant_ep * 12 * deduction_ep_pct / 100, 2)
avantage_elt = round(montant_elt * 12 * deduction_elt_pct / 100, 2)
avantage_ep_total = round(avantage_ep * nb_annees, 2)
avantage_elt_total = round(avantage_elt * nb_annees, 2)
net_mensuel_ep = round(montant_ep * (1 - deduction_ep_pct / 100), 2)
net_annuel_ep = round(net_mensuel_ep * 12, 2)
net_mensuel_elt = round(montant_elt * (1 - deduction_elt_pct / 100), 2)
net_annuel_elt = round(net_mensuel_elt * 12, 2)

cap_ep = calculateur(montant_ep, duree, frais_entree_ep, frais_gestion_ep, taux_ep)
cap_elt = calculateur(montant_elt, duree, frais_entree_elt, frais_gestion_elt, taux_elt)

st.subheader("📊 Résumé EP")
st.markdown(f"- 💰 Montant net mensuel : {net_mensuel_ep} €")
st.markdown(f"- 💰 Montant net annuel : {net_annuel_ep} €")
st.markdown(f"- 🧾 Déduction annuelle : {avantage_ep} €")
st.markdown(f"- 🧾 Déduction totale : {avantage_ep_total} €")
st.markdown(f"- 📅 Durée : {nb_annees} ans")
st.markdown(f"**📌 Capital estimé à 67 ans : {cap_ep:,.2f} €**")
st.line_chart(plot_evolution(montant_ep, duree, frais_entree_ep, frais_gestion_ep, taux_ep))

st.subheader("📊 Résumé ELT")
st.markdown(f"- 💰 Montant net mensuel : {net_mensuel_elt} €")
st.markdown(f"- 💰 Montant net annuel : {net_annuel_elt} €")
st.markdown(f"- 🧾 Déduction annuelle : {avantage_elt} €")
st.markdown(f"- 🧾 Déduction totale : {avantage_elt_total} €")
st.markdown(f"- 📅 Durée : {nb_annees} ans")
st.markdown(f"**📌 Capital estimé à 67 ans : {cap_elt:,.2f} €**")
st.line_chart(plot_evolution(montant_elt, duree, frais_entree_elt, frais_gestion_elt, taux_elt))

# NON-FISCAL Section
st.header("🟠 Épargne Non-Fiscale")

col3, col4 = st.columns(2)
with col3:
    montant_nf = st.number_input("Montant mensuel Non-Fiscal (€)", 10.0, 5000.0, 150.0, step=10.0)
    duree_nf = st.slider("Durée (années)", 1, 99, 10)
with col4:
    montant_initial_nf = st.number_input("Montant initial investi (€)", 0.0, 100000.0, 0.0, step=100.0)
    taux_nf = st.number_input("Taux (%)", 0.0, 25.0, 8.0, step=0.1)
    frais_entree_nf = st.number_input("Frais d'entrée (%)", 0.0, 5.0, 3.0, step=0.1)
    frais_gestion_nf = st.number_input("Frais gestion (%)", 0.0, 5.0, 1.25, step=0.1)

cap_nf = calculateur(montant_nf, duree_nf, frais_entree_nf, frais_gestion_nf, taux_nf, montant_initial_nf)
total_investi_nf = montant_nf * 12 * duree_nf + montant_initial_nf
profit_nf = round(cap_nf - total_investi_nf, 2)

st.subheader("📊 Résumé Non-Fiscal")
st.markdown(f"- 💰 Total investi : {total_investi_nf:,.2f} €")
st.markdown(f"- 📈 Capital final : {cap_nf:,.2f} €")
st.markdown(f"- 💹 Profit net : {profit_nf:,.2f} €")
st.line_chart(plot_evolution(montant_nf, duree_nf, frais_entree_nf, frais_gestion_nf, taux_nf, montant_initial_nf))
