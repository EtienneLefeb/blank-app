import streamlit as st
import random
import os

# --- CONFIGURATION DES CHEMINS D'IMAGE ---
# Assurez-vous que le dossier 'images' est au même niveau que ce fichier (ou ajustez le chemin)
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

# --- DÉFINITION DU QUIZ DE PERSONNALITÉ (10 QUESTIONS) ---
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
    },
    4: {
        "question": "Quel est votre talent caché ?",
        "options": {
            "A": "Dormir pendant des mois.",
            "B": "Voler les objets brillants des humains.",
            "C": "Me reproduire très rapidement.",
            "D": "Parler à l'eau."
        }
    },
    5: {
        "question": "Décrivez votre hygiène personnelle :",
        "options": {
            "A": "Un bain de boue, c'est suffisant.",
            "B": "Je me gratte souvent.",
            "C": "Je me fais nettoyer par des crevettes.",
            "D": "Je n'ai pas le temps, je travaille."
        }
    },
    6: {
        "question": "Votre couleur d'humeur typique ?",
        "options": {
            "A": "Vert boue.",
            "B": "Rouge colère.",
            "C": "Orange ou blanc, cela dépend de ma colère.",
            "D": "Noir (comme l'uniforme de travail)."
        }
    },
    7: {
        "question": "Si vous gagnez à la loterie, que faites-vous ?",
        "options": {
            "A": "J'achète le marécage le plus grand et je m'y prélasse.",
            "B": "J'achète un jet-pack et je fais le singe dans les airs.",
            "C": "J'achète une anémone de luxe pour ma retraite.",
            "D": "Je reverse tout à la reine pour l'efficacité de la colonie."
        }
    },
    8: {
        "question": "Votre plus grande peur secrète ?",
        "options": {
            "A": "Le dentiste (un bâton entre les mâchoires).",
            "B": "Les cages de zoo.",
            "C": "Être seul sans mon anémone.",
            "D": "Les bottes d'humains."
        }
    },
    9: {
        "question": "Votre devise dans la vie ?",
        "options": {
            "A": "Chasse ou sois chassé.",
            "B": "Toujours plus de vacarme.",
            "C": "Restons cachés, la vie est moins dangereuse.",
            "D": "Pour la Reine et la Colonie !"
        }
    },
    10: {
        "question": "Comment gérez-vous le stress ?",
        "options": {
            "A": "Je reste immobile pendant 3 heures.",
            "B": "Je crie très fort.",
            "C": "Je nage en rond jusqu'à l'épuisement.",
            "D": "Je travaille deux fois plus."
        }
    }
}
NOMBRE_DE_QUESTIONS = len(QUIZ_QUESTIONS)
ANIMAUX_RESULTATS = ["Rat", "Singe", "Poisson Clown", "Fourmi"]

# --- MAPPING DES IMAGES D'ANIMAUX ---
ANIMAL_IMAGE_PATHS = {
    "Crocodile": os.path.join(IMAGE_FOLDER, "crocodile.png"),
    "Rat": os.path.join(IMAGE_FOLDER, "rat.png"),
    "Singe": os.path.join(IMAGE_FOLDER, "singe.png"),
    "Poisson Clown": os.path.join(IMAGE_FOLDER, "poisson_clown.png"),
    "Fourmi": os.path.join(IMAGE_FOLDER, "fourmi.png"),
    "Loutre" :os.path.join(IMAGE_FOLDER, "loutre.png")
}

# --- COMMENTAIRES DE RÉSULTAT ---
COMMENTAIRES_ANIMAUX = {
    "Rat": "Ah, le Rat. Vous passez votre temps dans l'ombre à grignoter des restes. C'est... discret. Mais quand même un Rat. Félicitations pour cette existence souterraine et stressante !",
    "Singe": "Un Singe. Bruyant, agité et obsédé par les bananes. Vous êtes probablement la personne la plus embêtante à une fête. Essayez la maturité la prochaine fois.",
    "Poisson Clown": "Le Poisson Clown. Mignon, certes, mais entièrement dépendant d'une anémone urticante pour survivre. En gros, vous êtes le colocataire qui ne paie jamais son loyer. Pathétique.",
    "Fourmi": "La Fourmi. Vous travaillez dur, vous suivez les ordres à la lettre, vous n'avez aucune individualité. Un robot miniature. C'est l'anti-charisme incarné. Bravo pour votre conformité.",
    "Crocodile": "LE CROCODILE ! Lent, puissant, silencieux. Vous êtes au sommet de la chaîne alimentaire et vous n'avez besoin de l'approbation de personne. La meilleure personne, tout simplement.",
    "Loutre": "La loutre ! Elle est si mignonne, et elle tabasse la grosse victime de Castor pour le bien de la planète. Vous avez le courage et la force de repousser le mal et les barrages."
}
# ---------------------------------------------


# --- Configuration de la page et Initialisation de l'État de Session ---
st.set_page_config(
    page_title="Le Quiz Débile",
    layout="centered",
    initial_sidebar_state="expanded" 
)

if 'captcha_valide' not in st.session_state:
    st.session_state.captcha_valide = False
if 'choix_captcha' not in st.session_state:
    st.session_state.choix_captcha = None
if 'quiz_step' not in st.session_state:
    st.session_state.quiz_step = 0 
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}

st.title("Bienvenue sur le quiz débile 👋")
st.markdown("---")

# --- Fonctions du Quiz ---

def verifier_choix(choix):
    """Logique du CAPTCHA"""
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

def next_question(reponse_q, current_step):
    """Passe à la question suivante et enregistre la réponse."""
    st.session_state.quiz_answers[current_step] = reponse_q
    st.session_state.quiz_step += 1
    
