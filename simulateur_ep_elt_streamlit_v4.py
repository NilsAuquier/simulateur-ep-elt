
import streamlit as st
from math import pow
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Simulateur EP / ELT / Non-Fiscal", layout="centered")

def future_value_annuity(P, r, n):
    return P * ((pow(1 + r, n) - 1) / r)

def calculateur(montant, duree, frais_entree, frais_courant, taux_interet):
    montant_net = montant * (1 - frais_entree / 100)
    r = (taux_interet - frais_courant) / 12 / 100
    capital = future_value_annuity(montant_net, r, duree * 12)
    return round(capital, 2)

def plot_evolution(mensualite, duree, frais_entree, frais_courant, taux):
    mensualite_net = mensualite * (1 - frais_entree / 100)
    r = (taux - frais_courant) / 12 / 100
    capitals = []
    total = 0
    for mois in range(1, duree * 12 + 1):
        total = total * (1 + r) + mensualite_net
        capitals.append(total)
    return capitals

st.title("🧮 Simulateur Épargne Pension / Long Terme / Non-Fiscal")

age = st.slider("Âge actuel", 18, 60, 23)
duree = 67 - age

# Section EP + ELT
st.header("🔹 Épargne Pension & Long Terme")

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

cap_ep = calculateur(montant_ep, duree, frais_entree_ep, frais_gestion_ep, taux_ep)
cap_elt = calculateur(montant_elt, duree, frais_entree_elt, frais_gestion_elt, taux_elt)

st.markdown(f"**📌 Capital estimé EP à 67 ans : {cap_ep:,.2f} €**")
st.markdown(f"**📌 Capital estimé ELT à 67 ans : {cap_elt:,.2f} €**")

# Graphique EP
st.subheader("📈 Évolution capital EP")
cap_evo_ep = plot_evolution(montant_ep, duree, frais_entree_ep, frais_gestion_ep, taux_ep)
st.line_chart(cap_evo_ep)

# Graphique ELT
st.subheader("📈 Évolution capital ELT")
cap_evo_elt = plot_evolution(montant_elt, duree, frais_entree_elt, frais_gestion_elt, taux_elt)
st.line_chart(cap_evo_elt)

# Section NON-FISCAL
st.header("🟠 Épargne Non-Fiscale")

col3, col4 = st.columns(2)
with col3:
    montant_nf = st.number_input("Montant Non-Fiscal (€)", 10.0, 5000.0, 150.0, step=10.0)
    duree_nf = st.slider("Durée Non-Fiscale (années)", 1, 99, 10)
with col4:
    taux_nf = st.number_input("Taux Non-Fiscal (%)", 0.0, 25.0, 8.0, step=0.1)
    frais_entree_nf = st.number_input("Frais entrée NF (%)", 0.0, 5.0, 3.0, step=0.1)
    frais_gestion_nf = st.number_input("Frais gestion NF (%)", 0.0, 5.0, 1.25, step=0.1)

cap_nf = calculateur(montant_nf, duree_nf, frais_entree_nf, frais_gestion_nf, taux_nf)
st.markdown(f"**📌 Capital estimé Non-Fiscal après {duree_nf} ans : {cap_nf:,.2f} €**")

# Graphique NON-FISCAL
st.subheader("📈 Évolution capital Non-Fiscal")
cap_evo_nf = plot_evolution(montant_nf, duree_nf, frais_entree_nf, frais_gestion_nf, taux_nf)
st.line_chart(cap_evo_nf)

# PDF GENERATOR
st.subheader("📄 Générer un PDF personnalisé")
nom = st.text_input("Nom du client")
prenom = st.text_input("Prénom du client")
choix = st.multiselect("Quels produits inclure ?", ["EP", "ELT", "Non-Fiscal"])

if st.button("📥 Générer le PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    today = datetime.date.today().strftime("%d/%m/%Y")
    pdf.multi_cell(0, 10, f"Conseil financier personnalisé – {today}")
    pdf.multi_cell(0, 10, f"Client : {prenom} {nom}\n")

    if "EP" in choix:
        pdf.multi_cell(0, 10, f"🔹 Épargne Pension (EP)")
        pdf.multi_cell(0, 10, f"Montant : {montant_ep} €/mois pendant {duree} ans")
        pdf.multi_cell(0, 10, f"Taux : {taux_ep}% | Frais entrée : {frais_entree_ep}% | Frais gestion : {frais_gestion_ep}%")
        pdf.multi_cell(0, 10, f"Capital estimé : {cap_ep:,.2f} €\n")

    if "ELT" in choix:
        pdf.multi_cell(0, 10, f"🔸 Épargne à Long Terme (ELT)")
        pdf.multi_cell(0, 10, f"Montant : {montant_elt} €/mois pendant {duree} ans")
        pdf.multi_cell(0, 10, f"Taux : {taux_elt}% | Frais entrée : {frais_entree_elt}% | Frais gestion : {frais_gestion_elt}%")
        pdf.multi_cell(0, 10, f"Capital estimé : {cap_elt:,.2f} €\n")

    if "Non-Fiscal" in choix:
        pdf.multi_cell(0, 10, f"🟠 Épargne Non-Fiscale")
        pdf.multi_cell(0, 10, f"Montant : {montant_nf} €/mois pendant {duree_nf} ans")
        pdf.multi_cell(0, 10, f"Taux : {taux_nf}% | Frais entrée : {frais_entree_nf}% | Frais gestion : {frais_gestion_nf}%")
        pdf.multi_cell(0, 10, f"Capital estimé : {cap_nf:,.2f} €\n")

    file_name = f"conseil_{prenom}_{nom}.pdf"
    pdf.output(file_name)
    with open(file_name, "rb") as f:
        st.download_button("Télécharger le PDF", f, file_name=file_name)
