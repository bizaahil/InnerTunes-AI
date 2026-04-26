from typing import List, Dict, Tuple
from dataclasses import dataclass
from collections import Counter
import csv


@dataclass
class Song:
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    InnerTunes AI recommender.

    This class scores songs, explains recommendations,
    estimates confidence, and checks for filter bubble risk.
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
            reasons.append("genre match")

        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.5
            reasons.append("mood match")

        energy_similarity = 1.0 - abs(song.energy - user.target_energy)
        energy_similarity = max(0.0, energy_similarity)
        score += energy_similarity
        reasons.append(f"energy similarity {energy_similarity:.2f}")

        if user.likes_acoustic and song.acousticness >= 0.65:
            score += 1.0
            reasons.append("matches acoustic preference")

        if not user.likes_acoustic and song.acousticness < 0.65:
            score += 0.5
            reasons.append("matches non-acoustic preference")

        return score, reasons

    def confidence_score(self, user: UserProfile, song: Song) -> float:
        score, _ = self.score_song(user, song)
        max_score = 5.5
        confidence = score / max_score
        return round(min(confidence, 1.0), 2)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        if not self.songs:
            return []

        scored_songs = []

        for song in self.songs:
            score, _ = self.score_song(user, song)
            scored_songs.append((song, score))

        scored_songs.sort(key=lambda item: item[1], reverse=True)

        return [song for song, score in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self.score_song(user, song)
        confidence = self.confidence_score(user, song)

        if not reasons:
            return "This song was recommended as a fallback because no strong preference match was found."

        return (
            f"Recommended because of: {', '.join(reasons)}. "
            f"Match score: {score:.2f}. "
            f"Confidence: {confidence:.0%}."
        )

    def detect_filter_bubble(self, recommendations: List[Song]) -> str:
        if not recommendations:
            return "No recommendations available to evaluate for bias."

        genre_counts = Counter(song.genre for song in recommendations)
        most_common_genre, count = genre_counts.most_common(1)[0]

        percentage = count / len(recommendations)

        if percentage >= 0.60:
            return (
                f"Filter bubble warning: {percentage:.0%} of recommendations are "
                f"{most_common_genre}. The system may be over-favoring one genre."
            )

        return "No major filter bubble detected. Recommendations are reasonably diverse."


def load_songs(csv_path: str) -> List[Dict]:
    songs = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)

    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    score = 0.0
    reasons = []

    if song["genre"].lower() == user_prefs.get("favorite_genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"].lower() == user_prefs.get("favorite_mood", "").lower():
        score += 1.5
        reasons.append("mood match (+1.5)")

    target_energy = user_prefs.get("target_energy", 0.5)
    energy_similarity = 1.0 - abs(song["energy"] - target_energy)
    energy_similarity = max(0.0, energy_similarity)

    score += energy_similarity
    reasons.append(f"energy similarity (+{energy_similarity:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic", False)

    if likes_acoustic and song["acousticness"] >= 0.65:
        score += 1.0
        reasons.append("acoustic preference match (+1.0)")

    if not likes_acoustic and song["acousticness"] < 0.65:
        score += 0.5
        reasons.append("non-acoustic preference match (+0.5)")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    scored = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        confidence = min(score / 5.5, 1.0)
        explanation = ", ".join(reasons) + f", confidence: {confidence:.0%}"
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]