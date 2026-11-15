"""ML class guide data: what each live class covered and where every topic is taught.

HOW TO ADD A NEW CLASS (the only file you need to edit):
1. Append a dict to CLASSES with n, title, summary and topics.
2. Each topic is (topic name, [references]). A reference is
     "ml:N"          -> lesson N of the Statistics & ML track in the Data Science & AI handbook
     "py:N", "de:N", "gov:N" -> lesson N of the Python, Data Engineering or Governance track
     "guide:<slug>"  -> a companion lesson in tools/mlguide/guide_lessons.py
   A topic with no reference is shown as a GAP, so new gaps are visible straight away.
3. Run: python3 tools/gen_site.py   (and capture.py first if you added companion code).
"""

CLASSES = [
 {"n": 1, "title": "Statistics refresher and hypothesis testing",
  "summary": "Hypothesis testing, the Central Limit Theorem, parametric and non-parametric tests, and the introduction to the hypothesis-testing case study.",
  "topics": [
   ("Descriptive vs inferential statistics; population and sample", ["ml:1", "ml:3"]),
   ("Mean, median, mode, variance, standard deviation, IQR, percentiles", ["ml:1"]),
   ("Symmetric and skewed distributions, kurtosis", ["ml:1", "ml:2"]),
   ("Standardisation (z-scores) to compare variables", ["ml:1", "ml:9"]),
   ("Central Limit Theorem (sample means look normal from about n = 30)", ["ml:3"]),
   ("Parametric vs non-parametric tests and when to use each", ["ml:5"]),
   ("Z-test vs t-test (known vs unknown population SD, sample size)", ["ml:4"]),
   ("One-sample, paired (before/after) and independent two-sample tests", ["ml:4", "guide:hypothesis-case-study"]),
   ("Chi-square for two categorical variables; ANOVA for three or more groups", ["ml:5", "guide:hypothesis-case-study"]),
   ("Hypothesis-testing case study set-up (SciPy, NumPy, pandas)", ["guide:hypothesis-case-study"]),
  ]},
 {"n": 2, "title": "Running the tests: p-value, alpha and critical values",
  "summary": "Tests implemented on the case study; p-value, alpha, critical value, one-tailed and two-tailed tests.",
  "topics": [
   ("Null and alternative hypotheses", ["ml:4"]),
   ("Confidence level and alpha (alpha = 1 - confidence)", ["ml:3", "ml:4"]),
   ("p-value and the decision rule (p < alpha: reject H0)", ["ml:4"]),
   ("Six-step testing procedure; test statistic vs critical value (z = 1.96 at 95%)", ["ml:4", "guide:hypothesis-case-study"]),
   ("Standard error vs standard deviation", ["ml:3"]),
   ("One-tailed vs two-tailed tests", ["ml:4", "guide:hypothesis-case-study"]),
   ("One-sample t-test and paired t-test in Python (ttest_1samp, ttest_rel)", ["ml:4", "guide:hypothesis-case-study"]),
   ("Reading z, t and chi-square tables", ["ml:4", "ml:5", "guide:hypothesis-case-study"]),
  ]},
 {"n": 3, "title": "Hypothesis testing concluded; introduction to machine learning",
  "summary": "Case study concluded; introduction to ML, types of business problems, converting a business problem to a statistics problem, types of ML systems.",
  "topics": [
   ("Independent t-test, ANOVA (f_oneway), chi-square (chi2_contingency) on the case", ["ml:5", "guide:hypothesis-case-study"]),
   ("Expected vs observed tables and degrees of freedom", ["ml:5", "guide:hypothesis-case-study"]),
   ("Pearson and Spearman rank correlation", ["ml:1", "ml:5", "guide:hypothesis-case-study"]),
   ("What machine learning is; ML vs AI vs deep learning vs GenAI", ["ml:7", "ml:26"]),
   ("Business problem types: regression, classification, segmentation, forecasting", ["ml:7"]),
   ("Converting a business problem into a statistics problem (Y, X, unit, metric)", ["ml:7", "gov:1"]),
   ("Supervised and unsupervised learning systems", ["ml:7"]),
   ("Semi-supervised learning (a few labelled rows plus many unlabelled)", ["guide:semi-supervised"]),
  ]},
 {"n": 4, "title": "Project lifecycles and types of models",
  "summary": "Life cycle of analytics and machine-learning projects, linear and non-linear models, the linear equation and link functions.",
  "topics": [
   ("Lifecycle of an analytics (dashboard) project: brief, audit, cleaning, Power BI, views, validation, access, support", ["guide:analytics-lifecycle"]),
   ("Lifecycle of an ML project: business problem to retraining (12 steps)", ["ml:7", "ml:27", "guide:analytics-lifecycle"]),
   ("Data audit and cleaning plan", ["guide:analytics-lifecycle", "py:17"]),
   ("Dependent (Y) and independent (X) variables", ["ml:7", "ml:10"]),
   ("Linear vs non-linear models; slope, intercept and the linear equation", ["ml:7", "ml:10"]),
   ("Link functions (identity, sigmoid, exp)", ["ml:7", "ml:13"]),
   ("Train/test split (80:20) and evaluation gaps", ["ml:8"]),
  ]},
 {"n": 5, "title": "Gradient descent for linear regression",
  "summary": "Gradient Descent implemented for Linear Regression in Python.",
  "topics": [
   ("Loss functions for regression: error, SSE, MSE, RMSE", ["ml:11", "ml:30"]),
   ("OLS summary (statsmodels): R2, adjusted R2, coefficients, p-values", ["ml:10"]),
   ("Gradient descent: derivatives, learning rate, iterations", ["ml:11"]),
   ("Gradient descent from scratch matching the OLS answer", ["ml:11"]),
  ]},
 {"n": 6, "title": "Preprocessing, overfitting and heuristic segmentation",
  "summary": "Missing value imputation, outlier treatment, categorical encoding, overfitting and underfitting, introduction to segmentation, heuristic and RFM segmentation.",
  "topics": [
   ("Scaling: StandardScaler, MinMaxScaler, RobustScaler", ["ml:9"]),
   ("Nominal vs ordinal data; one-hot, ordinal and label encoding", ["ml:9", "guide:car-sales-regression"]),
   ("Missing-value imputation: SimpleImputer, KNNImputer, model-based", ["ml:9", "guide:car-sales-regression"]),
   ("Outlier capping: IQR, mean +/- 3 SD, percentile", ["ml:9", "guide:car-sales-regression"]),
   ("Overfitting vs underfitting from train and test RMSE; bias and variance", ["ml:12", "guide:car-sales-regression"]),
   ("Heuristic segmentation: demographic, loyalty, life stage, value", ["guide:customer-360"]),
   ("RFM segmentation with percentile rules (Gold, Silver, Bronze)", ["ml:22", "guide:customer-360"]),
  ]},
 {"n": 7, "title": "K-nearest neighbours, GridSearchCV and classification metrics",
  "summary": "KNNClassifier and KNNRegressor, GridSearchCV, implementation on the bank-loans case study, evaluation metrics for classification.",
  "topics": [
   ("KNN classifier and regressor: distance, k, majority vs distance weights", ["ml:16"]),
   ("Why distance-based models need standardised X", ["ml:9", "ml:16"]),
   ("GridSearchCV and k-fold cross-validation", ["ml:15", "ml:16"]),
   ("Bank-loans case study in Python", ["ml:16"]),
   ("Classification metrics: confusion matrix, accuracy, precision, recall, F1, ROC-AUC", ["ml:14"]),
   ("Credit-risk evaluation: gains table, lift, KS, Gini", ["guide:iv-woe-ks"]),
  ]},
 {"n": 8, "title": "Analytics file creation",
  "summary": "Analytics file creation; Customer 360 case study started.",
  "topics": [
   ("What an analytics file is, why it matters, where it is used", ["guide:customer-360"]),
   ("Deciding Y from the business problem (forecast, churn, high spender, segments)", ["ml:7", "guide:customer-360"]),
   ("Source tables: customers, products, transactions", ["guide:customer-360", "py:18"]),
  ]},
 {"n": 9, "title": "Customer 360 and the end-to-end linear regression case",
  "summary": "Customer 360 file creation completed; end-to-end linear regression case study (car sales) introduced and solved.",
  "topics": [
   ("Customer 360 variables: baskets, value, margin, discount, category penetration, flags, deciles", ["guide:customer-360"]),
   ("Period-based segments: new, churner, upward and downward migrator; churn and high-spender targets", ["guide:customer-360"]),
   ("End-to-end regression case: car sales drivers", ["guide:car-sales-regression", "ml:10"]),
   ("Dummy variables with n - 1 columns (drop_first)", ["ml:9", "guide:car-sales-regression"]),
  ]},
 {"n": 10, "title": "Feature selection, imputers and Naive Bayes",
  "summary": "Feature selection techniques (VIF), SimpleImputer and KNNImputer, introduction to the Naive Bayes classifier.",
  "topics": [
   ("Feature selection: correlation, RFE, SelectKBest, tree importance", ["ml:9", "ml:18"]),
   ("Multicollinearity and VIF = 1 / (1 - R2); drop above 5", ["ml:10", "guide:car-sales-regression"]),
   ("Information Value and WOE for variable screening", ["guide:iv-woe-ks"]),
   ("SimpleImputer vs KNNImputer (distance with missing columns)", ["ml:9", "guide:car-sales-regression"]),
   ("Naive Bayes: conditional probability, Bayes' rule, GaussianNB, CategoricalNB, BernoulliNB", ["ml:2", "ml:20"]),
  ]},
]

