"""Practice Lab challenges. Each challenge: a small table, code that looks right, a trap, a hint and the fix.
engine: sql (SQLite in the browser), excel (formula engine), python (Pyodide), decide (read the result and decide), scenario (choose the best option)."""

ORDERS = {"name": "orders", "cols": ["order_id", "customer", "city", "amount", "status", "coupon"],
          "rows": [[101, "Asha", "Mumbai", 1200, "completed", "NEW10"], [102, "Ravi", "Mumbai", 800, "cancelled", None], [103, "Asha", "Mumbai", 500, "completed", None],
                   [104, "Neha", "Delhi", 900, "completed", "FEST"], [105, "Kabir", "Mumbai", 300, "completed", None], [106, "Ravi", "Pune", 700, "completed", None]]}
EMP = {"name": "employees", "cols": ["emp_id", "name", "dept", "salary", "manager_id"],
       "rows": [[1, "Meera", "Sales", 90000, None], [2, "Arjun", "Sales", 90000, 1], [3, "Divya", "Sales", 60000, 1], [4, "Rohan", "Tech", 120000, None], [5, "Sara", "Tech", 95000, 4], [6, "Vikram", "HR", None, None]]}
CUST = {"name": "customers", "cols": ["customer_id", "name", "city"], "rows": [[1, "Asha", "Mumbai"], [2, "Ravi", "Pune"], [3, "Neha", "Delhi"], [4, "Kabir", "Mumbai"]]}
ORD2 = {"name": "orders2", "cols": ["order_id", "customer_id", "amount"], "rows": [[1, 1, 500], [2, 1, 700], [3, 2, 300], [4, 3, 900]]}
DAILY = {"name": "daily_sales", "cols": ["day", "sales"], "rows": [["2026-10-01", 100], ["2026-10-02", 140], ["2026-10-03", 90], ["2026-10-04", 160], ["2026-10-05", 120]]}
STORE_A = {"name": "store_a", "cols": ["product", "price"], "rows": [["Pen", 10], ["Book", 50], ["Bag", 300]]}
STORE_B = {"name": "store_b", "cols": ["product", "price"], "rows": [["Pen", 10], ["Lamp", 200]]}

C = []
def add(**k): C.append(k)

# ---------------------------------------------------------------- SQL (runs in SQLite)
add(id="sql-select", seg="data", sec="SQL", topic="Basics", level="Basic", title="Show only Mumbai orders", tagline="Filter rows with WHERE",
    q="Show all orders from Mumbai.", tables=[ORDERS], engine="sql", code="SELECT *\nFROM orders\nWHERE city = 'mumbai';",
    trap="Text comparison is case-sensitive here: 'mumbai' is not 'Mumbai', so no rows come back.", hint="Look at how Mumbai is written inside the table.",
    fix="SELECT *\nFROM orders\nWHERE city = 'Mumbai';", ask="Did you get the 4 Mumbai orders?", answer="off")
add(id="sql-cancelled", seg="data", sec="SQL", topic="Business metrics", level="Basic", title="Total revenue from Mumbai", tagline="Which rows should count?",
    q="What's the total revenue from Mumbai?", tables=[ORDERS], engine="sql", code="SELECT SUM(amount) AS revenue\nFROM orders\nWHERE city = 'Mumbai';",
    trap="Order 102 was cancelled. Cancelled orders are not revenue, so 2,800 is too high. The right answer is 2,000.", hint="Look at the status column.",
    fix="SELECT SUM(amount) AS revenue\nFROM orders\nWHERE city = 'Mumbai'\n  AND status = 'completed';", ask="Is 2,800 the right revenue?", answer="off")
add(id="sql-count-distinct", seg="data", sec="SQL", topic="Counting & GROUP BY", level="Basic", title="How many customers ordered?", tagline="Count people, not rows",
    q="How many different customers placed an order?", tables=[ORDERS], engine="sql", code="SELECT COUNT(customer) AS customers\nFROM orders;",
    trap="COUNT(customer) counts rows, so Asha and Ravi are counted twice. There are 4 different customers.", hint="Some names appear more than once.",
    fix="SELECT COUNT(DISTINCT customer) AS customers\nFROM orders;", ask="Is 6 the number of customers?", answer="off")
add(id="sql-null-count", seg="data", sec="SQL", topic="NULLs", level="Basic", title="Orders without a coupon", tagline="NULL is not equal to anything",
    q="How many orders were placed without a coupon?", tables=[ORDERS], engine="sql", code="SELECT COUNT(*) AS no_coupon\nFROM orders\nWHERE coupon = NULL;",
    trap="Nothing is ever '= NULL', not even NULL. You must write IS NULL. The answer is 4.", hint="NULL means 'unknown'. Is unknown equal to unknown?",
    fix="SELECT COUNT(*) AS no_coupon\nFROM orders\nWHERE coupon IS NULL;", ask="Is 0 the right count?", answer="off")
add(id="sql-avg-null", seg="data", sec="SQL", topic="NULLs", level="Intermediate", title="Average salary in the company", tagline="AVG skips NULLs",
    q="What is the average salary of all employees? (Vikram's salary is not entered yet.)", tables=[EMP], engine="sql", code="SELECT AVG(salary) AS avg_salary\nFROM employees;",
    trap="AVG ignores NULL, so it averages 5 people, not 6. That is fine if you want 'average of known salaries', but say so. If missing should count as 0, use COALESCE.", hint="How many salaries are actually filled in?",
    fix="SELECT AVG(salary) AS avg_known_salaries,\n       AVG(COALESCE(salary, 0)) AS avg_if_missing_is_zero,\n       COUNT(salary) AS people_with_salary\nFROM employees;", ask="Is this the average for all 6 employees?", answer="off")
