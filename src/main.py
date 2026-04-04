"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.4,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.95,
    },
    # Edge cases
    "Conflicting (sad + high energy)": {
        "favorite_genre": "classical",
        "favorite_mood": "sad",
        "target_energy": 0.9,
    },
    "Unknown Genre": {
        "favorite_genre": "reggae",
        "favorite_mood": "happy",
        "target_energy": 0.6,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in PROFILES.items():
        print("\n" + "=" * 45)
        print(f"  Profile: {profile_name}")
        print("=" * 45)

        recommendations = recommend_songs(user_prefs, songs, k=5)
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n  #{i} {song['title']} by {song['artist']}")
            print(f"      Score : {score:.2f} / 4.00")
            print(f"      Why   : {explanation}")


if __name__ == "__main__":
    main()
