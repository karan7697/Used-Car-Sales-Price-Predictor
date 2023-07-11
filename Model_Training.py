import pandas as pd
import sqlite3
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import pickle

con = sqlite3.connect('carsDB1.db')
cars = pd.read_sql('select * from Cars_selected',con)

X = cars.drop(['price'],axis=1)
y = cars['price']


X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    train_size=0.7,
                                                    test_size = 0.3,random_state=42)

regressor=DecisionTreeRegressor()
regressor.fit(X_train.values, y_train)

accuracy_score_dt = regressor.score(X_test.values,y_test)
# print(accuracy_score_dt)
# Saving model to disk
pickle.dump(regressor, open('model_2.pkl','wb'))