add(id="sql-groupby", seg="data", sec="SQL", topic="Counting & GROUP BY", level="Intermediate", title="Revenue by city", tagline="WHERE vs HAVING",
    q="Show cities whose completed revenue is above 1,000.", tables=[ORDERS], engine="sql", code="SELECT city, SUM(amount) AS revenue\nFROM orders\nGROUP BY city\nHAVING revenue > 1000;",
    trap="The HAVING part is fine, but cancelled orders are still counted, so Mumbai shows 2,800 instead of 2,000. Filter rows with WHERE before grouping.", hint="Which rows should be removed before you add them up?",
    fix="SELECT city, SUM(amount) AS revenue\nFROM orders\nWHERE status = 'completed'\nGROUP BY city\nHAVING SUM(amount) > 1000;", ask="Is Mumbai's revenue right?", answer="off")
add(id="sql-left-join", seg="data", sec="SQL", topic="JOINs", level="Intermediate", title="Every customer and their spend", tagline="INNER JOIN drops people",
    q="List every customer with their total spend (0 if they never ordered).", tables=[CUST, ORD2], engine="sql",
    code="SELECT c.name, SUM(o.amount) AS spend\nFROM customers c\nJOIN orders2 o ON o.customer_id = c.customer_id\nGROUP BY c.name;",
    trap="An inner JOIN keeps only customers who have orders, so Kabir disappears. Use LEFT JOIN and COALESCE to show 0.", hint="Count the customers in the result. Who is missing?",
    fix="SELECT c.name, COALESCE(SUM(o.amount), 0) AS spend\nFROM customers c\nLEFT JOIN orders2 o ON o.customer_id = c.customer_id\nGROUP BY c.name;", ask="Are all 4 customers listed?", answer="off")
add(id="sql-union", seg="data", sec="SQL", topic="Subqueries & sets", level="Intermediate", title="Combine two stores' sales", tagline="UNION removes duplicates",
    q="Combine both stores' sales lines to calculate total sales.", tables=[STORE_A, STORE_B], engine="sql",
    code="SELECT SUM(price) AS total FROM (\n  SELECT product, price FROM store_a\n  UNION\n  SELECT product, price FROM store_b\n);",
    trap="UNION removes duplicate rows. Both stores sold a Pen for 10, so one real sale vanished: 560 instead of 570. Use UNION ALL for real transactions.", hint="Does any row appear in both stores?",
    fix="SELECT SUM(price) AS total FROM (\n  SELECT product, price FROM store_a\n  UNION ALL\n  SELECT product, price FROM store_b\n);", ask="Is 560 the total of all sales?", answer="off")
add(id="sql-top-tie", seg="data", sec="SQL", topic="Ranking & ties", level="Advanced", title="Highest paid in each department", tagline="Decide what a tie means",
    q="Who is the highest-paid employee in each department?", tables=[EMP], engine="sql",
    code="SELECT dept, name, salary\nFROM (\n  SELECT dept, name, salary,\n         ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn\n  FROM employees\n)\nWHERE rn = 1;",
    trap="Meera and Arjun both earn 90,000 in Sales. ROW_NUMBER picks only one of them at random. Use RANK (or DENSE_RANK) so ties are kept.", hint="Look at the Sales salaries.",
    fix="SELECT dept, name, salary\nFROM (\n  SELECT dept, name, salary,\n         RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk\n  FROM employees\n  WHERE salary IS NOT NULL\n)\nWHERE rnk = 1;", ask="Does Sales show everyone who is top paid?", answer="off")
add(id="sql-running", seg="data", sec="SQL", topic="Window functions", level="Advanced", title="Running total of daily sales", tagline="ORDER BY inside OVER",
    q="Show each day's sales and the running total so far.", tables=[DAILY], engine="sql",
    code="SELECT day, sales,\n       SUM(sales) OVER () AS running_total\nFROM daily_sales\nORDER BY day;",
    trap="OVER () with nothing inside sums the whole table on every row (610). A running total needs ORDER BY day inside OVER.", hint="Should the first day's running total be 610?",
    fix="SELECT day, sales,\n       SUM(sales) OVER (ORDER BY day) AS running_total\nFROM daily_sales\nORDER BY day;", ask="Is the running total right on day 1?", answer="off")
add(id="sql-lag", seg="data", sec="SQL", topic="Window functions", level="Advanced", title="Day-on-day change", tagline="LAG looks at the previous row",
    q="Show how much sales changed compared with the previous day.", tables=[DAILY], engine="sql",
    code="SELECT day, sales,\n       sales - LAG(sales) OVER (ORDER BY day) AS change\nFROM daily_sales;",
    trap="This one is correct! The first day has no previous day, so its change is NULL, which is exactly right.", hint="Check day 2: 140 − 100.",
    fix="SELECT day, sales,\n       sales - LAG(sales) OVER (ORDER BY day) AS change\nFROM daily_sales;", ask="Is this query right?", answer="right")
add(id="sql-self-join", seg="data", sec="SQL", topic="JOINs", level="Advanced", title="Employees and their managers", tagline="Join a table to itself",
    q="List every employee with their manager's name (blank if no manager).", tables=[EMP], engine="sql",
    code="SELECT e.name AS employee, m.name AS manager\nFROM employees e\nJOIN employees m ON e.manager_id = m.emp_id;",
    trap="The inner join hides people without a manager (Meera, Rohan, Vikram). Use LEFT JOIN so everyone appears.", hint="How many of the 6 employees are shown?",
    fix="SELECT e.name AS employee, m.name AS manager\nFROM employees e\nLEFT JOIN employees m ON e.manager_id = m.emp_id;", ask="Is every employee listed?", answer="off")

