import unittest

from scripts.validate_repo import ValidationError, validate_anti_concentration


def work(designer="A", label="L", country="C", genre="G", sources=None):
    return {
        "designer": designer,
        "label": label,
        "country": country,
        "genre": genre,
        "evidence_source_ids": sources or ["source-a", "source-b"],
    }


LIMITS = {"designer": 3, "label": 6, "country": 16, "genre": 18, "source": 12}


class AntiConcentrationTest(unittest.TestCase):
    def test_accepts_values_at_limits(self):
        validate_anti_concentration([work() for _ in range(3)], LIMITS)

    def test_rejects_designer_above_limit(self):
        with self.assertRaisesRegex(ValidationError, "designer concentration"):
            validate_anti_concentration([work() for _ in range(4)], LIMITS)

    def test_rejects_source_above_limit(self):
        works = [
            work(designer=str(index), label=str(index), country=str(index), genre=str(index),
                 sources=["shared", str(index)])
            for index in range(13)
        ]
        with self.assertRaisesRegex(ValidationError, "source concentration"):
            validate_anti_concentration(works, LIMITS)
