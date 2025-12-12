import streamlit as st
import random
import pandas as pd 

# --- 1. CONFIGURATION DU JEU ---

# Définition des valeurs des cartes
VALEURS = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, 'Valet': 10, 'Dame': 10, 'Roi': 10,
    'As': 11
}
CARTES = list(VALEURS.keys())

# --- MAPPING VISUEL DES CARTES (Emojis) ---
CARTE_EMOJIS = {
    'As': '🅰️', 'Roi': '👑', 'Dame': '👸', 'Valet': '🤵',
    '10': '🔟', '9': '9️⃣', '8': '8️⃣', '7': '7️⃣', '6': '6️⃣',
    '5': '5️⃣', '4': '4️⃣', '3': '3️⃣', '2': '2️⃣'
}

def get_main_visual(main):
    """Convertit une liste de cartes (strings) en une chaîne d'emojis."""
    return ' '.join([CARTE_EMOJIS.get(carte, carte) for carte in main])

# --- 2. FONCTIONS DE BASE DU JEU ---

def creer_paquet():
    """Crée et mélange un paquet de cartes."""
    paquet = CARTES.copy() * 4 * len(['Pique', 'Trèfle', 'Cœur', 'Carreau'])
    random.shuffle(paquet)
    return paquet

def calculer_score(main):
    """Calcule le meilleur score possible pour une main (gestion de l'As)."""
    score = 0
    nombre_as = main.count('As')
    
    for carte in main:
        score += VALEURS[carte]
    
    while score > 21 and nombre_as > 0:
        score -= 10
        nombre_as -= 1
        
    return score

def distribuer_cartes(paquet):
    """Distribue les cartes initiales."""
    if len(paquet) < 20: 
        st.session_state.paquet = creer_paquet()
        paquet = st.session_state.paquet
        
    main_joueur = [paquet.pop(), paquet.pop()]
    main_croupier = [paquet.pop(), paquet.pop()]
    return main_joueur, main_croupier

def action_tirer(main, paquet):
    """Ajoute une carte à la main du joueur."""
    main.append(paquet.pop())
    return main

def tour_croupier():
    """Joue la main du croupier (tire jusqu'à 17 ou plus)."""
    paquet = st.session_state.paquet
    main_croupier = st.session_state.main_croupier
    
    while calculer_score(main_croupier) < 17:
        main_croupier.append(paquet.pop())
        
    st.session_state.statut_jeu = 'resultat'

# --- 3. FONCTIONS DE GESTION DE L'ÉTAT (Streamlit) ---

def initialiser_etat_session():
    """Initialise les variables de la session Streamlit."""
    if 'jetons' not in st.session_state:
        st.session_state.jetons = 100 
    if 'statut_jeu' not in st.session_state:
        st.session_state.statut_jeu = 'pseudo' 
    if 'pseudo' not in st.session_state:
        st.session_state.pseudo = ""
    if 'mise' not in st.session_state:
        st.session_state.mise = 0
    if 'paquet' not in st.session_state:
        st.session_state.paquet = creer_paquet()
    if 'main_joueur' not in st.session_state:
         st.session_state.main_joueur = []
    if 'main_croupier' not in st.session_state:
         st.session_state.main_croupier = []
    if 'leaderboard' not in st.session_state:
         st.session_state.leaderboard = [] 

def enregistrer_pseudo(pseudo_saisi):
    """Enregistre le pseudo et passe à l'étape de mise."""
    if pseudo_saisi.strip():
        st.session_state.pseudo = pseudo_saisi.strip()
        st.session_state.statut_jeu = 'mise'
        st.rerun()
    else:
        st.error("Veuillez saisir un pseudo valide pour commencer.")

def lancer_partie(mise_valeur):
    """Lance la distribution et passe à l'étape du jeu."""
    
    if mise_valeur <= 0:
        st.error("Veuillez miser un montant supérieur à zéro.")
        return
    if mise_valeur > st.session_state.jetons:
        st.error(f"Vous n'avez que {st.session_state.jetons} jetons. Mise trop élevée.")
        return

    st.session_state.mise = mise_valeur
    st.session_state.jetons -= mise_valeur 
    
    main_joueur, main_croupier = distribuer_cartes(st.session_state.paquet)
    st.session_state.main_joueur = main_joueur
    st.session_state.main_croupier = main_croupier
    
    st.session_state.statut_jeu = 'jouer'

def reinitialiser_partie():
    """Réinitialise le statut pour une nouvelle mise."""
    st.session_state.statut_jeu = 'mise'
    st.session_state.main_joueur = []
    st.session_state.main_croupier = []
    st.session_state.mise = 0