# ---------------------------------------------------------------- Excel (formula engine, cells A1.. from the table)
SALES_X = {"name": "Sheet1", "cols": ["Region", "Product", "Units", "Price", "Sales"],
           "rows": [["North", "Pen", 10, 20, 200], ["South", "Book", 5, 120, 600], ["South", "Pen", 8, 20, 160], ["East", "Bag", 2, 900, 1800], ["North", "Book", "", 120, 0], ["West", "Lamp", 3, 150, 450]]}
add(id="xl-sum", seg="data", sec="Excel", topic="Basics", level="Basic", title="Total sales", tagline="SUM a range",
    q="Find the total of the Sales column (E2:E7).", tables=[SALES_X], engine="excel", code="=SUM(E2:E6)",
    trap="The range stops at row 6, so row 7 (West, 450) is left out. Always check the range covers every row.", hint="How many data rows are there?",
    fix="=SUM(E2:E7)", ask="Does this include every row?", answer="off")
add(id="xl-average-blank", seg="data", sec="Excel", topic="Basics", level="Basic", title="Average units sold", tagline="Blanks vs zeros",
    q="What is the average number of units sold (C2:C7)? Row 6 has no units entered yet.", tables=[SALES_X], engine="excel", code="=AVERAGE(C2:C7)",
    trap="This is right if a blank means 'not entered yet': AVERAGE skips empty cells and divides by 5. If a blank should count as 0, use =SUM(C2:C7)/ROWS(C2:C7).", hint="AVERAGE ignores empty cells.",
    fix="=AVERAGE(C2:C7)", ask="Is 5.6 a correct average of the entered units?", answer="right")
add(id="xl-sumif", seg="data", sec="Excel", topic="Conditional sums", level="Basic", title="Sales in the South", tagline="SUMIF picks rows",
    q="Total sales for the South region.", tables=[SALES_X], engine="excel", code='=SUMIF(A2:A7,"South",D2:D7)',
    trap="The sum range is D (Price), not E (Sales), so it adds prices: 140 instead of 760.", hint="Which column holds sales?",
    fix='=SUMIF(A2:A7,"South",E2:E7)', ask="Is 140 the South sales?", answer="off")
add(id="xl-countif", seg="data", sec="Excel", topic="Conditional sums", level="Basic", title="How many Pen orders?", tagline="COUNTIF counts matches",
    q="Count how many rows are for the product Pen.", tables=[SALES_X], engine="excel", code='=COUNTIF(B2:B7,"Pen")',
    trap="This one is correct: two rows sell Pens.", hint="Count the Pen rows yourself.", fix='=COUNTIF(B2:B7,"Pen")', ask="Is 2 right?", answer="right")
add(id="xl-if", seg="data", sec="Excel", topic="Logical", level="Intermediate", title="Big order flag", tagline="IF with the right sign",
    q="Show 'Big' when the sale in E5 is 1,000 or more, otherwise 'Small'.", tables=[SALES_X], engine="excel", code='=IF(E5>1000,"Big","Small")',
    trap="With > a sale of exactly 1,000 would be 'Small'. The rule says '1,000 or more', so use >=. (Here E5 is 1,800, but the formula must work for every row.)", hint="What happens for exactly 1,000?",
    fix='=IF(E5>=1000,"Big","Small")', ask="Does this formula follow the rule for every possible sale?", answer="off")
add(id="xl-sumproduct", seg="data", sec="Excel", topic="Advanced formulas", level="Intermediate", title="Check the Sales column", tagline="SUMPRODUCT",
    q="Total sales should equal Units × Price summed. Check it with one formula.", tables=[SALES_X], engine="excel", code="=SUMPRODUCT(C2:C7,D2:D7)",
    trap="This is right: SUMPRODUCT multiplies each pair and adds them (3,210), which matches SUM(E2:E7) = 3,210.", hint="Compare with =SUM(E2:E7).",
    fix="=SUMPRODUCT(C2:C7,D2:D7)", ask="Is 3,210 correct?", answer="right")
add(id="xl-vlookup", seg="data", sec="Excel", topic="Lookups", level="Intermediate", title="Price of a Bag", tagline="Exact match",
    q="Look up the price of 'Bag' from the table (columns B to D).", tables=[SALES_X], engine="excel", code='=VLOOKUP("Bag",B2:D7,3,FALSE)',
    trap="This is right: FALSE means exact match, and column 3 of B:D is Price (900).", hint="Count columns starting from B.", fix='=VLOOKUP("Bag",B2:D7,3,FALSE)', ask="Is 900 right?", answer="right")
add(id="xl-percent", seg="data", sec="Excel", topic="Advanced formulas", level="Advanced", title="East's share of sales", tagline="Percent of total",
    q="What share of total sales comes from East (E5)?", tables=[SALES_X], engine="excel", code="=E5/SUM(E2:E6)",
    trap="The total leaves out row 7 (West). Use the whole range (and $ signs if you copy it down): =E5/SUM($E$2:$E$7).", hint="Is the total the full total?",
    fix="=E5/SUM($E$2:$E$7)", ask="Is this the right share?", answer="off")