# What a complete "Machine Learning using Python" course should also include, mapped to lessons.
# Used for the completeness checklist on the guide page.
COMPLETENESS = [
 ("Probability and distributions, Bayes' rule", ["ml:2"]),
 ("A/B testing, statistical power and sample size", ["ml:6"]),
 ("scikit-learn pipelines and saving models", ["ml:8"]),
 ("Regularisation: Ridge, Lasso, Elastic Net", ["ml:12"]),
 ("Logistic regression and odds ratios", ["ml:13"]),
 ("Decision trees", ["ml:17"]),
 ("Random forests and bagging", ["ml:18"]),
 ("Gradient boosting: XGBoost, LightGBM, CatBoost", ["ml:19"]),
 ("Support vector machines", ["ml:20"]),
 ("Imbalanced classes: class weights, resampling, thresholds", ["ml:21"]),
 ("K-means clustering", ["ml:22"]),
 ("Hierarchical clustering, DBSCAN, PCA, t-SNE", ["ml:23"]),
 ("Time-series forecasting: ETS, ARIMA, lag features", ["ml:24"]),
 ("Text analytics and NLP", ["ml:25"]),
 ("Neural networks and deep learning", ["ml:26"]),
 ("Explainability (SHAP), fairness, deployment and monitoring", ["ml:27"]),
 ("Recommendation systems", ["ml:29"]),
 ("Regression metrics: MAE, MSE, RMSE, R2, MAPE", ["ml:30"]),
 ("End-to-end capstone (churn prediction)", ["ml:28"]),
 ("Semi-supervised learning", ["guide:semi-supervised"]),
 ("Analytics file / Customer 360", ["guide:customer-360"]),
 ("WOE, IV, KS and Gini (credit risk)", ["guide:iv-woe-ks"]),
 ("Deployment basics: Streamlit, FastAPI, Docker", ["ai:fastapi-docker"]),
 ("SQL for building analytics files", ["py:23", "track:sql"]),
]