def enregistrer_score_final():
    """Enregistre le score du joueur (jetons restants) dans le leaderboard."""
    nouveau_score = {
        'Pseudo': st.session_state.pseudo,
        'Jetons Finaux': st.session_state.jetons
    }
    st.session_state.leaderboard.append(nouveau_score)
    # Tri et passage à l'écran de fin de jeu
    st.session_state.statut_jeu = 'game_over'

def afficher_leaderboard():
    """Affiche le tableau des scores trié."""
    if st.session_state.leaderboard:
        df = pd.DataFrame(st.session_state.leaderboard)
        df_sorted = df.sort_values(by='Jetons Finaux', ascending=False).reset_index(drop=True)
        df_sorted.index = df_sorted.index + 1
        
        st.markdown("### 🏆 Tableau des Scores (Leaderboard)")
        st.dataframe(df_sorted, use_container_width=True)
    else:
        st.info("Aucun score enregistré pour l'instant.")

# --- 4. INTERFACE UTILISATEUR ET LOGIQUE DU JEU ---

st.set_page_config(layout="centered", page_title="Blackjack Py")
initialiser_etat_session()

st.title("♠️ Blackjack Streamlit")
st.subheader("Bienvenue au Casino Py!")

# --- ÉTAPE 1 : PSEUDO ---
if st.session_state.statut_jeu == 'pseudo':
    st.markdown("---")
    st.header("Entrez votre Pseudo")
    
    pseudo_input = st.text_input("Pseudo :", max_chars=15, key="pseudo_input")
    
    if st.button("Commencer le Jeu", type="primary"):
        enregistrer_pseudo(pseudo_input)
        
    afficher_leaderboard()

# --- ÉTAPE 2 : MISE ---
elif st.session_state.statut_jeu == 'mise':
    
    st.info(f"Joueur : **{st.session_state.pseudo}** | 💰 **Vos Jetons :** {st.session_state.jetons}")
    st.markdown("---")
    
    col_mise, col_stop = st.columns([3, 1])
    
    with col_mise:
        st.header("Placez votre Mise")
        
        if st.session_state.jetons <= 0:
            st.error(f"FIN DE JEU : Vous n'avez plus de jetons. 😢 Votre score final est enregistré.")
            enregistrer_score_final()
            st.rerun()
        else:
            mise_choisie = st.number_input(
                "Combien de jetons voulez-vous miser ?",
                min_value=10,
                max_value=st.session_state.jetons,
                value=min(max( 10 , int(0.1*st.session_state.jetons)),st.session_state.jetons),
                step=5
            )
            
            st.button(
                f"Distribuer les cartes (Mise: {mise_choisie})",
                on_click=lancer_partie,
                args=(mise_choisie,),
                type="primary"
            )
            
    with col_stop:
        st.markdown("<br><br>", unsafe_allow_html=True) # Espace pour aligner le bouton
        if st.button("🔴 Arrêter et Sauvegarder", key="stop_game_mise"):
            enregistrer_score_final()
            st.rerun()
        
    # Affichage du classement sous la mise
    st.markdown("---")
    afficher_leaderboard()


# --- ÉTAPE 3 : JEU (Tirer/Rester) ---
elif st.session_state.statut_jeu == 'jouer':
    
    score_joueur = calculer_score(st.session_state.main_joueur)
    
    if score_joueur > 21:
        st.session_state.statut_jeu = 'resultat'
        st.rerun() 
        
    st.success(f"Partie en cours. Mise actuelle : {st.session_state.mise} jetons.")
    st.markdown("---")
    
    # Bouton Arrêter et Sauvegarder dans la phase de jeu
    if st.button("🔴 Arrêter et Sauvegarder", key="stop_game_jouer"):
        enregistrer_score_final()
        st.rerun()

    # Affichage du Croupier
    st.header("Main du Croupier")
    carte_croupier_visible = get_main_visual([st.session_state.main_croupier[0]])
    st.markdown(f"**Cartes :** {carte_croupier_visible} 🎴 (?)") 
    
    # Affichage du Joueur
    st.header(f"Votre Main ({st.session_state.pseudo})")
    main_joueur_visuel = get_main_visual(st.session_state.main_joueur)
    st.markdown(f"**Cartes :** {main_joueur_visuel}")
    st.warning(f"**Votre Score :** {score_joueur}")

    # Vérification du Blackjack Naturel (qui envoie directement au résultat)
    if len(st.session_state.main_joueur) == 2 and score_joueur == 21:
        st.info("🎉 **BLACKJACK NATUREL !** (Paie 3:2)")
        st.session_state.statut_jeu = 'resultat'
        st.rerun()
        
    col_hit, col_stand = st.columns(2)
    
    with col_hit:
        if st.button("Tirer (Hit)", type="primary", disabled=(score_joueur >= 21)):
            action_tirer(st.session_state.main_joueur, st.session_state.paquet)
            st.rerun()

    with col_stand:
        if st.button("Rester (Stand)", type="secondary"):
            tour_croupier()
            st.rerun()