# ---------------------------------------------------------------- Python (Pyodide)
add(id="py-sum", seg="data", sec="Python", topic="Basics", level="Basic", title="Total of a list", tagline="Loops and totals",
    q="Add up the order amounts.", engine="python", code="amounts = [1200, 800, 500, 900, 300, 700]\ntotal = 0\nfor a in amounts:\n    total = a\nprint(total)",
    trap="total = a replaces the total each time, so only the last amount (700) is left. Use total = total + a (or total += a, or sum()).", hint="What does total hold after each step?",
    fix="amounts = [1200, 800, 500, 900, 300, 700]\ntotal = 0\nfor a in amounts:\n    total += a\nprint(total)   # or print(sum(amounts))", ask="Is 700 the total?", answer="off")
add(id="py-range", seg="data", sec="Python", topic="Basics", level="Basic", title="Count from 1 to 5", tagline="range stops early",
    q="Print the numbers 1 to 5.", engine="python", code="for i in range(1, 5):\n    print(i)",
    trap="range(1, 5) stops before 5, so 5 is missing. Use range(1, 6).", hint="Does the output include 5?", fix="for i in range(1, 6):\n    print(i)", ask="Did it print 1 to 5?", answer="off")
add(id="py-int-input", seg="data", sec="Python", topic="Basics", level="Basic", title="Add two numbers typed as text", tagline="Text vs numbers",
    q="Two numbers arrived as text from a form. Add them.", engine="python", code='a = "10"\nb = "5"\nprint(a + b)',
    trap="Adding text joins it: '10' + '5' = '105'. Convert to numbers first with int().", hint="Is the answer 15?", fix='a = "10"\nb = "5"\nprint(int(a) + int(b))', ask="Is 105 right?", answer="off")
add(id="py-dict", seg="data", sec="Python", topic="Data structures", level="Intermediate", title="Count orders per city", tagline="Dictionaries",
    q="Count how many orders came from each city.", engine="python", code='cities = ["Mumbai", "Mumbai", "Delhi", "Mumbai", "Pune"]\ncounts = {}\nfor c in cities:\n    counts[c] = 1\nprint(counts)',
    trap="counts[c] = 1 resets the count each time, so every city shows 1. Add one instead: counts[c] = counts.get(c, 0) + 1.", hint="How many Mumbai orders are there?",
    fix='cities = ["Mumbai", "Mumbai", "Delhi", "Mumbai", "Pune"]\ncounts = {}\nfor c in cities:\n    counts[c] = counts.get(c, 0) + 1\nprint(counts)', ask="Does Mumbai show 3?", answer="off")
add(id="py-mutable", seg="data", sec="Python", topic="Data structures", level="Intermediate", title="Copy a list", tagline="Two names, one list",
    q="Make a copy of the price list and give a discount on the copy only.", engine="python", code="prices = [100, 200, 300]\nsale = prices\nsale[0] = 90\nprint('prices:', prices)\nprint('sale:', sale)",
    trap="sale = prices does not copy; both names point to the same list, so the original changed too. Use prices.copy() or list(prices).", hint="Did the original prices change?",
    fix="prices = [100, 200, 300]\nsale = prices.copy()\nsale[0] = 90\nprint('prices:', prices)\nprint('sale:', sale)", ask="Are the original prices unchanged?", answer="off")
add(id="py-average", seg="data", sec="Python", topic="Functions", level="Intermediate", title="Average function", tagline="Empty lists",
    q="Write a function that returns the average of a list.", engine="python", code="def average(nums):\n    return sum(nums) / len(nums)\n\nprint(average([4, 6, 8]))\nprint(average([]))",
    trap="An empty list makes len(nums) zero, and dividing by zero crashes. Handle the empty case.", hint="Run it: what happens on the second line?",
    fix="def average(nums):\n    if not nums:\n        return None\n    return sum(nums) / len(nums)\n\nprint(average([4, 6, 8]))\nprint(average([]))", ask="Does the function work for every list?", answer="off")
add(id="py-float", seg="data", sec="Python", topic="Functions", level="Advanced", title="Money with decimals", tagline="Floats are approximate",
    q="Check if 0.1 + 0.2 equals 0.3.", engine="python", code="print(0.1 + 0.2 == 0.3)",
    trap="Computers store decimals approximately, so 0.1 + 0.2 is 0.30000000000000004. Compare with round() or math.isclose(), and use Decimal or paise for money.", hint="Print 0.1 + 0.2 to see the real value.",
    fix="import math\nprint(0.1 + 0.2)\nprint(math.isclose(0.1 + 0.2, 0.3))\nprint(round(0.1 + 0.2, 2) == 0.3)", ask="Should this print True?", answer="off")
add(id="py-sorted", seg="data", sec="Python", topic="Data structures", level="Advanced", title="Top 2 customers by spend", tagline="Sort by value",
    q="Find the two customers who spent the most.", engine="python", code='spend = {"Asha": 1700, "Ravi": 1500, "Neha": 900, "Kabir": 300}\ntop = sorted(spend)[:2]\nprint(top)',
    trap="sorted(spend) sorts the names alphabetically, not by money. Sort by the values, highest first.", hint="Is Asha (1,700) first because of money or because of the letter A?",
    fix='spend = {"Asha": 1700, "Ravi": 1500, "Neha": 900, "Kabir": 300}\ntop = sorted(spend, key=spend.get, reverse=True)[:2]\nprint(top)', ask="Is this sorted by spend?", answer="off")

