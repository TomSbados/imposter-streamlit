"""
Imposter Game — Streamlit Edition
"""

import streamlit as st
import random

# ── Categories + vague imposter hints ─────────────────────────────────────────
# Each entry: ("Category Name", "Vague hint for imposter")

CATEGORIES = [
    # General
    ("Jeffrey Epstein's Contacts", "powerful people"),
    ("Car Brands", "vehicles"),
    ("Fast Food Chains", "food"),
    ("US Presidents", "leaders"),
    ("Marvel Superheroes", "fiction"),
    ("Olympic Sports", "competition"),
    ("Social Media Apps", "internet"),
    ("Types of Cheese", "dairy"),
    ("Dog Breeds", "animals"),
    ("Countries in Africa", "places"),
    ("Tech Billionaires", "rich people"),
    ("Conspiracy Theories", "secrets"),
    ("Things in a Hospital", "medical"),
    ("Words That Sound Rude But Aren't", "language"),
    ("Reality TV Shows", "entertainment"),
    ("Things Found at a Crime Scene", "evidence"),
    ("Poker Terms", "gambling"),
    ("Types of Therapy", "mental health"),
    ("Things Elon Musk Has Named", "branding"),
    ("Rejected McDonald's Menu Items", "food"),
    ("Currencies Around the World", "money"),
    ("Military Ranks", "hierarchy"),
    ("Types of Knives", "tools"),
    ("Illegal Drugs", "substances"),
    ("Types of Plastic Surgery", "body"),
    ("Cults", "groups"),
    ("Dictators", "power"),
    ("Things You'd Find in Vegas", "nightlife"),
    ("Phobias", "fear"),
    ("Slang Terms From the 2000s", "language"),
    ("Mafia Terminology", "crime"),
    ("Bond Villains", "fiction"),
    ("Serial Killers", "crime"),
    ("Cocktails", "drinks"),
    ("Skateboard Tricks", "sports"),
    ("Wrestling Moves", "combat"),
    ("Gym Equipment", "fitness"),
    ("Crypto Coins", "money"),
    ("Sneaker Brands", "fashion"),
    ("Things at a Funeral", "death"),
    ("Prison Slang", "crime"),
    ("Reasons to Call 911", "emergency"),
    ("Kanye West Albums", "music"),
    ("OnlyFans Niches", "content"),
    ("Scam Types", "deception"),
    ("Taxi Apps", "transport"),
    ("Things in a Trap House", "chaos"),
    ("Eminem Songs", "music"),
    ("Tattoo Styles", "art"),
    ("Street Gang Names", "groups"),

    # Vegas
    ("Things You See on the Strip", "nightlife"),
    ("Casino Games", "gambling"),
    ("Famous Vegas Hotels", "places"),
    ("Vegas Buffet Foods", "food"),
    ("Things Said by a Blackjack Dealer", "gambling"),
    ("Slot Machine Symbols", "gambling"),
    ("Vegas Show Acts", "entertainment"),
    ("Things in a Casino That Have No Clocks", "objects"),
    ("Reasons the Pit Boss is Watching You", "suspicion"),
    ("Free Drink Excuses", "social"),
    ("Things That Happen at 4am on Fremont Street", "chaos"),
    ("Reasons Someone is Running Through a Casino", "urgency"),
    ("What's in a Stranger's Cup at the Craps Table", "drinks"),
    ("Things You Find in a Vegas Hotel Room That Weren't Yours", "mystery"),
    ("Excuses for Being Down $3,000", "money"),
    ("Things the Uber Driver Has Seen This Week", "stories"),
    ("What Happened in Vegas That Definitely Won't Stay There", "secrets"),
    ("Reasons the Bachelor Party Got Kicked Out", "trouble"),
    ("Things a Vegas Magician Says", "performance"),
    ("Jobs That Only Exist in Vegas", "work"),
    ("Poker Hands", "gambling"),
    ("Reasons You're Down Bad at the Tables", "losing"),
    ("Things High Rollers Say", "wealth"),
    ("Ways to Lose Money Faster", "money"),
    ("Things Overheard at the Sportsbook", "gambling"),
    ("VIP Bottle Service Excuses", "nightlife"),
    ("Casino Chip Colors", "gambling"),
    ("Card Counting Techniques", "strategy"),
    ("Things a Casino Cheater Would Say", "deception"),
    ("Reasons You're Banned from the Bellagio", "trouble"),
    ("Drive-Thru Wedding Chapel Names", "romance"),
    ("Celebrity Residency Acts", "entertainment"),
    ("Things on a Vegas Pawn Shop Shelf", "objects"),
    ("Reasons Someone is Crying Outside a Casino", "emotions"),
    ("What the Guy in Head-to-Toe Affliction is Doing", "chaos"),
    ("Names of Fake Elvis Impersonators", "performance"),
    ("Things Sold on the Strip for $20", "commerce"),
    ("Vegas Wedding Regrets", "romance"),
    ("Things People Lie About When They Get Home", "secrets"),
    ("Reasons to Visit the 24hr Wedding Chapel at 3am", "impulse"),
    ("What's in the Mystery Cocktail", "drinks"),
    ("Cirque du Soleil Act Names", "performance"),
    ("Things the Vegas Taxi Driver Says", "stories"),
    ("Crimes Committed on the Strip", "crime"),
    ("Reasons the Pool Party Got Shut Down", "trouble"),
    ("Things a Vegas Instagram Influencer Posts", "social media"),
    ("What's Inside the Mystery Bag at the Pawn Shop", "mystery"),
    ("Nicknames for Regular Gamblers", "people"),
    ("Things You Regret Buying at 2am", "impulse"),
    ("Occupations of People at the Roulette Table", "people"),
]