RESOURCES = [
 ("scikit-learn User Guide (official)", "https://scikit-learn.org/stable/user_guide.html", "Every algorithm in the course, with examples."),
 ("SciPy statistical functions (official)", "https://docs.scipy.org/doc/scipy/reference/stats.html", "ttest_1samp, ttest_rel, ttest_ind, f_oneway, chi2_contingency and more."),
 ("statsmodels documentation (official)", "https://www.statsmodels.org/stable/index.html", "OLS summaries, VIF, GLMs and time series."),
 ("pandas User Guide (official)", "https://pandas.pydata.org/docs/user_guide/index.html", "Building analytics files: groupby, pivot_table, merge, dates."),
 ("An Introduction to Statistical Learning, with Python (free book)", "https://www.statlearning.com/", "The standard free textbook for this syllabus."),
 ("Google Machine Learning Crash Course (free)", "https://developers.google.com/machine-learning/crash-course", "Short lessons on loss, gradient descent, generalisation and classification metrics."),
 ("OpenIntro Statistics (free book)", "https://www.openintro.org/book/os/", "Hypothesis testing, CLT and inference explained simply."),
 ("Kaggle Learn: Intermediate Machine Learning (free)", "https://www.kaggle.com/learn/intermediate-machine-learning", "Missing values, categorical variables, pipelines, cross-validation."),
 ("Kaggle datasets", "https://www.kaggle.com/datasets", "Practice data for the weekly regression and KNN assignments."),
]