# ---------------------------------------------------------------- Machine learning (Python, no libraries needed)
add(id="ml-accuracy", seg="data", sec="ML", topic="Model evaluation", level="Basic", title="99% accurate fraud model?", tagline="Accuracy on rare events",
    q="A model says 'not fraud' for every transaction. Is 99% accuracy good?", engine="python",
    code="actual = [0]*99 + [1]          # 1 = fraud, only 1 in 100\npredicted = [0]*100           # model always says 'not fraud'\naccuracy = sum(a == p for a, p in zip(actual, predicted)) / len(actual)\nprint('accuracy:', accuracy)",
    trap="With 1% fraud, a model that never finds fraud is still 99% accurate. Look at recall: it caught 0 of 1 frauds.", hint="How many frauds did it catch?",
    fix="actual = [0]*99 + [1]\npredicted = [0]*100\ntp = sum(a == 1 and p == 1 for a, p in zip(actual, predicted))\nrecall = tp / sum(actual)\nprint('accuracy:', sum(a == p for a, p in zip(actual, predicted)) / 100)\nprint('recall (frauds caught):', recall)", ask="Is this a good fraud model?", answer="off")
add(id="ml-leakage", seg="data", sec="ML", topic="Data preparation", level="Intermediate", title="Perfect churn model", tagline="Data leakage",
    q="A churn model uses the column 'days_since_cancellation' and gets 100% accuracy. Good news?", engine="decide", tables=[{"name": "customers", "cols": ["customer", "monthly_bill", "complaints", "days_since_cancellation", "churned"], "rows": [["A", 499, 0, None, 0], ["B", 799, 3, 12, 1], ["C", 299, 1, None, 0], ["D", 999, 4, 30, 1]]}],
    code="Features: monthly_bill, complaints, days_since_cancellation\nTest accuracy: 100%", result="100% accuracy",
    trap="days_since_cancellation only exists after a customer has churned, so it gives the answer away (leakage). Remove any column you would not know at prediction time.", hint="Would you know this column before the customer leaves?",
    fix="Features: monthly_bill, complaints   (drop days_since_cancellation)\nExpect a realistic accuracy and check recall on churners.", ask="Can we trust 100%?", answer="off")
add(id="ml-split", seg="data", sec="ML", topic="Model evaluation", level="Intermediate", title="Train and test on the same data", tagline="Overfitting",
    q="The model scores 98% on the data it was trained on. Ready to launch?", engine="decide", code="model.fit(X, y)\nscore = model.score(X, y)   # 0.98", result="0.98",
    trap="Scoring on the training data shows memory, not skill. Keep a test set the model never saw (train_test_split) or use cross-validation.", hint="Did the model ever see new data?",
    fix="X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nmodel.fit(X_train, y_train)\nprint(model.score(X_test, y_test))", ask="Is 98% a fair score?", answer="off")
add(id="ml-scaling", seg="data", sec="ML", topic="Data preparation", level="Advanced", title="KNN with income and age", tagline="Feature scaling",
    q="Find the nearest customer to a new person (age 30, income ₹50,000) using distance.", engine="python",
    code="import math\npeople = {'P1': (31, 90000), 'P2': (55, 51000)}\nnew = (30, 50000)\nfor k, (age, inc) in people.items():\n    print(k, round(math.dist(new, (age, inc))))",
    trap="Income is in thousands and age in tens, so income decides everything: P2 (age 55) looks 'nearest'. Scale features first (for example divide by the range).", hint="Who is really more similar to a 30-year-old?",
    fix="import math\npeople = {'P1': (31, 90000), 'P2': (55, 51000)}\nnew = (30, 50000)\nage_rng, inc_rng = 40, 100000\nfor k, (age, inc) in people.items():\n    print(k, round(math.dist((new[0]/age_rng, new[1]/inc_rng), (age/age_rng, inc/inc_rng)), 3))", ask="Is P2 really the most similar person?", answer="off")
add(id="ml-correlation", seg="data", sec="ML", topic="Statistics", level="Advanced", title="Ice cream causes drowning?", tagline="Correlation vs causation",
    q="Ice-cream sales and drownings rise together (correlation 0.9). Should we ban ice cream?", engine="decide", code="corr(ice_cream_sales, drownings) = 0.9", result="0.9",
    trap="Both go up in hot weather (a confounder). Correlation does not prove cause; you need an experiment or to control for temperature.", hint="What else happens in summer?",
    fix="Control for temperature or run an experiment before claiming cause and effect.", ask="Does ice cream cause drowning?", answer="off")

# ---------------------------------------------------------------- Power BI and Tableau (read the result and decide)
SALES_T = {"name": "Sales", "cols": ["Region", "Sales", "Profit"], "rows": [["North", 1000, 100], ["South", 4000, 200], ["East", 500, 150]]}
add(id="pbi-avg-ratio", seg="data", sec="Power BI", topic="DAX measures", level="Basic", title="Total profit margin", tagline="Average of ratios",
    q="What is the company's profit margin?", tables=[SALES_T], engine="decide", code="Margin = AVERAGEX(Sales, Sales[Profit] / Sales[Sales])", result="18.0%",
    trap="Averaging each region's margin (10%, 5%, 30%) gives 18%, but small East counts as much as big South. True margin = total profit / total sales = 450 / 5,500 = 8.2%.", hint="Add up profit and sales first.",
    fix="Margin = DIVIDE(SUM(Sales[Profit]), SUM(Sales[Sales]))   -- 8.2%", ask="Is 18% the company margin?", answer="off")
