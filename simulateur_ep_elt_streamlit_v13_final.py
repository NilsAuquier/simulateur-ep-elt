
# simulateur_ep_elt_streamlit_v12.py
import streamlit as st
from math import pow
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Simulateur EP / ELT / Non-Fiscal", layout="wide")

def future_value_annuity(P, r, n):
    return P * ((pow(1 + r, n) - 1) / r)

def mensualite_nettoyee(P, frais_entree, taxe_versement):
    return P * (1 - frais_entree / 100) * (1 - taxe_versement / 100)

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

age = st.slider("Age actuel", 18, 60, 23)
duree = 67 - age

st.markdown("## Epargne Pension et Long Terme")
col1, col2 = st.columns(2)
with col1:
    montant_ep = st.number_input("Montant EP mensuel (€)", 30.00, 112.50, 87.50, step=0.01)
    taux_ep = st.number_input("Taux EP (%)", 0.00, 25.00, 5.00, step=0.01)
    frais_entree_ep = st.number_input("Frais entree EP (%)", 0.00, 5.00, 3.00, step=0.01)
    frais_gestion_ep = st.number_input("Frais gestion EP (%)", 0.00, 5.00, 1.90, step=0.01)
    deduction_ep_pct = st.number_input("Deduction EP (%)", 0.00, 100.00, 30.00, step=0.01)
    avantage_ep = round(montant_ep * 12 * deduction_ep_pct / 100, 2)
    total_avantage_ep = round(avantage_ep * duree, 2)
    net_mensuel_ep = round(montant_ep * (1 - deduction_ep_pct / 100), 2)
    net_annuel_ep = round(net_mensuel_ep * 12, 2)
    cap_ep = calculateur(montant_ep, duree, frais_entree_ep, frais_gestion_ep, taux_ep, taxe_lib=8.0)
    st.success(f"Capital estime a 67 ans : {cap_ep:,.2f} €")
    st.info(f"Net mensuel : {net_mensuel_ep:.2f} € | Net annuel : {net_annuel_ep:.2f} €")
    st.warning(f"Avantage fiscal annuel : {avantage_ep:.2f} € | Total : {total_avantage_ep:.2f} €")
    st.line_chart(plot_evolution(montant_ep, duree, frais_entree_ep, frais_gestion_ep, taux_ep, taxe_lib=8.0))

with col2:
    montant_elt = st.number_input("Montant ELT mensuel (€)", 30.00, 210.83, 100.00, step=0.01)
    taux_elt = st.number_input("Taux ELT (%)", 0.00, 25.00, 5.00, step=0.01)
    frais_entree_elt = st.number_input("Frais entree ELT (%)", 0.00, 5.00, 3.00, step=0.01)
    frais_gestion_elt = st.number_input("Frais gestion ELT (%)", 0.00, 5.00, 1.00, step=0.01)
    deduction_elt_pct = st.number_input("Deduction ELT (%)", 0.00, 100.00, 30.00, step=0.01)
    avantage_elt = round(montant_elt * 12 * deduction_elt_pct / 100, 2)
    total_avantage_elt = round(avantage_elt * duree, 2)
    net_mensuel_elt = round(montant_elt * (1 - deduction_elt_pct / 100), 2)
    net_annuel_elt = round(net_mensuel_elt * 12, 2)
    cap_elt = calculateur(montant_elt, duree, frais_entree_elt, frais_gestion_elt, taux_elt, taxe_lib=10.0, taxe_versement=2.0)
    st.success(f"Capital estime a 67 ans : {cap_elt:,.2f} €")
    st.info(f"Net mensuel : {net_mensuel_elt:.2f} € | Net annuel : {net_annuel_elt:.2f} €")
    st.warning(f"Avantage fiscal annuel : {avantage_elt:.2f} € | Total : {total_avantage_elt:.2f} €")
    st.line_chart(plot_evolution(montant_elt, duree, frais_entree_elt, frais_gestion_elt, taux_elt, taxe_lib=10.0, taxe_versement=2.0))

st.markdown("## Epargne Non Fiscale")
col3, col4 = st.columns(2)
with col3:
    montant_nf = st.number_input("Montant NF mensuel (€)", 10.00, 5000.00, 150.00, step=1.00)
    duree_nf = st.slider("Duree investissement (ans)", 1, 99, 10)
with col4:
    montant_initial_nf = st.number_input("Montant initial (€)", 0.00, 100000.00, 0.00, step=100.00)
    taux_nf = st.number_input("Taux NF (%)", 0.00, 25.00, 8.00, step=0.01)
    frais_entree_nf = st.number_input("Frais entree NF (%)", 0.00, 5.00, 3.00, step=0.01)
    frais_gestion_nf = st.number_input("Frais gestion NF (%)", 0.00, 5.00, 1.25, step=0.01)

cap_nf = calculateur(montant_nf, duree_nf, frais_entree_nf, frais_gestion_nf, taux_nf, montant_initial_nf, taxe_versement=2.0, split_60=False)
total_investi_nf = montant_nf * 12 * duree_nf + montant_initial_nf
profit_nf = round(cap_nf - total_investi_nf, 2)
st.success(f"Capital final apres {duree_nf} ans : {cap_nf:,.2f} €")
st.info(f"Total investi : {total_investi_nf:,.2f} €")
st.warning(f"Profit net estime : {profit_nf:,.2f} €")
st.line_chart(plot_evolution(montant_nf, duree_nf, frais_entree_nf, frais_gestion_nf, taux_nf, montant_initial_nf, taxe_versement=2.0, split_60=False))



