"""
Command line runner for InnerTunes AI.

This file runs the full applied AI system:
- loads song data
- recommends songs
- explains recommendations
- checks filter bubble risk
- runs reliability evaluation
"""

from recommender import (
    load_songs,
    recommend_songs,
    Recommender,
    Song,
)

from evaluator import Evaluator


PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.4,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.95,
        "likes_acoustic": False,
    },
    "Conflicting Sad + High Energy": {
        "favorite_genre": "classical",
        "favorite_mood": "sad",
        "target_energy": 0.9,
        "likes_acoustic": True,
    },
    "Unknown Genre": {
        "favorite_genre": "reggae",
        "favorite_mood": "happy",
        "target_energy": 0.6,
        "likes_acoustic": False,
    },
}


def main() -> None:
    songs_data = load_songs("data/songs.csv")

    # Convert CSV dictionaries into Song objects for the full AI system.
    songs = [Song(**song) for song in songs_data]

    recommender = Recommender(songs)

    for profile_name, user_prefs in PROFILES.items():
        print("\n" + "=" * 45)
        print(f"  Profile: {profile_name}")
        print("=" * 45)

        recommendations = recommend_songs(user_prefs, songs_data, k=5)

        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n  #{i} {song['title']} by {song['artist']}")
            print(f"      Score : {score:.2f}")
            print(f"      Why   : {explanation}")

        object_recommendations = recommender.recommend(
            user=type(
                "UserProfileLike",
                (),
                user_prefs,
            )(),
            k=5,
        )

        print("\n  Diversity Check:")
        print(f"      {recommender.detect_filter_bubble(object_recommendations)}")

    evaluator = Evaluator(recommender)
    evaluator.run_tests()


if __name__ == "__main__":
    main()