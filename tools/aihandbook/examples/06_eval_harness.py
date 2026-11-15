# Week 4, Subject 13: a tiny evaluation harness with a golden dataset
GOLDEN = [
    {"question": "How many paid leave days per year?", "must_contain": "20"},
    {"question": "How many days can leave be carried forward?", "must_contain": "5"},
    {"question": "Who approves remote work?", "must_contain": "manager"},
    {"question": "What is the CEO's salary?", "must_contain": "not in the document"},
]

def system_under_test(question):
    answers = {
        "How many paid leave days per year?": "You get 20 days of paid leave.",
        "How many days can leave be carried forward?": "Up to 5 days.",
        "Who approves remote work?": "Your manager approves it.",
        "What is the CEO's salary?": "The CEO earns 5 crore.",  # a hallucination the test should catch
    }
    return answers[question]

passed = 0
for case in GOLDEN:
    answer = system_under_test(case["question"])
    ok = case["must_contain"].lower() in answer.lower()
    passed += ok
    status = "PASS" if ok else "FAIL"
    print(f"{status}  {case['question']}  ->  {answer}")
print(f"Score: {passed}/{len(GOLDEN)} ({passed / len(GOLDEN):.0%})")