def reset_quiz():
    """Réinitialise toutes les variables de session pour recommencer."""
    st.session_state.quiz_step = 0
    st.session_state.captcha_valide = False
    st.session_state.quiz_answers = {}
    if 'images_melangees' in st.session_state:
        del st.session_state.images_melangees


# --- Logique Principale d'Affichage ---

nom_utilisateur = st.text_input("Veuillez entrer votre nom pour commencer :")

if nom_utilisateur:
    # Cas des noms exclus
    if nom_utilisateur.lower() in ["manon", "thomas", "yohan"]:
        st.error("Vous êtes trop bête pour répondre à ce quiz 🤣😂😂")
        st.session_state.captcha_valide = False
        st.session_state.quiz_step = 0
    elif nom_utilisateur.lower() in ["michel","kaiser"]:
        st.error("Vous êtes trop bête pour répondre à ce quiz 🤣😂😂, mais joyeux anniversaire quand même 🥳🥳🥳")
        st.session_state.captcha_valide = False
        st.session_state.quiz_step = 0
    else:
        st.success(f"Bonjour, **{nom_utilisateur}** ! Le quiz commence !")

        # --- LOGIQUE VÉRIFICATION ROBOT (CAPTCHA) ---
        st.markdown("### Vérification de sécurité")
        
        checkbox_value = st.checkbox("Je ne suis pas un robot", 
                                     value=st.session_state.captcha_valide, 
                                     disabled=st.session_state.captcha_valide, 
                                     key="robot_check")

        if checkbox_value and not st.session_state.captcha_valide:
            st.warning(f"Veuillez sélectionner la **meilleure personne** pour continuer.")
            
            # Mélanger les images pour le CAPTCHA
            images_liste = list(images_choix.keys())
            if 'images_melangees' not in st.session_state:
                random.shuffle(images_liste)
                st.session_state.images_melangees = images_liste
            
            images_a_afficher = st.session_state.images_melangees
            cols = st.columns(len(images_a_afficher))

            # Affichage du CAPTCHA (Images + Boutons)
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
            
            # 1. Traitement des questions
            if st.session_state.quiz_step > 0 and st.session_state.quiz_step <= NOMBRE_DE_QUESTIONS:
                
                if st.session_state.quiz_step == 1:
                     st.success("🤖 Vérification réussie ! Passons au vrai quiz maintenant !")
                     
                current_step = st.session_state.quiz_step
                q_data = QUIZ_QUESTIONS[current_step]

                st.header(f"Question {current_step} / {NOMBRE_DE_QUESTIONS} :")
                
                default_answer = st.session_state.quiz_answers.get(current_step)
                if default_answer is None:
                    default_answer = list(q_data["options"].values())[0]

                try:
                    default_index = list(q_data["options"].values()).index(default_answer)
                except ValueError:
                    default_index = 0

                reponse_q = st.radio(
                    q_data["question"],
                    q_data["options"].values(),
                    index=default_index, 
                    key=f"q_{current_step}_radio"
                )

                if st.button("Suivant", key=f"btn_next_q_{current_step}", on_click=next_question, args=(reponse_q, current_step)):
                    st.rerun()
        
            # 2. Affichage des Résultats
            elif st.session_state.quiz_step == NOMBRE_DE_QUESTIONS + 1:
                st.header("🎉 Vos Résultats de Personnalité Débile")
                st.balloons()

                # DÉTERMINATION DU RÉSULTAT
                if nom_utilisateur.lower() == "etienne":
                    resultat_animal = "Crocodile"
                elif nom_utilisateur.lower() == "tony":
                    resultat_animal = "Loutre"
                else:
                    resultat_animal = random.choice(ANIMAUX_RESULTATS)

                # DÉTERMINATION DU CHEMIN DE L'IMAGE ET DU COMMENTAIRE
                image_resultat_path = ANIMAL_IMAGE_PATHS.get(resultat_animal)
                commentaire = COMMENTAIRES_ANIMAUX.get(resultat_animal, "Commentaire non trouvé.")
                
                # AFFICHAGE DE L'IMAGE
                if image_resultat_path and os.path.exists(image_resultat_path):
                    st.image(image_resultat_path, caption=f"Vous êtes un(e) **{resultat_animal}**", width=300) 
                else:
                    st.error(f"⚠️ Image de l'animal non trouvée. Vérifiez '{os.path.basename(image_resultat_path)}' dans '{IMAGE_FOLDER}/'.")

                # AFFICHAGE DU RÉSULTAT ET DU COMMENTAIRE DÉNIGRANT
                st.warning(f"Votre animal de personnalité est un **{resultat_animal}** !")
                st.markdown(f"> **{commentaire}**")
                
                st.markdown("---")
                
                st.subheader("Vos réponses (pour information) :")
                for q_num, ans in st.session_state.quiz_answers.items():
                    st.write(f"**Q{q_num}:** {ans}")
                
                # Bouton de réinitialisation
                if st.button("Recommencer le Quiz", on_click=reset_quiz):
                    st.rerun() 
            
            # 3. Message d'attente/bouton de démarrage après le CAPTCHA (étape 0)
            elif st.session_state.quiz_step == 0:
                 st.success("🤖 Vérification réussie ! Cliquez sur le bouton 'Commencer le Quiz' ci-dessous.")
                 if st.button("Commencer le Quiz", key="start_quiz"):
                    st.session_state.quiz_step = 1
                    st.rerun()
                    
        else:
            if st.session_state.quiz_step != 0:
                reset_quiz()


else:
    st.info("Veuillez entrer votre nom ci-dessus pour continuer.")