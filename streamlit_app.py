import streamlit as st

# Définition du titre de l'application
st.title("Application de Bienvenue Simple 👋")

# --- Interface Utilisateur pour la Saisie ---

# Utiliser `st.text_input` pour obtenir une saisie de texte de l'utilisateur
# Le premier argument est l'étiquette (label) affichée au-dessus du champ.
nom_utilisateur = st.text_input("Veuillez entrer votre nom :")

# --- Logique et Affichage du Résultat ---

# On vérifie si l'utilisateur a entré quelque chose (la chaîne n'est pas vide)
if nom_utilisateur:
    # Affiche un message de bienvenue personnalisé.
    # `st.success` affiche le message dans un conteneur vert pour le mettre en évidence.
    st.success(f"Bonjour, **{nom_utilisateur}** ! Bienvenue sur l'application Streamlit.")
else:
    # Affiche une instruction si le champ est vide.
    st.info("Veuillez entrer votre nom ci-dessus pour continuer.")