add(id="pbi-calc-col", seg="data", sec="Power BI", topic="DAX measures", level="Intermediate", title="Calculated column or measure?", tagline="Filter context",
    q="A calculated column Total = SUM(Sales[Sales]) is placed in a table by Region. What shows on each row?", tables=[SALES_T], engine="decide", code="Total (column) = SUM(Sales[Sales])", result="5,500 on every row",
    trap="A calculated column is computed once per row without the visual's filters, so SUM sees the whole table (5,500) on every row. Use a measure so each region shows its own total.", hint="Columns are calculated before you filter.",
    fix="Total Sales (measure) = SUM(Sales[Sales])", ask="Should every region show 5,500?", answer="off")
add(id="pbi-divide", seg="data", sec="Power BI", topic="DAX measures", level="Basic", title="Growth % with zero last year", tagline="Safe division",
    q="Growth % = (This year − Last year) / Last year. A new region had 0 last year.", engine="decide", code="Growth % = ([TY] - [LY]) / [LY]", result="Infinity / error",
    trap="Dividing by zero gives an error or infinity. DIVIDE() returns blank (or a value you choose) instead.", hint="What is 100 / 0?",
    fix="Growth % = DIVIDE([TY] - [LY], [LY])", ask="Is this measure safe?", answer="off")
add(id="pbi-time", seg="data", sec="Power BI", topic="Time intelligence", level="Advanced", title="Year-to-date that resets wrong", tagline="Date tables",
    q="TOTALYTD returns strange numbers and Sales by month repeats the same value.", engine="decide", code="Sales YTD = TOTALYTD(SUM(Sales[Sales]), Sales[OrderDate])", result="Wrong YTD",
    trap="Time intelligence needs a proper date table marked as a date table, with a relationship to Sales. Use 'Date'[Date], not the fact table's date column.", hint="Is there a Date table marked as a date table?",
    fix="Sales YTD = TOTALYTD(SUM(Sales[Sales]), 'Date'[Date])   -- with a marked Date table", ask="Is the measure set up correctly?", answer="off")
add(id="pbi-right", seg="data", sec="Power BI", topic="DAX measures", level="Intermediate", title="South share of total", tagline="ALL removes filters",
    q="Each region's share of total sales.", tables=[SALES_T], engine="decide", code="Share = DIVIDE(SUM(Sales[Sales]), CALCULATE(SUM(Sales[Sales]), ALL(Sales)))", result="South 72.7%",
    trap="This one is correct: ALL removes the Region filter for the denominator, so each region is divided by 5,500 (South 4,000 / 5,500 = 72.7%).", hint="Check 4,000 / 5,500.",
    fix="Share = DIVIDE(SUM(Sales[Sales]), CALCULATE(SUM(Sales[Sales]), ALL(Sales)))", ask="Is this measure right?", answer="right")
add(id="tab-margin", seg="data", sec="Tableau", topic="Calculations", level="Basic", title="Profit margin in Tableau", tagline="Row-level vs aggregate",
    q="Calculated field Margin = [Profit]/[Sales], shown as AVG(Margin) for the company.", tables=[SALES_T], engine="decide", code="Margin = [Profit] / [Sales]   →   AVG(Margin)", result="18.0%",
    trap="Same trap as Power BI: averaging row ratios. Use an aggregate calculation: SUM([Profit]) / SUM([Sales]) = 8.2%.", hint="Should East (500 sales) weigh as much as South (4,000)?",
    fix="Margin = SUM([Profit]) / SUM([Sales])", ask="Is 18% right?", answer="off")
add(id="tab-filter-lod", seg="data", sec="Tableau", topic="LOD & filters", level="Advanced", title="FIXED ignores my filter", tagline="Order of operations",
    q="{FIXED [Customer] : SUM([Sales])} does not change when I filter Region = South.", engine="decide", code="{FIXED [Customer] : SUM([Sales])}   with a Region filter", result="Unchanged",
    trap="FIXED LODs are computed before normal dimension filters. Right-click the Region filter → Add to Context so it applies first.", hint="Which runs first: the filter or FIXED?",
    fix="Add the Region filter to context (grey pill)", ask="Is the filter set up correctly?", answer="off")
add(id="tab-topn", seg="data", sec="Tableau", topic="LOD & filters", level="Intermediate", title="Top 5 products in the South", tagline="Context filters",
    q="A Top 5 filter by Sales plus a Region = South filter shows only 2 products.", engine="decide", code="Product: Top 5 by SUM(Sales)\nRegion: South", result="2 products",
    trap="Top N is calculated before the Region filter, so Tableau finds the national top 5 and then keeps those that are also in the South. Add Region to context.", hint="Order of operations again.",
    fix="Region filter → Add to Context, then Top 5", ask="Is this the South's top 5?", answer="off")
add(id="tab-date", seg="data", sec="Tableau", topic="Calculations", level="Basic", title="Monthly trend line", tagline="Discrete vs continuous",
    q="You want one line over time but get separate Jan–Dec points per year.", engine="decide", code="MONTH(Order Date) as a blue (discrete) pill", result="Jan–Dec headers",
    trap="Blue MONTH is discrete: it groups all Januaries together. Use the green (continuous) MONTH for a timeline.", hint="Blue makes headers; green makes axes.",
    fix="Right-click the date pill → choose the green Month (continuous)", ask="Is this a timeline?", answer="off")

# ---------------------------------------------------------------- AI PM (real interview scenarios)
def pm(id, level, topic, title, q, options, best, why):
    add(id=id, seg="pm", sec="AI PM", topic=topic, level=level, title=title, tagline=topic, q=q, engine="scenario", options=options, best=best, trap=why, hint="Think about the user, the goal metric and the risk.")
