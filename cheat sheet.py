 # This code is not meant to be perfect, or
# even good at all. It does work.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

xa = np.random.normal(2, 1, 100)
xb = np.random.normal(3, 1, 100)
xc = xa + xb
df = pd.DataFrame({
    'xa': xa,
    'xb': xb,
    'xc': xc,
    'intercept': 1
})
df_melt = pd.melt(df[['xa', 'xb', 'xc']])

from scipy import stats
from statsmodels.stats import multicomp
import statsmodels.api as sm

print(stats.ttest_ind(xa, xb).pvalue)
print(stats.normaltest(xa).pvalue)
print(stats.levene(xa, xb).pvalue)
print(stats.mannwhitneyu(xa, xb,
      alternative='two-sided').pvalue)

print(stats.f_oneway(xa, xb, xc).pvalue)
tukey = multicomp.pairwise_tukeyhsd(
    df_melt['value'], df_melt['variable'],
    alpha=0.05)
print(tukey)

contin = pd.crosstab(df['xa'], df['xb'])
chi2 = stats.chi2_contingency(contin)
print(chi2.pvalue)

reg = stats.linregress(xc, xa)
print(reg.slope, reg.intercept)
print(reg.pvalue, reg.rvalue)
results = sm.OLS(
    df['xc'],
    df[['xa', 'xb', 'intercept']]
).fit()
print(results.summary())

from sklearn.model_selection import \
    train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import \
    MinMaxScaler, StandardScaler, \
    FunctionTransformer
from sklearn.decomposition import PCA
from sklearn.linear_model import \
    LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import \
    KNeighborsClassifier
from sklearn.tree import \
    DecisionTreeClassifier
from sklearn.ensemble import \
    RandomForestClassifier
from sklearn.neural_network import MLPClassifier

X = np.stack([xa, xb, xc], axis=1)
y = (xa + xb + xc) // 3
X_train, X_valid, y_train, y_valid \
    = train_test_split(X, y)

model = LinearRegression(
    fit_intercept=True)
model = GaussianNB()
model = make_pipeline(
    StandardScaler(),
    PCA(2),
    KNeighborsClassifier(5) )
model = DecisionTreeClassifier(max_depth=4)
model = RandomForestClassifier(n_estimators=20,
        max_depth=3, min_samples_leaf=10)
model = MLPClassifier(hidden_layer_sizes=(4, 3))

model.fit(X_train, y_train)
print(model.predict(X_valid))
print(model.score(X_valid, y_valid))

from sklearn.cluster import KMeans
model = KMeans(n_clusters=5)
y = model.fit_predict(X)
print(model.predict(X))

from sklearn.neighbors import \
    KNeighborsRegressor
from sklearn.ensemble import \
    RandomForestRegressor
from sklearn.neural_network import MLPRegressor

model = KNeighborsRegressor(5)
model = RandomForestRegressor(100, max_depth=5)
model = MLPRegressor(hidden_layer_sizes=(8, 6),
    activation='logistic')
                     
model.fit(X_train, y_train)
print(model.score(X_valid, y_valid))