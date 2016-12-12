from sklearn.ensemble import RandomForestClassifier

classifier = RandomForestClassifier()
hyper_param_grid = {'n_estimators': [1,10,100,1000,10000], 'max_depth': [1,5,10,20,50,100], 'max_features': ['sqrt','log2'],'min_samples_split': [2,5,10]},

from sklearn.grid_search import GridSearchCV

grid_search = GridSearchCV(classifier, hyper_param_grid, cv = 5, verbose = 3)

grid_search.fit(X, y)

grid_search.best_params_

grid_search.best_score_

## Para eviatr overfit
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)

grid_search = GridSearch(classifier, hyper_param_grid, cv=5)
grid_search.fit(X_train, y_train)

grid_search.predict(X_test)

grid_search.score(X_test, y_test)

## O puedes usar de nuevo cv
cross_val_score(grid_search, X, y, cv = 5)