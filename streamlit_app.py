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

    if nom_utilisateur in ["Manon","manon","Thomas","thomas","yohan","Yohan"] :
        st.error("Vous êtes trop bête pour répondre à ce quiz 🤣😂😂")
    # Affiche un message de bienvenue personnalisé.
    # `st.success` affiche le message dans un conteneur vert pour le mettre en évidence.
    else :
        st.success(f"Bonjour, **{nom_utilisateur}** ! Le quiz commence !")

        st.header("Question 1 :")
        # Définir la question
        question = "Quel est le meilleurte type d'individu ?"

        # Définir les options de réponse
        options = ["Alpha", "Beta", "Gamma", "Omega"]

        # Afficher la question et les options de radio buttons.
        # La variable 'reponse_quiz' stockera la valeur de l'option sélectionnée.
        reponse_quiz = st.radio(
            question,
            options
        )

        # --- 3. Affichage des Résultats ou Feedback ---

        # Créer un bouton pour valider la réponse (c'est plus clair pour un quiz)
        if st.button("Valider ma réponse"):
            # Définir la bonne réponse pour la vérification
            bonne_reponse = "Omega"
            
            if reponse_quiz == bonne_reponse:
                st.success(f"Félicitations, **{nom_utilisateur+' ! Vous avez trouvé' }** ! La bonne réponse est bien {bonne_reponse}.")
            else:
                # st.warning est souvent mieux qu'st.error pour une mauvaise réponse
                st.warning(f"Dommage. Votre choix est '{reponse_quiz}'. Réessayez et peut-être que vous apprendrez quelque chose aujourd'hui 🤔")
else:
    # Affiche une instruction si le champ est vide.
    st.info("Veuillez entrer votre nom ci-dessus pour continuer.")