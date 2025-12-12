import streamlit as st
import random

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
    # Note : Si vous voulez des cartes réelles, il faudrait utiliser st.image ici
    return ' '.join([CARTE_EMOJIS.get(carte, carte) for carte in main])

# --- 2. FONCTIONS DE BASE DU JEU ---

def creer_paquet():
    """Crée et mélange un paquet de 52 cartes (multiplié par 4 pour le réalisme)."""
    # Utiliser un paquet de 4 jeux de 52 cartes
    paquet = CARTES.copy() * 4 * len(['Pique', 'Trèfle', 'Cœur', 'Carreau'])
    random.shuffle(paquet)
    return paquet

def calculer_score(main):
    """Calcule le meilleur score possible pour une main."""
    score = 0
    nombre_as = main.count('As')
    
    # Calcul initial (As = 11)
    for carte in main:
        score += VALEURS[carte]
    
    # Ajustement des As (de 11 à 1 si > 21)
    while score > 21 and nombre_as > 0:
        score -= 10  # On change un As de 11 à 1
        nombre_as -= 1
        
    return score

def distribuer_cartes(paquet):
    """Distribue les cartes initiales."""
    # S'assurer qu'il y a assez de cartes, sinon on recrée le paquet
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
    
    # Le croupier doit tirer jusqu'à un score de 17 ou plus
    while calculer_score(main_croupier) < 17:
        main_croupier.append(paquet.pop())
        
    st.session_state.statut_jeu = 'resultat'

# --- 3. FONCTIONS DE GESTION DE L'ÉTAT (Streamlit) ---

def initialiser_etat_session():
    """Initialise les variables de la session Streamlit."""
    if 'jetons' not in st.session_state:
        st.session_state.jetons = 100 # Le joueur commence avec 100 jetons
    if 'statut_jeu' not in st.session_state:
        # 'mise', 'jouer', 'resultat'
        st.session_state.statut_jeu = 'mise' 
    if 'mise' not in st.session_state:
        st.session_state.mise = 0
    if 'paquet' not in st.session_state:
        st.session_state.paquet = creer_paquet()
    if 'main_joueur' not in st.session_state:
         st.session_state.main_joueur = []
    if 'main_croupier' not in st.session_state:
         st.session_state.main_croupier = []

def lancer_partie(mise_valeur):
    """Lance la distribution et passe à l'étape du jeu."""
    
    # 1. Vérification de la mise
    if mise_valeur <= 0:
        st.error("Veuillez miser un montant supérieur à zéro.")
        return
    if mise_valeur > st.session_state.jetons:
        st.error(f"Vous n'avez que {st.session_state.jetons} jetons. Mise trop élevée.")
        return

    # 2. Enregistrement de la mise et déduction des jetons
    st.session_state.mise = mise_valeur
    st.session_state.jetons -= mise_valeur 
    
    # 3. Distribution des cartes
    main_joueur, main_croupier = distribuer_cartes(st.session_state.paquet)
    st.session_state.main_joueur = main_joueur
    st.session_state.main_croupier = main_croupier
    
    # 4. Passage à l'étape du jeu
    st.session_state.statut_jeu = 'jouer'

def reinitialiser_partie():
    """Réinitialise le statut pour une nouvelle mise."""
    st.session_state.statut_jeu = 'mise'
    st.session_state.main_joueur = []
    st.session_state.main_croupier = []
    st.session_state.mise = 0
    # Ne pas recréer le paquet entier sauf s'il est presque vide.


# --- 4. INTERFACE UTILISATEUR ET LOGIQUE DU JEU ---

st.set_page_config(layout="centered", page_title="Blackjack Py")
initialiser_etat_session()

st.title("♠️ Blackjack Streamlit")
st.subheader("Bienvenue au Casino Py!")

# Affichage des jetons
st.info(f"💰 **Vos Jetons :** {st.session_state.jetons}")

if st.session_state.statut_jeu == 'mise':
    
    st.markdown("---")
    st.header("Placez votre Mise")
    
    if st.session_state.jetons <= 0:
        st.error("Vous n'avez plus de jetons. Veuillez recharger pour jouer à nouveau.")
    else:
        # Saisie de la mise
        mise_choisie = st.number_input(
            "Combien de jetons voulez-vous miser ?",
            min_value=10,
            max_value=st.session_state.jetons,
            # Valeur par défaut : max(10, 10% du solde), limitée au solde total.
            value=min(max( 10 , int(0.1*st.session_state.jetons)),st.session_state.jetons),
            step=5
        )
        
        # Bouton de lancement de la partie
        st.button(
            f"Distribuer les cartes (Mise: {mise_choisie})",
            on_click=lancer_partie,
            args=(mise_choisie,),
            type="primary"
        )