pm("pm-metric", "Basic", "Metrics", "Pick the right success metric", "You launched an AI 'smart reply' in a chat app. Which is the best primary success metric?",
   ["Number of AI suggestions shown", "Share of messages sent using a suggestion, with no drop in conversation length", "Model accuracy on a test set", "App store rating"], 1,
   "Suggestions shown is output, not value. Adoption of suggestions while conversations stay healthy measures real user value. Accuracy is a guardrail, not the goal.")
pm("pm-prioritise", "Basic", "Prioritisation", "Three requests, one sprint", "Sales wants a custom report for one big client, support wants a fix for a bug hitting 20% of users, and the CEO wants an AI chatbot demo. What do you do first?",
   ["CEO's chatbot demo", "The big client's report", "Fix the bug hitting 20% of users, then size the others with data", "Do all three halfway"], 2,
   "Widespread user pain usually wins: it protects retention and trust. Then compare the others by impact and effort (RICE) and agree the order with stakeholders.")
pm("pm-rca", "Intermediate", "Root cause analysis", "Orders dropped 15% yesterday", "Food-delivery orders fell 15% yesterday. What is your first step?",
   ["Blame the new design", "Check data and tracking issues, then segment by platform, city, app version and funnel step", "Launch a discount", "Wait a week"], 1,
   "First confirm the drop is real (tracking, outages), then segment to find where it happened before forming hypotheses. Fixes come after the cause.")
pm("pm-ai-build", "Intermediate", "AI product sense", "Should this be AI?", "A bank wants AI to approve personal loans automatically. What is the best first move?",
   ["Ship a fully automatic AI approver", "Start with AI that recommends and explains, a human approves, and fairness and regulation are reviewed", "Use a random number", "Let customers approve themselves"], 1,
   "High-stakes decisions need human review, explanations, bias testing and RBI compliance. Start with decision support and measure quality before automating more.")
pm("pm-eval", "Intermediate", "AI product sense", "Measuring an AI support bot", "How do you know your AI support assistant is good before launch?",
   ["Ask the model to grade itself only", "Build a test set of real questions with expected answers, measure accuracy, safety and escalation, then pilot with a hold-out group", "Count words in replies", "Ask the team if they like it"], 1,
   "AI features need evaluation sets and staged rollouts: offline tests for quality and safety, then an A/B or pilot measuring resolution, CSAT and escalations.")
pm("pm-guesstimate", "Intermediate", "Estimation", "Guesstimate: daily UPI payments at chai stalls", "How should you structure a guesstimate of daily UPI payments at chai stalls in Bengaluru?",
   ["Give a confident number immediately", "Break it into stalls × customers per stall × share paying by UPI, state assumptions and sanity-check", "Search online", "Refuse"], 1,
   "Interviewers score the structure: segment, state assumptions, calculate, then sanity-check the answer against something you know.")
pm("pm-tradeoff", "Advanced", "Strategy", "Growth vs trust", "An AI feature that auto-posts on users' social media would triple engagement but some users complain. What do you do?",
   ["Keep it on for everyone", "Make it opt-in with clear previews and easy undo, measure retention and complaints", "Hide the setting", "Remove the whole product"], 1,
   "Short-term engagement that erodes trust hurts long-term retention. Consent, transparency and control keep the gain while protecting users.")
pm("pm-north-star", "Advanced", "Metrics", "North Star for an edtech app", "Which is the best North Star metric for a learning app like SkillNavora?",
   ["Total sign-ups", "Weekly learners completing at least one lesson or practice test", "Page views", "Number of courses listed"], 1,
   "A North Star should capture delivered value and predict revenue: weekly active learners who complete learning, not vanity counts.")
pm("pm-stakeholder", "Advanced", "Stakeholders", "Engineering says your AI deadline is impossible", "Engineering says the AI feature date is impossible. Leadership already announced it. What do you do?",
   ["Push engineers to work weekends", "Understand the estimate, cut scope to a smaller valuable version, align leadership on the trade-off with options", "Miss the date silently", "Blame engineering"], 1,
   "Good PMs negotiate scope, not quality: find the smallest valuable release, show options with risks, and get explicit agreement.")
pm("pm-experiment", "Advanced", "Experiments", "A/B test shows +2% conversion", "Your A/B test shows +2% conversion after 2 days with p = 0.04. Ship it?",
   ["Ship immediately", "Wait for the planned sample size and a full weekly cycle, check guardrail metrics, then decide", "Stop the test", "Ignore the result"], 1,
   "Peeking early inflates false positives and misses weekday patterns. Run to the planned size, check guardrails (refunds, latency), then decide.")

# ---------------------------------------------------------------- GenAI (real-life scenarios)
def gen(id, level, topic, title, q, options, best, why):
    add(id=id, seg="genai", sec="GenAI", topic=topic, level=level, title=title, tagline=topic, q=q, engine="scenario", options=options, best=best, trap=why, hint="Think about context, examples, checking and safety.")
gen("g-prompt", "Basic", "Prompting", "Write a leave-request email", "Which prompt will give the best email asking your manager for 2 days' leave?",
    ["Write an email", "Write a short, polite email to my manager Priya asking for leave on 12–13 Nov for my sister's wedding. Mention I'll finish the report by the 11th. Under 100 words.", "Email leave", "Make it good"], 1,
    "Good prompts give the task, context, details and format. The more specific you are, the less you need to fix.")
