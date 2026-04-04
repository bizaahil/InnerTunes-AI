# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests songs from a small catalog based on a user's preferred genre, mood, and energy level. It assumes the user can describe their taste with a single genre and mood label, and that those labels are present in the catalog. This system is built for classroom exploration only — it is not designed for real users or production use.

---

## 3. How the Model Works

Every song in the catalog gets a score based on how well it matches the user's preferences. The system checks three things:

1. **Genre** — if the song's genre matches what the user listed as their favorite, it gets the most points (+2.0). Genre is weighted the highest because it's the broadest signal of taste.
2. **Mood** — if the song's mood matches (e.g. chill, happy, intense), it gets +1.0 points.
3. **Energy** — the closer a song's energy level is to the user's target, the more points it earns (up to +1.0). This rewards songs that feel the right intensity, not just ones that are generically high or low energy.

After every song is scored, the list is sorted from highest to lowest and the top 5 are returned as recommendations, each with an explanation of why it ranked where it did.

---

## 4. Data

The catalog contains 18 songs across 12 genres including pop, lofi, rock, hip-hop, r&b, jazz, ambient, electronic, folk, country, metal, and classical. Moods represented include happy, chill, intense, focused, melancholic, confident, romantic, angry, sad, soulful, nostalgic, euphoric, relaxed, and moody. 8 songs were added to the original 10-song starter dataset to improve genre and mood diversity. Parts of musical taste still missing include latin, gospel, reggae, and world music genres, and the catalog skews toward Western popular music styles.

---

## 5. Strengths

The system works best for users whose favorite genre is well-represented in the catalog — particularly lofi and pop users, who have multiple songs to compete for the top spot. The scoring logic correctly captures the difference between a Chill Lofi listener and a Deep Intense Rock listener without any overlap in their top results. The energy similarity calculation is a strength: it rewards songs that are close to the user's target rather than just high or low, which makes recommendations feel tuned rather than arbitrary. The explanation output ("genre match +2.0, mood match +1.0, energy similarity +0.98") makes the system transparent and easy to audit.

---

## 6. Limitations and Bias

The system has a structural genre bias — with genre worth +2.0 out of a max 4.0 points, any song in the wrong genre can never outscore a mediocre genre match, even if it perfectly matches mood and energy. This creates a filter bubble where users are locked into their declared genre regardless of how well other songs actually fit their vibe.

The energy gap calculation also introduces a subtle bias against low-energy users. Because energy similarity is calculated as `1.0 - abs(difference)`, a user with `target_energy=0.2` will rarely see high scores from this feature alone — but a user targeting `0.5` benefits from the widest range of songs scoring reasonably well, giving them more variety by default.

The catalog itself is the biggest source of bias — 18 songs spread across 12 genres means some genres (lofi, pop) have 2–3 songs while most have only 1. A user whose favorite genre is reggae, blues, or classical gets no genre points at all on most songs, making their recommendations essentially random compared to a pop or lofi user. The system does not account for this imbalance.

---

## 7. Evaluation

Five user profiles were tested: High-Energy Pop, Chill Lofi, Deep Intense Rock, Conflicting (classical/sad/high energy), and Unknown Genre (reggae).

**What I looked for:** Whether the top-ranked song matched what a real listener with that profile would actually want, and whether scores felt proportional to the quality of the match.

**Results:**
- High-Energy Pop and Chill Lofi both returned strong #1 results (3.92 and 3.98/4.00) that matched intuition well
- Deep Intense Rock found its perfect match (Storm Runner, 3.96) but only because one song happened to exist in the catalog
- The Conflicting profile exposed a weakness — Winter Piano ranked #1 at 3.32 despite its energy (0.22) being completely opposite to the user's target (0.9); genre + mood weight dominated
- The Unknown Genre (reggae) profile maxed out at 1.84/4.00 because no reggae songs exist in the catalog, making recommendations essentially energy-only guesses

**Experiment:** Halved genre weight to +1.0 and doubled energy to ×2.0. Top results stayed the same but cross-genre songs scored significantly higher, confirming the system is weight-sensitive even when rankings don't shift at the top.

**What surprised me:** Gym Hero kept appearing in Happy Pop results at #2 despite its mood being "intense" not "happy." Genre weight alone (+2.0) was enough to outrank songs that matched mood but not genre — revealing that the scoring logic prioritizes label over feel.

---

## 8. Future Work

- **Lower genre dominance** — reduce genre to +1.5 and raise mood to +1.5 so emotional feel competes more equally with genre labels
- **Add a secondary genre preference** — let users specify a fallback genre (e.g. "I like lofi but also ambient") so the catalog gap problem is less punishing
- **Improve catalog balance** — ensure every genre has at least 3 songs so recommendations don't collapse to energy-only guessing for underrepresented users
- **Learn from skips** — track whether users skip or replay recommended songs and adjust weights over time, moving toward a hybrid collaborative + content-based approach

---

## 9. Personal Reflection

The biggest learning moment in this project was seeing how much a simple numeric weight controls the entire behavior of the system. Changing genre from +2.0 to +1.0 didn't flip the rankings, but it changed how competitive every other song became — which is exactly how real systems get tuned. Using AI tools helped with brainstorming the scoring logic and identifying edge cases I wouldn't have thought to test, like a user with conflicting preferences (sad mood + high energy). But I had to double-check the outputs manually, because the AI suggestions always sounded reasonable even when the math revealed a flaw.

What surprised me most was that such a simple algorithm — three rules, some addition, a sort — can still feel like a real recommendation. When Midnight Coding came up as #1 for a Chill Lofi profile with a 3.98/4.00, it genuinely felt correct. That made me realize that real recommenders like Spotify aren't magic — they're doing something similar at a much larger scale with many more features. The difference is they have millions of users to learn from, and we only had rules we wrote by hand.
