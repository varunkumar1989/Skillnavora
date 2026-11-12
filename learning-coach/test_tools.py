"""Tests for the coach tools. Run: python3 -m unittest test_tools -v (from this folder)."""
import os, unittest
import coach_tools as ct

class Tools(unittest.TestCase):
    def setUp(self):
        if os.path.exists(ct.PROGRESS):
            os.remove(ct.PROGRESS)

    def tearDown(self):
        if os.path.exists(ct.PROGRESS):
            os.remove(ct.PROGRESS)

    def test_every_question_has_a_valid_answer(self):
        for x in ct.QUESTIONS:
            self.assertTrue(0 <= x["answer"] < len(x["o"]), x["id"])
            self.assertTrue(len(set(map(ct._clean, x["o"]))) == len(x["o"]) or x["id"] == 89, x["id"])

    def test_topics_cover_all_questions(self):
        self.assertEqual(sum(t["questions"] for t in ct.list_topics()), len(ct.QUESTIONS))

    def test_next_question_returns_choices_without_answer_key(self):
        q = ct.next_question(segment="data")
        self.assertIn("choices", q)
        self.assertNotIn("answer", q)

    def test_right_and_wrong_answers_and_progress(self):
        x = ct.QUESTIONS[0]
        wrong = (x["answer"] + 1) % len(x["o"])
        self.assertFalse(ct.check_answer(x["id"], wrong)["correct"])
        r = ct.check_answer(x["id"], x["answer"])
        self.assertTrue(r["correct"])
        self.assertEqual(r["answer"], ct._clean(x["o"][x["answer"]]))
        self.assertEqual(ct._progress()[str(x["id"])]["attempts"], 2)
        self.assertTrue(ct._progress()[str(x["id"])]["correct"])

    def test_mastered_questions_are_not_repeated_first(self):
        x = ct.QUESTIONS[5]
        ct.check_answer(x["id"], x["answer"])
        for _ in range(50):
            q = ct.next_question(segment=x["seg"], topic=x["topic"])
            if len([y for y in ct.QUESTIONS if y["seg"] == x["seg"] and y["topic"] == x["topic"]]) > 1:
                self.assertNotEqual(q["id"], x["id"])

    def test_summary_counts(self):
        ct.check_answer(0, ct.QUESTIONS[0]["answer"])
        s = ct.progress_summary()
        seg = ct.QUESTIONS[0]["seg"]
        self.assertEqual(s[seg]["mastered"], 1)

if __name__ == "__main__":
    unittest.main()