gen("g-hallucination", "Basic", "Safety", "The AI gave a fake reference", "An AI tool gave you a research paper link that doesn't exist. What happened and what should you do?",
    ["It's always right, use it", "It hallucinated: AI can make up facts. Ask for sources, check them yourself, or use a tool that searches real documents", "The internet is broken", "Delete the AI"], 1,
    "LLMs predict likely text and can invent facts. Always verify facts, numbers and links, especially for school, work or money.")
gen("g-privacy", "Basic", "Safety", "Sharing customer data", "You want AI to summarise a spreadsheet of customers' phone numbers and addresses. What's safest?",
    ["Paste everything into any free chatbot", "Remove personal details or use your company's approved AI tool with data protection", "Post it online", "Email it to friends"], 1,
    "Personal data needs protection (India's DPDP Act). Remove or mask it, and use approved tools with clear data policies.")
gen("g-few-shot", "Intermediate", "Prompting", "Classify customer reviews", "You want AI to label reviews as Happy, Neutral or Angry in the same style every time. Best approach?",
    ["Ask once and hope", "Give 3 labelled examples in the prompt and ask for one word as output", "Ask it to be creative", "Use longer reviews"], 1,
    "Few-shot examples show the exact format and labels you want, which makes results consistent.")
gen("g-rag", "Intermediate", "RAG", "Chatbot for your school's rules", "You want a chatbot that answers questions using your school's rulebook. What's the right method?",
    ["Hope the AI already knows it", "Give the AI the rulebook (RAG): search the right pages and answer only from them, with page references", "Train a new AI from scratch", "Ask students to guess"], 1,
    "RAG retrieves the relevant parts of your documents and asks the AI to answer from them, with sources, so answers are accurate and up to date.")
gen("g-agent", "Intermediate", "Agents", "Automate weekly reports", "Every Monday you copy numbers from Google Sheets, write a summary and post it in Slack. How can AI help?",
    ["Do it by hand forever", "Build an automation (n8n/Make/Zapier) that reads the sheet, asks Claude for a summary in your format, and posts to Slack for your review", "Ask AI to guess the numbers", "Stop reporting"], 1,
    "Automations connect apps; the AI step writes the summary from real data. Keep a human check before posting.")
gen("g-mcp", "Advanced", "Agents", "Let Claude use your tools", "You want Claude to read your Google Drive and create Jira tickets. What do you use?",
    ["Copy-paste everything", "Connect Drive and Jira through MCP connectors with the least access needed, and approve actions", "Give Claude your password", "Screenshots"], 1,
    "MCP connectors let AI use tools safely with permissions. Approve actions that create or change things.")
gen("g-cost", "Advanced", "Building apps", "Your AI app is too expensive", "Your AI chatbot costs too much each month. What helps most without hurting quality?",
    ["Use the biggest model for everything", "Send simple questions to a smaller model, cache the long system prompt, and keep answers short", "Turn off the app", "Add more text to every prompt"], 1,
    "Model routing, prompt caching and shorter outputs cut cost a lot while keeping quality for hard questions.")

ASSIGN = {
    "SQL": [("SQLBolt interactive lessons", "https://sqlbolt.com/"), ("W3Schools SQL exercises", "https://www.w3schools.com/sql/sql_exercises.asp"), ("LeetCode SQL 50", "https://leetcode.com/studyplan/top-sql-50/"), ("HackerRank SQL", "https://www.hackerrank.com/domains/sql"), ("DataLemur SQL questions", "https://datalemur.com/questions"), ("ChaturIQ SQL traps", "https://chaturiq.com/")],
    "Excel": [("W3Schools Excel exercises", "https://www.w3schools.com/excel/excel_exercises.php"), ("Excel Practice Online", "https://excel-practice-online.com/"), ("Chandoo Excel School (free lessons)", "https://chandoo.org/wp/excel-school/"), ("Microsoft Excel training", "https://support.microsoft.com/excel")],
    "Python": [("W3Schools Python exercises", "https://www.w3schools.com/python/python_exercises.asp"), ("Kaggle Learn: Python and Pandas", "https://www.kaggle.com/learn"), ("HackerRank Python", "https://www.hackerrank.com/domains/python"), ("Exercism Python track", "https://exercism.org/tracks/python")],
    "ML": [("Kaggle Learn: Intro to Machine Learning", "https://www.kaggle.com/learn/intro-to-machine-learning"), ("Kaggle Titanic competition", "https://www.kaggle.com/competitions/titanic"), ("Google ML Crash Course", "https://developers.google.com/machine-learning/crash-course")],
    "Power BI": [("Microsoft Learn: PL-300 path", "https://learn.microsoft.com/en-us/training/career-paths/data-analyst"), ("Power BI sample datasets", "https://learn.microsoft.com/en-us/power-bi/create-reports/sample-datasets"), ("DAX Guide", "https://dax.guide/")],
    "Tableau": [("Makeover Monday weekly challenge", "https://makeovermonday.co.uk/"), ("Workout Wednesday", "https://workout-wednesday.com/"), ("Tableau free training", "https://www.tableau.com/learn/training")],
    "AI PM": [("NextLeap PM question bank", "https://nextleap.app/interview-preparation/product-management/questions"), ("HelloPM interview guide", "https://hellopm.co/resources-for-product-management-interview/"), ("Exponent PM questions", "https://www.tryexponent.com/questions")],
    "GenAI": [("Anthropic prompt engineering tutorial", "https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview"), ("DeepLearning.AI short courses", "https://www.deeplearning.ai/short-courses/"), ("Google Prompting essentials", "https://ai.google.dev/gemini-api/docs/prompting-strategies")],
}