# PDF GENERATION
st.markdown("---")
st.markdown("## 📄 Générer un PDF récapitulatif personnalisé")

nom = st.text_input("Nom du client")
prenom = st.text_input("Prénom du client")
produits_selectionnes = st.multiselect("Produits à inclure dans le PDF :", ["EP", "ELT", "Epargne non fiscale"])
taux_msci = st.number_input("Taux moyen historique MSCI World (%)", 0.0, 20.0, 8.53, step=0.01)
date_rdv = st.date_input("Date du prochain rendez-vous")

if st.button("📥 Générer le PDF récapitulatif"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 11)

    pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Bonjour {prenom} {nom},\n\nJ’espère que vous allez bien.\n")
    pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")("Suite à notre récent entretien, au cours duquel nous avons réalisé une analyse approfondie de votre situation financière, et après évaluation par un conseiller agréé, je tiens à vous transmettre un récapitulatif des points essentiels abordés ainsi que des recommandations adaptées à vos besoins et à vos objectifs à long terme.\n")
    pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")("Ces propositions s’inscrivent dans une approche personnalisée, en tenant compte des informations que vous nous avez communiquées, afin de vous accompagner au mieux dans l’optimisation et la protection de vos intérêts financiers.\n")

    if "EP" in produits_selectionnes:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, "ÉPARGNES PENSION", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Montants : {montant_ep:.2f} € BRUTS")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Coût net mensuel : {net_mensuel_ep:.2f} € / mois")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Déductibilité : {avantage_ep:.2f} € / an")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Durée de l'investissement - {duree} ans : âge terme - 67 ans")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")("Frais d'entrée : 3,00 %")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")("Frais de Gestion (annuels) : 1,90 % (EP/ELT Europe Equity AXA); 0,85 % (EP/ELT Multifunds AXA); 1,25 % (EP/ELT iShares P&V).")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")("Rendement attendu : Entre 5,00 % et 10,00 %.")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Dans votre cas, nous partons d'un capital investi de {(montant_ep * 12 * duree):,.2f} € pour atteindre un montant estimé de {cap_ep:,.2f} € au terme du contrat, taxes et frais compris. L'avantage fiscal perçu représente quant à lui {total_avantage_ep:,.2f} €.\n")

    if "ELT" in produits_selectionnes:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, "ÉPARGNES LONG TERME", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Montants : {montant_elt:.2f} € BRUTS")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Coût net mensuel : {net_mensuel_elt:.2f} € / mois")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Déductibilité : {avantage_elt:.2f} € / an")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Durée de l'investissement - {duree} ans : âge terme - 67 ans")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")("Frais d'entrée : 3,00 %")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")("Frais de Gestion (annuels) : 1,90 %, 0,85 %, 0,85 %, 0,85 %, 1,00 %, 1,25 % selon fonds sélectionnés.")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")("Rendement attendu : Entre 5,00 % et 10,00 %.")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Dans votre cas, nous partons d'un capital investi de {(montant_elt * 12 * duree):,.2f} € pour atteindre un montant estimé de {cap_elt:,.2f} € au terme du contrat, taxes et frais compris. L'avantage fiscal perçu représente quant à lui {total_avantage_elt:,.2f} €.\n")

    if "Epargne non fiscale" in produits_selectionnes:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, "ÉPARGNE NON-FISCALE", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Montants : {montant_nf:.2f} € BRUTS")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")("Frais d'entrée : 3,00 %")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")("Frais de Gestion (annuels) : 1,25 %")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")("Rendement attendu : Entre 8,00 % et 14,00 %.")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Durée de l'investissement - {duree_nf} ans : âge terme - {age + duree_nf} ans.")
        pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Dans votre cas, nous partons d'un capital investi de {total_investi_nf:,.2f} € pour atteindre un montant estimé de {cap_nf:,.2f} € au terme des {duree_nf} années, taxes et frais compris.\n")

    pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"Je vous rappelle que ces calculs ont été réalisés sur base d'un rendement fictif de {taux_msci:.2f} %. Sur une période d'environ 30 ans, il convient plutôt d'envisager un rendement final de l'ordre de 5,00 % à 10,00 %, ces 37 dernières années le rendement étant de 8,53 % en moyenne par an (MSCI World Index).\n")
    pdf.multi_cell(0, 10, lambda s: s.encode("latin-1", "replace").decode("latin-1")(f"POUR NOTRE PROCHAIN RENDEZ-VOUS : {date_rdv.strftime('%A %d %B %Y')}")

    file_name = f"recommandations_{prenom}_{nom}.pdf"
    pdf.output(f"/mnt/data/{file_name}")
    st.success("📄 PDF généré avec succès !")
    with open(f"/mnt/data/{file_name}", "rb") as f:
        st.download_button("📥 Télécharger le PDF", f, file_name=file_name)
