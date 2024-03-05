import os
import joblib
pred=joblib.load("saved_models\model.joblib")

predict=pred.predict()
print(predict)