# --- ÉTAPE 4 : RÉSULTAT ---
elif st.session_state.statut_jeu == 'resultat':
    
    score_joueur = calculer_score(st.session_state.main_joueur)
    score_croupier = calculer_score(st.session_state.main_croupier)
    mise = st.session_state.mise
    
    st.header("Résultats de la Partie")
    
    # Affichage des mains finales (VISUEL)
    main_joueur_visuel = get_main_visual(st.session_state.main_joueur)
    main_croupier_visuel = get_main_visual(st.session_state.main_croupier)

    st.markdown(f"**Votre Main ({st.session_state.pseudo}):** {main_joueur_visuel} (Score: **{score_joueur}**)")
    st.markdown(f"**Main du Croupier:** {main_croupier_visuel} (Score: **{score_croupier}**)")
    st.markdown("---")

    resultat = ""
    gain_net = 0

    joueur_blackjack = (len(st.session_state.main_joueur) == 2 and score_joueur == 21)
    croupier_blackjack = (len(st.session_state.main_croupier) == 2 and score_croupier == 21)
    
    # Logique de gain
    if joueur_blackjack and not croupier_blackjack:
        gain_net = int(mise * 1.5)
        st.balloons()
        resultat = f"🎉 **BLACKJACK !** Vous gagnez **{gain_net}** jetons. (Paie 3:2)"
    elif score_joueur > 21:
        resultat = f"❌ **Bust !** Votre score est de {score_joueur}. Vous perdez la mise de **{mise}**."
        gain_net = -mise
    elif score_croupier > 21:
        resultat = f"✅ Le Croupier a Bust ({score_croupier}) ! Vous gagnez **{mise}** jetons."
        gain_net = mise
    elif score_joueur > score_croupier:
        resultat = f"🎉 **Victoire !** Votre score ({score_joueur}) bat le Croupier ({score_croupier}). Vous gagnez **{mise}** jetons."
        gain_net = mise
    elif score_joueur < score_croupier:
        if croupier_blackjack:
             resultat = f"😭 **Défaite.** Le Croupier a Blackjack. Vous perdez la mise de **{mise}**."
        else:
             resultat = f"😭 **Défaite.** Votre score ({score_joueur}) est inférieur au Croupier ({score_croupier}). Vous perdez la mise de **{mise}**."
        gain_net = -mise
    else: 
        resultat = f"🤝 **Égalité (Push).** Scores identiques ({score_joueur}). Votre mise de **{mise}** jetons vous est retournée."
        gain_net = 0

    # Application du gain
    if gain_net >= 0:
        st.session_state.jetons += (mise + gain_net)
    
    st.metric("Résultat Net", f"{'+' if gain_net >= 0 else ''}{gain_net} jetons", delta=gain_net)
    st.subheader(resultat)
    
    # Bouton pour rejouer
    if st.session_state.jetons > 0:
        col_rejouer, col_stop_res = st.columns([3, 1])
        with col_rejouer:
            st.button("Jouer une autre main", on_click=reinitialiser_partie, type="primary")
        with col_stop_res:
             if st.button("🔴 Arrêter et Sauvegarder", key="stop_game_res"):
                enregistrer_score_final()
                st.rerun()

    else:
        st.error("FIN DE JEU : Vous n'avez plus de jetons. 😢")
        enregistrer_score_final() 
        st.rerun() 


# --- ÉTAPE 5 : GAME OVER ET CLASSEMENT ---
elif st.session_state.statut_jeu == 'game_over':
    
    st.header(f"Game Over, {st.session_state.pseudo}!")
    st.error(f"Votre aventure s'arrête ici. Votre score final était de **{st.session_state.jetons}** jetons.")
    st.markdown("---")
    
    afficher_leaderboard()
    
    # Option pour recommencer à zéro (avec un nouveau pseudo ou le même)
    if st.button("Recommencer à zéro", type="primary"):
        del st.session_state.jetons
        st.session_state.statut_jeu = 'pseudo'
        st.session_state.pseudo = ""
        st.rerun()