"""
Imposter Game — Streamlit Edition
"""

import streamlit as st
import random

# ── Categories (just the names) ───────────────────────────────────────────────

CATEGORIES = [
    "Jeffrey Epstein's Contacts",
    "Car Brands",
    "Fast Food Chains",
    "US Presidents",
    "Marvel Superheroes",
    "Olympic Sports",
    "Social Media Apps",
    "Types of Cheese",
    "Dog Breeds",
    "Countries in Africa",
    "Tech Billionaires",
    "Conspiracy Theories",
    "Things in a Hospital",
    "Words That Sound Rude But Aren't",
    "Reality TV Shows",
    "Things Found at a Crime Scene",
    "Poker Terms",
    "Types of Therapy",
    "Things Elon Musk Has Named",
    "Rejected McDonald's Menu Items",
    "Currencies Around the World",
    "Military Ranks",
    "Types of Knives",
    "Illegal Drugs",
    "Types of Plastic Surgery",
    "Cults",
    "Dictators",
    "Things You'd Find in Vegas",
    "Phobias",
    "Slang Terms From the 2000s",
    "Mafia Terminology",
    "Bond Villains",
    "Serial Killers",
    "Cocktails",
    "Skateboard Tricks",
    "Wrestling Moves",
    "Gym Equipment",
    "Crypto Coins",
    "Sneaker Brands",
    "Things at a Funeral",
    "Prison Slang",
    "Reasons to Call 911",
    "Kanye West Albums",
    "OnlyFans Niches",
    "Scam Types",
    "Taxi Apps",
    "Things in a Trap House",
    "Eminem Songs",
    "Tattoo Styles",
    "Street Gang Names",
]

CATEGORIES = [
    # Classic Vegas
    "Things You See on the Strip",
    "Casino Games",
    "Famous Vegas Hotels",
    "Vegas Buffet Foods",
    "Things Said by a Blackjack Dealer",
    "Slot Machine Symbols",
    "Vegas Show Acts",
    "Things in a Casino That Have No Clocks",
    "Reasons the Pit Boss is Watching You",
    "Free Drink Excuses",

    # Chaotic Vegas Energy
    "Things That Happen at 4am on Fremont Street",
    "Reasons Someone is Running Through a Casino",
    "What's in a Stranger's Cup at the Craps Table",
    "Things You Find in a Vegas Hotel Room That Weren't Yours",
    "Excuses for Being Down $3,000",
    "Things the Uber Driver Has Seen This Week",
    "What Happened in Vegas That Definitely Won't Stay There",
    "Reasons the Bachelor Party Got Kicked Out",
    "Things a Vegas Magician Says",
    "Jobs That Only Exist in Vegas",

    # Degenerate Gambling
    "Poker Hands",
    "Reasons You're Down Bad at the Tables",
    "Things High Rollers Say",
    "Ways to Lose Money Faster",
    "Things Overheard at the Sportsbook",
    "VIP Bottle Service Excuses",
    "Casino Chip Colors",
    "Card Counting Techniques",
    "Things a Casino Cheater Would Say",
    "Reasons You're Banned from the Bellagio",

    # Only in Vegas
    "Drive-Thru Wedding Chapel Names",
    "Celebrity Residency Acts",
    "Things on a Vegas Pawn Shop Shelf",
    "Reasons Someone is Crying Outside a Casino",
    "What the Guy in Head-to-Toe Affliction is Doing",
    "Names of Fake Elvis Impersonators",
    "Things Sold on the Strip for $20",
    "Vegas Wedding Regrets",
    "Things People Lie About When They Get Home",
    "Reasons to Visit the 24hr Wedding Chapel at 3am",

    # Unhinged Energy
    "What's in the Mystery Cocktail",
    "Cirque du Soleil Act Names",
    "Things the Vegas Taxi Driver Says",
    "Crimes Committed on the Strip",
    "Reasons the Pool Party Got Shut Down",
    "Things a Vegas Instagram Influencer Posts",
    "What's Inside the Mystery Bag at the Pawn Shop",
    "Nicknames for Regular Gamblers",
    "Things You Regret Buying at 2am",
    "Occupations of People at the Roulette Table",
]

# ── Session State Init ─────────────────────────────────────────────────────────

def init_state():
    defaults = {
        "phase": "setup",
        "num_players": 4,
        "num_imposters": 1,
        "roles": {},
        "category": None,
        "current_view_index": 0,
        "seen": set(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def reset_game():
    for k in ["phase", "num_players", "num_imposters", "roles", "category", "current_view_index", "seen"]:
        if k in st.session_state:
            del st.session_state[k]
    init_state()

def start_game(num_players, num_imposters):
    indices = list(range(num_players))
    imposters = set(random.sample(indices, num_imposters))
    roles = {i: ("imposter" if i in imposters else "civilian") for i in indices}
    category = random.choice(CATEGORIES)

    st.session_state.phase = "reveal"
    st.session_state.roles = roles
    st.session_state.category = category
    st.session_state.current_view_index = 0
    st.session_state.seen = set()

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
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PHASE: SETUP
# ══════════════════════════════════════════════════════════════════════════════

if st.session_state.phase == "setup":
    st.title("🕵️ Imposter Game")
    st.markdown("Everyone gets a **category** to discuss — but imposters don't know what it is. Find them before they fool you!")
    st.divider()

    num_players = st.slider("Number of players", min_value=3, max_value=12, value=st.session_state.num_players)
    st.session_state.num_players = num_players

    max_imposters = max(1, num_players // 3)
    num_imposters = st.slider("Number of imposters", min_value=1, max_value=max_imposters, value=min(st.session_state.num_imposters, max_imposters))
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

        if role == "civilian":
            st.markdown('<div class="role-box civilian-box">✅ CIVILIAN</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center"><span class="category-box">Category: {category}</span></div>', unsafe_allow_html=True)
            st.caption("You know the category. Discuss it without giving it away to the imposters!")
        else:
            st.markdown('<div class="role-box imposter-box">🔴 IMPOSTER</div>', unsafe_allow_html=True)
            st.markdown('<div style="text-align:center"><span class="category-box" style="background:#2e1a1a;color:#f87171">Category: ???</span></div>', unsafe_allow_html=True)
            st.caption("You don't know the category. Bluff your way through the discussion!")

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
    st.markdown("Imposters — bluff! Civilians — be specific enough to prove yourself without being too obvious.")
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