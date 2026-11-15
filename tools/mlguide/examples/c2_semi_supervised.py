"""Semi-supervised learning: train with a few labelled loans plus many unlabelled ones.
Mirrors the class example: some applications have a known outcome (Y), the rest do not.
Run: python c2_semi_supervised.py"""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.semi_supervised import LabelSpreading, SelfTrainingClassifier

X, y = make_classification(n_samples=2000, n_features=8, n_informative=5, n_redundant=1, n_clusters_per_class=1,
                           class_sep=0.8, flip_y=0.03, random_state=11)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=11, stratify=y)
scaler = StandardScaler().fit(X_train)
X_train, X_test = scaler.transform(X_train), scaler.transform(X_test)

rng = np.random.default_rng(3)
print(f"Training pool: {len(y_train)} applications | test set: {len(y_test)} (always labelled, never used to train)\n")
print(f"{'labelled':>9} {'unlabelled':>11} | {'supervised only':>15} | {'self-training':>13} | {'label spreading':>15}")
for n_lab in [10, 20, 50, 500]:
    accs = {"sup": [], "self": [], "spread": []}
    for seed in range(5):                                  # repeat to average out luck
        idx = np.random.default_rng(seed).choice(len(y_train), n_lab, replace=False)
        if len(set(y_train[idx])) < 2:                     # need both classes to train
            continue
        y_partial = np.full(len(y_train), -1)              # -1 means "no label" in scikit-learn
        y_partial[idx] = y_train[idx]

        sup = LogisticRegression().fit(X_train[idx], y_train[idx])
        accs["sup"].append(accuracy_score(y_test, sup.predict(X_test)))

        st = SelfTrainingClassifier(LogisticRegression(), threshold=0.9).fit(X_train, y_partial)
        accs["self"].append(accuracy_score(y_test, st.predict(X_test)))

        ls = LabelSpreading(kernel="knn", n_neighbors=10).fit(X_train, y_partial)
        accs["spread"].append(accuracy_score(y_test, ls.predict(X_test)))
    print(f"{n_lab:>9} {len(y_train) - n_lab:>11} | {np.mean(accs['sup']):>15.3f} | {np.mean(accs['self']):>13.3f} | {np.mean(accs['spread']):>15.3f}")

# What self-training did, step by step, for one run with 20 labels
idx = np.random.default_rng(0).choice(len(y_train), 20, replace=False)
y_partial = np.full(len(y_train), -1); y_partial[idx] = y_train[idx]
st = SelfTrainingClassifier(LogisticRegression(), threshold=0.9).fit(X_train, y_partial)
added = st.labeled_iter_
print(f"\nOne run with 20 labels: {int((added > 0).sum())} pseudo-labels added over {st.n_iter_} rounds; "
      f"{int((added == -1).sum())} rows stayed unlabelled (model never 90% sure).")
pseudo = added > 0
print(f"Pseudo-label accuracy against the hidden truth: {accuracy_score(y_train[pseudo], st.transduction_[pseudo]):.3f}")
