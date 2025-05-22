
import streamlit as st
from math import pow
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Simulateur EP / ELT", layout="centered")

def future_value_annuity(P, r, n):
    return P * ((pow(1 + r, n) - 1) / r)

def calculateur(montant, duree, frais_entree, frais_courant, taux_interet, taxe_60):
    montant_net = montant * (1 - frais_entree / 100)
    r = (taux_interet - frais_courant) / 12 / 100
    n1 = min(duree, 37) * 12
    capital_60 = future_value_annuity(montant_net, r, n1)
    capital_apres_taxe = capital_60 * (1 - taxe_60 / 100)
    if duree > 37:
        n2 = (duree - 37) * 12
        capital_67 = capital_apres_taxe * pow(1 + r, n2)
    else:
        capital_67 = capital_apres_taxe
    return round(capital_60, 2), round(capital_67, 2)

def calc_avantage_ep(montant):
    if montant <= 87.5:
        return round(montant * 12 * 0.30, 2)
    elif montant <= 112.5:
        return round(montant * 12 * 0.25, 2)
    return 0.0

def calc_avantage_elt(montant):
    return round(montant * 12 * 0.30, 2)

def plot_evolution(mensualite, duree, frais_entree, frais_courant, taux, taxe):
    mensualite_net = mensualite * (1 - frais_entree / 100)
    r = (taux - frais_courant) / 12 / 100
    capitals = []
    total = 0
    for mois in range(1, duree * 12 + 1):
        total = total * (1 + r) + mensualite_net
        if mois == 37 * 12:
            total *= (1 - taxe / 100)
        capitals.append(total)
    return capitals

# UI
st.title("🧮 Simulateur Épargne Pension (EP) & Épargne à Long Terme (ELT)")
st.markdown("Cet outil vous permet d’estimer le capital futur, les avantages fiscaux et le coût net d’une épargne pension ou long terme.")

age = st.number_input("Âge actuel", min_value=18, max_value=60, value=23)
duree = 67 - age
taux = st.slider("Taux d'intérêt annuel moyen (%)", 3.0, 10.0, 5.0, step=0.1)
frais_entree = st.slider("Frais d'entrée (%)", 0.0, 5.0, 3.0, step=0.1)
frais_courant = st.slider("Frais de gestion annuels (%)", 0.0, 2.0, 1.9, step=0.1)

st.header("🔹 Épargne Pension (EP)")
montant_ep = st.slider("Montant mensuel EP (€)", 30.0, 112.5, 87.5, step=2.5)
avantage_ep = calc_avantage_ep(montant_ep)
cout_net_ep = round((montant_ep * 12) - avantage_ep, 2)
cap_60_ep, cap_67_ep = calculateur(montant_ep, duree, frais_entree, frais_courant, taux, 8)

st.markdown(f"""
- 🧾 **Avantage fiscal annuel** : {avantage_ep} €
- 💸 **Coût net annuel réel** : {cout_net_ep} €
- 📈 **Capital estimé à 60 ans** (avant poursuite) : {cap_60_ep:,.2f} €
- 🏁 **Capital estimé à 67 ans** : **{cap_67_ep:,.2f} €**
""")

st.divider()

st.header("🔸 Épargne à Long Terme (ELT)")
frais_courant_elt = st.slider("Frais de gestion ELT (%)", 0.0, 2.0, 1.0, step=0.1)
montant_elt = st.slider("Montant mensuel ELT (€)", 30.0, 210.83, 100.0, step=2.5)
avantage_elt = calc_avantage_elt(montant_elt)
cout_net_elt = round((montant_elt * 12) - avantage_elt, 2)
cap_60_elt, cap_67_elt = calculateur(montant_elt, duree, frais_entree, frais_courant_elt, taux, 10)

st.markdown(f"""
- 🧾 **Avantage fiscal annuel** : {avantage_elt} €
- 💸 **Coût net annuel réel** : {cout_net_elt} €
- 📈 **Capital estimé à 60 ans** (avant poursuite) : {cap_60_elt:,.2f} €
- 🏁 **Capital estimé à 67 ans** : **{cap_67_elt:,.2f} €**
""")

# Graphique
st.subheader("📊 Évolution du capital")
cap_ep = plot_evolution(montant_ep, duree, frais_entree, frais_courant, taux, 8)
cap_elt = plot_evolution(montant_elt, duree, frais_entree, frais_courant_elt, taux, 10)

fig, ax = plt.subplots()
ax.plot(range(1, len(cap_ep)+1), cap_ep, label="EP", linewidth=2)
ax.plot(range(1, len(cap_elt)+1), cap_elt, label="ELT", linewidth=2)
ax.set_xlabel("Mois")
ax.set_ylabel("Capital (€)")
ax.legend()
st.pyplot(fig)

# PDF export
st.subheader("🧾 Générer un résumé PDF")
if st.button("📄 Télécharger le résumé PDF"):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"""
Simulateur EP / ELT - Résumé personnalisé

Âge actuel : {age} ans
Durée jusqu'à 67 ans : {duree} ans

ÉPARGNE PENSION (EP)
- Montant mensuel : {montant_ep} €
- Avantage fiscal annuel : {avantage_ep} €
- Coût net annuel : {cout_net_ep} €
- Capital estimé à 60 ans : {cap_60_ep} €
- Capital estimé à 67 ans : {cap_67_ep} €

ÉPARGNE LONG TERME (ELT)
- Montant mensuel : {montant_elt} €
- Avantage fiscal annuel : {avantage_elt} €
- Coût net annuel : {cout_net_elt} €
- Capital estimé à 60 ans : {cap_60_elt} €
- Capital estimé à 67 ans : {cap_67_elt} €
""")
    pdf.output("resume_ep_elt.pdf")
    with open("resume_ep_elt.pdf", "rb") as f:
        st.download_button("📥 Télécharger le PDF", f, file_name="resume_ep_elt.pdf")

