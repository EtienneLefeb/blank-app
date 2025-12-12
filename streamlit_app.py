import streamlit as st
import random
import os

# --- CONFIGURATION DES CHEMINS D'IMAGE (Identique) ---
IMAGE_FOLDER = "images" 
bonne_image = "Etienne" 

images_choix = {
    "Etienne": os.path.join(IMAGE_FOLDER, "etienne.jpg"),
    "Armand": os.path.join(IMAGE_FOLDER, "armand.jpg"),
    "Thomas": os.path.join(IMAGE_FOLDER, "thomas.jpg"),
    "Manon": os.path.join(IMAGE_FOLDER, "manon.jpg"),
    "Yohan": os.path.join(IMAGE_FOLDER, "yohan.jpg")
}
# ---------------------------------------------

# --- DÉFINITION DU QUIZ DE PERSONNALITÉ (Identique) ---
QUIZ_QUESTIONS = {
    1: {
        "question": "Quel est votre mode de déplacement préféré ?",
        "options": {
            "A": "Ramper lentement, sans se presser.",
            "B": "Sauter partout et faire du bruit.",
            "C": "Nager dans l'eau salée, loin de tout.",
            "D": "Marcher en ligne droite, porter 10 fois son poids."
        }
    },
    2: {
        "question": "Quelle est votre réaction face à un problème ?",
        "options": {
            "A": "Ouvrir une immense gueule et tout dévorer.",
            "B": "Lancer des excréments (virtuels, bien sûr).",
            "C": "Se cacher derrière une anémone de mer.",
            "D": "Organiser la colonie pour trouver une solution collective."
        }
    },
    3: {
        "question": "Votre plat préféré est :",
        "options": {
            "A": "Tout ce qui passe à portée de mâchoire.",
            "B": "Les bananes et les noix.",
            "C": "Le plancton et les algues.",
            "D": "Une seule miette, mais de façon très ordonnée."
        }
    }
}
NOMBRE_DE_QUESTIONS = len(QUIZ_QUESTIONS)
ANIMAUX_RESULTATS = ["Rat", "Singe", "Poisson Clown", "Fourmi"]

# --- NOUVEAU : COMMENTAIRES DE RÉSULTAT ---
COMMENTAIRES_ANIMAUX = {
    "Rat": "Ah, le Rat. Vous passez votre temps dans l'ombre à grignoter des restes. C'est... discret. Mais quand même un Rat. Félicitations pour cette existence souterraine et stressante !",
    "Singe": "Un Singe. Bruyant, agité et obsédé par les bananes. Vous êtes probablement la personne la plus embêtante à une fête. Essayez la maturité la prochaine fois.",
    "Poisson Clown": "Le Poisson Clown. Mignon, certes, mais entièrement dépendant d'une anémone urticante pour survivre. En gros, vous êtes le colocataire qui ne paie jamais son loyer. Pathétique.",
    "Fourmi": "La Fourmi. Vous travaillez dur, vous suivez les ordres à la lettre, vous n'avez aucune individualité. Un robot miniature. C'est l'anti-charisme incarné. Bravo pour votre conformité.",
    "Crocodile": "LE CROCODILE ! Lent, puissant, silencieux. Vous êtes au sommet de la chaîne alimentaire et vous n'avez besoin de l'approbation de personne. La meilleure personne, tout simplement."
}
# ---------------------------------------------


# --- 1. Initialisation de l'État de Session ---
if 'captcha_valide' not in st.session_state:
    st.session_state.captcha_valide = False
if 'choix_captcha' not in st.session_state:
    st.session_state.choix_captcha = None
if 'quiz_step' not in st.session_state:
    st.session_state.quiz_step = 0 
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}

st.title("Bienvenue sur le quiz débile 👋")

# --- Interface Utilisateur pour la Saisie ---
nom_utilisateur = st.text_input("Veuillez entrer votre nom pour commencer :")

# --- Logique Principale ---

