import streamlit as st
import random
import os # Importation du module os pour une meilleure gestion des chemins (si nécessaire, mais pas obligatoire ici)

# --- CONFIGURATION DES CHEMINS D'IMAGE ---
# Assurez-vous que le dossier 'images' existe à côté de votre script Streamlit
IMAGE_FOLDER = "images" 

# Définir l'image correcte
bonne_image = "Etienne"

# Définir les chemins d'accès (paths) pour chaque image
# ASSUREZ-VOUS QUE CES NOMS DE FICHIERS CORRESPONDENT À CEUX DANS VOTRE DOSSIER !
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

st.title("Application de Bienvenue Simple 👋")

# --- Interface Utilisateur pour la Saisie ---
nom_utilisateur = st.text_input("Veuillez entrer votre nom :")

# --- Logique Principale ---

if nom_utilisateur:
    # Cas des noms exclus
    if nom_utilisateur.lower() in ["manon", "thomas", "yohan"]:
        st.error("Vous êtes trop bête pour répondre à ce quiz 🤣😂😂")
        st.session_state.captcha_valide = False 
    else:
        st.success(f"Bonjour, **{nom_utilisateur}** ! Le quiz commence !")

        # --- NOUVELLE LOGIQUE : VÉRIFICATION ROBOT ---

        st.markdown("### Vérification de sécurité")
        checkbox_value = st.checkbox("Je ne suis pas un robot", 
                                     value=st.session_state.captcha_valide, 
                                     disabled=st.session_state.captcha_valide, 
                                     key="robot_check")

        if checkbox_value and not st.session_state.captcha_valide:
            st.warning(f"Veuillez sélectionner la ** meilleure personne ** pour continuer.")

            images_liste = list(images_choix.keys())
            random.shuffle(images_liste)

            # --- Affichage des 4 images simulées dans 4 colonnes ---
            cols = st.columns(len(images_liste))
            selection_image = st.empty()

            for i, image_nom in enumerate(images_liste):
                with cols[i]:
                    # NOUVEAU : Utilisation de st.image avec le chemin du fichier
                    image_path = images_choix[image_nom]
                    
                    # Vérification si le fichier existe pour éviter une erreur Streamlit
                    if os.path.exists(image_path):
                        # Vous pouvez ajuster 'width' pour la taille désirée
                        st.image(image_path, caption=image_nom, width=120) 
                    else:
                        st.error(f"Fichier non trouvé : {image_path}")
                        st.stop() # Arrête le script si un fichier manque
                        
                    # Créer un bouton pour la sélection
                    if st.button("Choisir", key=f"btn_{i}"):
                        selection_image.markdown(f"Vous avez choisi **{image_nom}**")
                        
                        # Vérification de la réponse
                        if image_nom == bonne_image:
                            st.session_state.captcha_valide = True
                            st.success("🤖 Vérification réussie ! Vous pouvez continuer.")
                            st.rerun() 
                        else:
                            st.session_state.captcha_valide = False
                            st.error("❌ Mauvaise image. Veuillez réessayer.")
                            st.rerun()

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