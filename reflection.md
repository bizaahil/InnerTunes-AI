# Reflection: Music Recommender Simulation

## Profile Comparisons

**High-Energy Pop vs. Chill Lofi**
Both profiles found strong #1 matches (3.92 and 3.98 respectively), but for opposite reasons. The pop profile won because Sunrise City matched genre, mood, and energy all at once. The lofi profile won because the catalog has multiple lofi + chill songs, giving it real competition. The difference makes sense — pop is a well-represented genre here, and so is lofi.

**Deep Intense Rock vs. Unknown Genre (Reggae)**
Rock got a near-perfect #1 (Storm Runner, 3.96) while reggae's best result was only 1.84. The rock user got lucky — there happened to be one perfect match. The reggae user got nothing because the genre doesn't exist in the catalog. This exposes a real fairness problem: your score out of 4.0 depends heavily on whether your taste is represented in the dataset, not on how well the system works.

**Why does Gym Hero keep showing up for Happy Pop users?**
Gym Hero is a pop song, so it immediately gets +2.0 points — the same as Sunrise City. Its mood is "intense" not "happy," so it misses the +1.0 mood bonus. But because genre is worth twice as much as mood, it still outscores non-pop songs that do match the happy mood. In plain terms: the system cares more about genre labels than it does about how the song actually feels. A real recommender would need to weigh mood more heavily, or learn from whether users actually skip the song.
