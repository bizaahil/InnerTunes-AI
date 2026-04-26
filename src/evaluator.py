from recommender import Recommender, UserProfile, Song


class Evaluator:
    """
    Runs reliability tests on the recommender system.
    """

    def __init__(self, recommender: Recommender):
        self.recommender = recommender

    def run_tests(self):
        print("\n--- Running Reliability Tests ---\n")

        test_cases = [
            {
                "name": "High Energy Pop User",
                "profile": UserProfile("pop", "happy", 0.9, False),
            },
            {
                "name": "Low Energy Acoustic User",
                "profile": UserProfile("folk", "sad", 0.2, True),
            },
            {
                "name": "Mixed Preferences User",
                "profile": UserProfile("rock", "chill", 0.5, False),
            },
            {
                "name": "Edge Case (Unknown Genre)",
                "profile": UserProfile("unknown", "happy", 0.7, False),
            },
        ]

        results = []

        for test in test_cases:
            print(f"\nTest: {test['name']}")

            recommendations = self.recommender.recommend(test["profile"], k=5)

            if not recommendations:
                print("❌ No recommendations returned")
                results.append(False)
                continue

            print("Top Recommendation:", recommendations[0].title)

            explanation = self.recommender.explain_recommendation(
                test["profile"], recommendations[0]
            )
            print("Explanation:", explanation)

            confidence = self.recommender.confidence_score(
                test["profile"], recommendations[0]
            )
            print("Confidence:", confidence)

            if confidence < 0.3:
                print("⚠️ Low confidence recommendation")
                results.append(False)
            else:
                results.append(True)

        passed = sum(results)
        total = len(results)

        print(f"\n--- Test Summary ---")
        print(f"{passed} / {total} tests passed")

        return passed, total