elif st.session_state.statut_jeu == 'jouer':
    
    score_joueur = calculer_score(st.session_state.main_joueur)
    
    # Si le joueur a BUST après avoir tiré, on passe directement au résultat
    if score_joueur > 21:
        st.session_state.statut_jeu = 'resultat'
        st.rerun() # Rafraîchir pour afficher le résultat
        
    st.success(f"Partie en cours. Mise actuelle : {st.session_state.mise} jetons.")
    st.markdown("---")
    
    # Affichage du Croupier (VISUEL)
    st.header("Main du Croupier")
    carte_croupier_visible = get_main_visual([st.session_state.main_croupier[0]])
    st.markdown(f"**Cartes :** {carte_croupier_visible} 🎴 (?)") 
    
    # Affichage du Joueur (VISUEL)
    st.header("Votre Main")
    main_joueur_visuel = get_main_visual(st.session_state.main_joueur)
    st.markdown(f"**Cartes :** {main_joueur_visuel}")
    st.warning(f"**Votre Score :** {score_joueur}")

    # --- BOUTONS D'ACTION DU JOUEUR ---
    
    # Vérification du Blackjack Naturel (21 avec 2 cartes)
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

elif st.session_state.statut_jeu == 'resultat':
    
    score_joueur = calculer_score(st.session_state.main_joueur)
    score_croupier = calculer_score(st.session_state.main_croupier)
    mise = st.session_state.mise
    
    st.header("Résultats de la Partie")
    
    # Affichage des mains finales (VISUEL)
    main_joueur_visuel = get_main_visual(st.session_state.main_joueur)
    main_croupier_visuel = get_main_visual(st.session_state.main_croupier)

    st.markdown(f"**Votre Main :** {main_joueur_visuel} (Score: **{score_joueur}**)")
    st.markdown(f"**Main du Croupier :** {main_croupier_visuel} (Score: **{score_croupier}**)")
    st.markdown("---")

    resultat = ""
    gain_net = 0  # Gain net par rapport à la mise initiale

    # --- LOGIQUE DE GAIN ---
    joueur_blackjack = (len(st.session_state.main_joueur) == 2 and score_joueur == 21)
    croupier_blackjack = (len(st.session_state.main_croupier) == 2 and score_croupier == 21)
    
    # 1. Blackjack (se paie 3:2, sauf en cas d'égalité avec le croupier)
    if joueur_blackjack and not croupier_blackjack:
        gain_net = int(mise * 1.5)
        st.balloons()
        resultat = f"🎉 **BLACKJACK !** Vous gagnez **{gain_net}** jetons. (Paie 3:2)"
    
    # 2. Défaite (Bust ou score inférieur)
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
        # Si le joueur n'a pas blackjack mais le croupier oui, le joueur perd.
        if croupier_blackjack:
             resultat = f"😭 **Défaite.** Le Croupier a Blackjack. Vous perdez la mise de **{mise}**."
        else:
             resultat = f"😭 **Défaite.** Votre score ({score_joueur}) est inférieur au Croupier ({score_croupier}). Vous perdez la mise de **{mise}**."
        gain_net = -mise
        
    else: # Égalité
        # Si les deux ont Blackjack, c'est Push
        resultat = f"🤝 **Égalité (Push).** Scores identiques ({score_joueur}). Votre mise de **{mise}** jetons vous est retournée."
        gain_net = 0

    # 3. Application du gain aux jetons
    # Si gain_net >= 0 : on ajoute le gain + la mise initiale (car la mise avait été retirée au départ).
    if gain_net >= 0:
        st.session_state.jetons += (mise + gain_net)
    
    st.metric("Résultat Net", f"{'+' if gain_net >= 0 else ''}{gain_net} jetons", delta=gain_net)
    st.subheader(resultat)
    
    # Bouton pour rejouer
    if st.session_state.jetons > 0:
        st.button("Jouer une autre main", on_click=reinitialiser_partie, type="primary")
    else:
        st.error("FIN DE JEU : Vous n'avez plus de jetons. 😢")