if nom_utilisateur:
    # Cas des noms exclus
    if nom_utilisateur.lower() in ["manon", "thomas", "yohan"]:
        st.error("Vous êtes trop bête pour répondre à ce quiz 🤣😂😂")
        st.session_state.captcha_valide = False
        st.session_state.quiz_step = 0
    else:
        st.success(f"Bonjour, **{nom_utilisateur}** ! Le quiz commence !")

        # --- LOGIQUE VÉRIFICATION ROBOT (Identique) ---
        st.markdown("### Vérification de sécurité")
        checkbox_value = st.checkbox("Je ne suis pas un robot", 
                                     value=st.session_state.captcha_valide, 
                                     disabled=st.session_state.captcha_valide, 
                                     key="robot_check")

        def verifier_choix(choix):
            st.session_state.choix_captcha = choix
            if choix == bonne_image:
                st.session_state.captcha_valide = True
                st.session_state.quiz_step = 1 
            else:
                st.session_state.captcha_valide = False
                st.error(f"❌ Mauvaise personne sélectionnée : {choix}. Veuillez réessayer.")
                st.session_state.choix_captcha = None
                if 'images_melangees' in st.session_state:
                    del st.session_state.images_melangees
                st.rerun()

        if checkbox_value and not st.session_state.captcha_valide:
            st.warning(f"Veuillez sélectionner la **{"meilleure personne"}** pour continuer.")
            images_liste = list(images_choix.keys())
            if 'images_melangees' not in st.session_state:
                random.shuffle(images_liste)
                st.session_state.images_melangees = images_liste
            
            images_a_afficher = st.session_state.images_melangees
            cols = st.columns(len(images_a_afficher))

            for i, image_nom in enumerate(images_a_afficher):
                with cols[i]:
                    image_path = images_choix[image_nom]
                    if os.path.exists(image_path):
                        st.image(image_path, caption=image_nom, width=120) 
                    else:
                        st.error(f"Fichier non trouvé : {image_path}")
                        st.stop()
                        
                    if st.button("Choisir", key=f"btn_{i}", on_click=verifier_choix, args=(image_nom,)):
                        pass
        
        # --- LOGIQUE DU QUIZ DE PERSONNALITÉ (Progression) ---

        if st.session_state.captcha_valide:
            if st.session_state.quiz_step == 1:
                 st.success("🤖 Vérification réussie ! Passons au vrai quiz maintenant !")
                 
            # 1. Traitement des questions
            if st.session_state.quiz_step <= NOMBRE_DE_QUESTIONS:
                current_step = st.session_state.quiz_step
                q_data = QUIZ_QUESTIONS[current_step]

                st.header(f"Question {current_step} / {NOMBRE_DE_QUESTIONS} :")
                
                reponse_q = st.radio(
                    q_data["question"],
                    q_data["options"].values(),
                    key=f"q_{current_step}_radio"
                )

                def next_question():
                    st.session_state.quiz_answers[current_step] = reponse_q
                    st.session_state.quiz_step += 1
                
                if st.button("Suivant", key=f"btn_next_q_{current_step}", on_click=next_question):
                    pass 

            # 2. Affichage des Résultats
            elif st.session_state.quiz_step == NOMBRE_DE_QUESTIONS + 1:
                st.header("🎉 Vos Résultats de Personnalité Débile")
                st.balloons()

                # DÉTERMINATION DU RÉSULTAT
                if nom_utilisateur.lower() == "etienne":
                    resultat_animal = "Crocodile"
                else:
                    resultat_animal = random.choice(ANIMAUX_RESULTATS)

                # AFFICHAGE DU RÉSULTAT ET DU COMMENTAIRE DÉNIGRANT
                commentaire = COMMENTAIRES_ANIMAUX.get(resultat_animal, "Commentaire non trouvé.")
                
                st.warning(f"Votre animal de personnalité est un **{resultat_animal}** !")
                st.markdown(f"> **{commentaire}**")
                
                st.markdown("---")
                
                st.subheader("Vos réponses (pour information) :")
                for q_num, ans in st.session_state.quiz_answers.items():
                    st.write(f"**Q{q_num}:** {ans}")
                
                # Bouton de réinitialisation
                def reset_quiz():
                    st.session_state.quiz_step = 0
                    st.session_state.captcha_valide = False
                    st.session_state.quiz_answers = {}
                    if 'images_melangees' in st.session_state:
                         del st.session_state.images_melangees
                
                if st.button("Recommencer le Quiz", on_click=reset_quiz):
                    st.rerun()

            # Message d'attente/bouton de démarrage
            elif st.session_state.quiz_step == 0:
                 st.success("🤖 Vérification réussie ! Cliquez sur le bouton 'Commencer le Quiz' ci-dessous.")
                 if st.button("Commencer le Quiz", key="start_quiz"):
                     st.session_state.quiz_step = 1
                     st.rerun()


else:
    st.info("Veuillez entrer votre nom ci-dessus pour continuer.")