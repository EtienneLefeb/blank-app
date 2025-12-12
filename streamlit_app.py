import streamlit as st
import random
import os

# --- CONFIGURATION DES CHEMINS D'IMAGE ---
IMAGE_FOLDER = "images" 
bonne_image = "Etienne" 

# Définir les chemins d'accès (paths) pour chaque image
# (Gardez votre configuration d'images telle quelle)
images_choix = {
    "Etienne": os.path.join(IMAGE_FOLDER, "etienne.jpg"),
    "Armand": os.path.join(IMAGE_FOLDER, "armand.jpg"),
    "Thomas": os.path.join(IMAGE_FOLDER, "thomas.jpg"),
    "Manon": os.path.join(IMAGE_FOLDER, "manon.jpg"),
    "Yohan": os.path.join(IMAGE_FOLDER, "yohan.jpg")
}
# ---------------------------------------------


# --- 1. Initialisation de l'État de Session ---
if 'captcha_valide' not in st.session_state:
    st.session_state.captcha_valide = False
# Ajout d'une variable pour stocker le choix de l'utilisateur
if 'choix_captcha' not in st.session_state:
    st.session_state.choix_captcha = None

st.title("Application de Bienvenue Simple 👋")

# --- Interface Utilisateur pour la Saisie ---
nom_utilisateur = st.text_input("Veuillez entrer votre nom :")

# --- Logique Principale ---

if nom_utilisateur:
    # Cas des noms exclus
    if nom_utilisateur.lower() in ["manon", "thomas", "yohan"]:
        st.error("Vous êtes trop bête pour répondre à ce quiz 🤣😂😂")
        st.session_state.captcha_valide = False
        st.session_state.choix_captcha = None # Réinitialisation du choix
    else:
        st.success(f"Bonjour, **{nom_utilisateur}** ! Le quiz commence !")

        # --- NOUVELLE LOGIQUE : VÉRIFICATION ROBOT ---

        st.markdown("### Vérification de sécurité")
        # Le checkbox est désactivé si le captcha est valide
        checkbox_value = st.checkbox("Je ne suis pas un robot", 
                                     value=st.session_state.captcha_valide, 
                                     disabled=st.session_state.captcha_valide, 
                                     key="robot_check")

        if checkbox_value and not st.session_state.captcha_valide:
            st.warning(f"Veuillez sélectionner la **{"meilleure personne"}** pour continuer.")

            images_liste = list(images_choix.keys())
            # On stocke l'ordre mélangé dans l'état de session pour éviter qu'il change
            # à chaque clic de bouton (ce qui rendrait la vérification confuse).
            if 'images_melangees' not in st.session_state:
                random.shuffle(images_liste)
                st.session_state.images_melangees = images_liste
            
            # Utiliser l'ordre mélangé stocké
            images_a_afficher = st.session_state.images_melangees

            # --- Affichage des images dans les colonnes ---
            cols = st.columns(len(images_a_afficher))

            # Fonction pour gérer le clic sur le bouton
            def verifier_choix(choix):
                st.session_state.choix_captcha = choix # Stocke le choix
                
                # Vérification immédiate
                if choix == bonne_image:
                    st.session_state.captcha_valide = True
                    st.success("🤖 Vérification réussie ! Vous pouvez continuer.")
                    # Inutile de rerun ici, le code continue et affiche le quiz
                else:
                    st.session_state.captcha_valide = False
                    st.error(f"❌ Mauvaise personne sélectionnée : {choix}. Veuillez réessayer.")
                    # On retire le choix temporaire et on rerunn
                    st.session_state.choix_captcha = None
                    # On réinitialise aussi le mélange pour avoir un nouvel ordre
                    del st.session_state.images_melangees
                    st.rerun()

            
            for i, image_nom in enumerate(images_a_afficher):
                with cols[i]:
                    image_path = images_choix[image_nom]
                    
                    if os.path.exists(image_path):
                        st.image(image_path, caption=image_nom, width=120) 
                    else:
                        st.error(f"Fichier non trouvé : {image_path}")
                        st.stop()
                        
                    # Créer un bouton pour la sélection
                    # Le callback 'on_click' appelle la fonction verifier_choix
                    if st.button("Choisir", key=f"btn_{i}", on_click=verifier_choix, args=(image_nom,)):
                        pass # Le traitement est fait dans la fonction verifier_choix

        # 3. Le Quiz n'apparaît que si la vérification est réussie
        if st.session_state.captcha_valide:
            st.header("Question 1 :")
            question = "Quel est le meilleurte type d'individu ?"
            options = ["Alpha", "Beta", "Gamma", "Omega"]

            reponse_quiz = st.radio(question, options, key="quiz_q1")

            if st.button("Valider ma réponse", key="validate_quiz"):
                bonne_reponse = "Omega"
                
                if reponse_quiz == bonne_reponse:
                    st.balloons() 
                    st.success(f"Félicitations, **{nom_utilisateur}** ! La bonne réponse est bien **{bonne_reponse}**.")
                else:
                    st.warning(f"Dommage. Votre choix est '{reponse_quiz}'. Réessayez et peut-être que vous apprendrez quelque chose aujourd'hui 🤔")
        else:
            st.info("Veuillez valider la vérification de sécurité pour accéder au quiz.")


else:
    st.info("Veuillez entrer votre nom ci-dessus pour continuer.")