# ── Random starter traits (avoids revealing who the imposter is) ──────────────

STARTER_TRAITS = [
    "the player who woke up earliest today",
    "the player wearing the most colors",
    "the player whose birthday is coming up soonest",
    "the player who traveled the furthest to get here",
    "the player with the longest hair",
    "the player who last ate something",
    "the player sitting closest to the door",
    "the player who most recently used their phone",
    "the player with the most steps today",
    "the player who laughed most recently",
    "the player wearing the most accessories",
    "the player who stayed up latest last night",
    "the player who has been to Vegas the most times",
    "the player who spent the most money today",
    "the player with the loudest laugh",
]

# ── Session State Init ─────────────────────────────────────────────────────────

def init_state():
    defaults = {
        "phase": "setup",
        "num_players": 4,
        "num_imposters": 1,
        "roles": {},
        "category": None,
        "hint": None,
        "current_view_index": 0,
        "seen": set(),
        "starter_trait": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def reset_game():
    for k in ["phase", "num_players", "num_imposters", "roles", "category", "hint",
              "current_view_index", "seen", "starter_trait"]:
        if k in st.session_state:
            del st.session_state[k]
    init_state()

def start_game(num_players, num_imposters):
    indices = list(range(num_players))
    imposters = set(random.sample(indices, num_imposters))
    roles = {i: ("imposter" if i in imposters else "civilian") for i in indices}

    category_name, hint = random.choice(CATEGORIES)
    starter_trait = random.choice(STARTER_TRAITS)

    st.session_state.phase = "reveal"
    st.session_state.roles = roles
    st.session_state.category = category_name
    st.session_state.hint = hint
    st.session_state.current_view_index = 0
    st.session_state.seen = set()
    st.session_state.starter_trait = starter_trait

# ── Styling ───────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Imposter Game", page_icon="🕵️", layout="centered")

st.markdown("""
<style>
    .role-box {
        font-size: 2.4rem;
        font-weight: 900;
        text-align: center;
        padding: 2.5rem 1rem;
        border-radius: 1.2rem;
        margin: 1rem 0;
        letter-spacing: 1px;
    }
    .civilian-box {
        background: #1a2e1a;
        color: #4ade80;
        border: 2px solid #166534;
    }
    .imposter-box {
        background: #2e1a1a;
        color: #f87171;
        border: 2px solid #991b1b;
    }
    .category-box {
        background: #1e1b2e;
        color: #a78bfa;
        font-size: 1.1rem;
        font-weight: 700;
        text-align: center;
        padding: 0.8rem 1.5rem;
        border-radius: 999px;
        display: inline-block;
        margin: 0.5rem auto;
    }
    .hint-box {
        background: #2e2a1a;
        color: #fbbf24;
        font-size: 1.1rem;
        font-weight: 700;
        text-align: center;
        padding: 0.8rem 1.5rem;
        border-radius: 999px;
        display: inline-block;
        margin: 0.5rem auto;
        border: 1px solid #92400e;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PHASE: SETUP
# ══════════════════════════════════════════════════════════════════════════════

if st.session_state.phase == "setup":
    st.title("🕵️ Imposter Game")
    st.markdown("Everyone gets a **category** to discuss — but imposters only get a vague hint. Find them before they fool you!")
    st.divider()

    num_players = st.slider("Number of players", min_value=3, max_value=12, value=st.session_state.num_players)
    st.session_state.num_players = num_players

    max_imposters = max(1, (num_players - 1) // 2)
    clamped_imposters = min(max(1, st.session_state.num_imposters), max_imposters)
    if max_imposters == 1:
        st.session_state.num_imposters = 1
        num_imposters = 1
        st.markdown("**Number of imposters:** 1")
    else:
        num_imposters = st.slider("Number of imposters", min_value=1, max_value=max_imposters, value=clamped_imposters)
        st.session_state.num_imposters = num_imposters

    st.divider()
    st.markdown(f"**{num_players} players** · **{num_imposters} imposter{'s' if num_imposters > 1 else ''}** · **{num_players - num_imposters} civilian{'s' if num_players - num_imposters > 1 else ''}**")

    if st.button("🚀 Start Game", type="primary", use_container_width=True):
        start_game(num_players, num_imposters)
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PHASE: REVEAL
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.phase == "reveal":
    idx = st.session_state.current_view_index
    total = st.session_state.num_players

    if idx >= total:
        st.session_state.phase = "play"
        st.rerun()

    player_num = idx + 1
    already_seen = idx in st.session_state.seen

    st.title("🔐 Role Reveal")
    st.markdown(f"### Pass the device to **Player {player_num}** 👇")
    st.caption("Everyone else — look away!")
    st.divider()

    if not already_seen:
        if st.button(f"👁 Show my role, Player {player_num}", type="primary", use_container_width=True):
            st.session_state.seen.add(idx)
            st.rerun()
    else:
        role = st.session_state.roles[idx]
        category = st.session_state.category
        hint = st.session_state.hint

        if role == "civilian":
            st.markdown('<div class="role-box civilian-box">✅ CIVILIAN</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center"><span class="category-box">Category: {category}</span></div>', unsafe_allow_html=True)
            st.caption("You know the category. Discuss it without giving it away to the imposters!")
        else:
            st.markdown('<div class="role-box imposter-box">🔴 IMPOSTER</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center"><span class="hint-box">Hint: {hint}</span></div>', unsafe_allow_html=True)
            st.caption("You don't know the exact category — just the hint. Bluff your way through!")

        st.divider()
        if st.button("✅ Done — pass to next player", use_container_width=True):
            st.session_state.current_view_index += 1
            st.rerun()

    st.progress(idx / total, text=f"Player {player_num} of {total}")

# ══════════════════════════════════════════════════════════════════════════════
# PHASE: PLAY
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.phase == "play":
    st.title("💬 Discussion Time")
    st.markdown("Everyone takes turns saying **one word or phrase** related to the category.")
    st.markdown("Imposters — use your hint to bluff! Civilians — be specific enough to prove yourself without being too obvious.")
    st.divider()

    trait = st.session_state.starter_trait
    st.success(f"### 🎯 First up: {trait}")
    st.caption("This was randomly chosen — it has nothing to do with who the imposter is.")

    st.divider()

    num_imposters = st.session_state.num_imposters
    st.info(f"There {'is' if num_imposters == 1 else 'are'} **{num_imposters} imposter{'s' if num_imposters > 1 else ''}** among you.")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎭 Reveal Roles", type="primary", use_container_width=True):
            st.session_state.phase = "result"
            st.rerun()
    with col2:
        if st.button("🔄 New Game", use_container_width=True):
            reset_game()
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PHASE: RESULT
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.phase == "result":
    st.title("🎭 The Reveal")
    st.markdown("**The category was:**")
    st.markdown(f'<div style="text-align:center"><span class="category-box" style="font-size:1.4rem;padding:1rem 2rem">{st.session_state.category}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center"><span class="hint-box">Imposter hint was: {st.session_state.hint}</span></div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("🧾 Player Roles")

    roles = st.session_state.roles
    for i in range(st.session_state.num_players):
        role = roles[i]
        if role == "imposter":
            st.markdown(f"**Player {i+1}** — 🔴 IMPOSTER")
        else:
            st.markdown(f"**Player {i+1}** — ✅ Civilian")

    st.divider()
    if st.button("🔄 Play Again", type="primary", use_container_width=True):
        reset_game()
        st.rerun()
