
import streamlit as st
from math import pow

def future_value_annuity(P, r, n):
    return P * ((pow(1 + r, n) - 1) / r)

def calculateur_ep_elt(montant_mensuel, duree_annees, frais_entree, frais_courant_annuel, taux_interet_annuel, taxe_lib_60):
    mois_total = duree_annees * 12
    r_net = (taux_interet_annuel - frais_courant_annuel) / 12 / 100
    montant_net = montant_mensuel * (1 - frais_entree / 100)

    if duree_annees > 37:
        n1 = 37 * 12
        fv_60 = future_value_annuity(montant_net, r_net, n1)
        fv_60_net = fv_60 * (1 - taxe_lib_60 / 100)
        n2 = (duree_annees - 37) * 12
        fv_67 = fv_60_net * pow(1 + r_net, n2)
        return round(fv_67, 2), round(fv_60_net, 2)
    else:
        fv_total = future_value_annuity(montant_net, r_net, mois_total)
        return round(fv_total, 2), round(fv_total * (1 - taxe_lib_60 / 100), 2)

st.title("Simulateur Épargne Pension / Épargne à Long Terme")

produit = st.selectbox("Choisissez un produit :", ["Épargne Pension", "Épargne à Long Terme"])

montant = st.slider("Montant mensuel brut (€)", min_value=30.0, max_value=250.0, step=2.5)

duree = st.slider("Durée de l'investissement (en années)", min_value=5, max_value=47, value=44)

taux = st.slider("Taux d'intérêt annuel moyen (%)", min_value=3.0, max_value=10.0, value=5.0, step=0.1)

if produit == "Épargne Pension":
    frais_courant = 1.9
    taxe_lib = 8
else:
    frais_courant = 1.0
    taxe_lib = 10

capital_final, capital_a_60 = calculateur_ep_elt(
    montant_mensuel=montant,
    duree_annees=duree,
    frais_entree=3.0,
    frais_courant_annuel=frais_courant,
    taux_interet_annuel=taux,
    taxe_lib_60=taxe_lib
)

st.subheader("Résultats de la simulation")
st.write(f"Montant net estimé à 60 ans (après taxe de {taxe_lib}%) : **{capital_a_60:,.2f} €**")
st.write(f"Montant net estimé à {duree + (23 - (67 - duree))} ans (fin d'investissement) : **{capital_final:,.2f} €**")
