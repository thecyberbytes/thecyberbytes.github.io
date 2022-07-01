import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def main():
    filename = 'cyber_web/models/trained_model.pkl'  # the trained model
    tdidf_filename = 'cyber_web/models/trained_tfidf.pkl'  # the trained TD-IDF vector
    cat_filename = 'cyber_web/models/category_dict.pkl'  # the news category dict
    
    # load the model
    loaded_model = pickle.load(open(filename, 'rb'))

    # load the tfidf
    loaded_tfidf = pickle.load(open(tdidf_filename, "rb" ) )

    # load the categories
    loaded_category_to_id = pickle.load(open(cat_filename, "rb" ) )

    # load the test data
    news_test_df = pd.read_excel("cyber_web/excels/Book3.xlsx")

    # perform TFIDF 
    news_test_df_tfidf = loaded_tfidf.transform(news_test_df['Title'].str.lower())

    y_pred_cat = loaded_model.predict(news_test_df_tfidf)
    y_pred_cat_name = []
    for cat_pred, cat_pred_val in enumerate(y_pred_cat):
      y_pred_cat_name.append([cat for cat, cat_id in loaded_category_to_id.items() if cat_id == cat_pred_val][0])

    #submit_test = ["Correct" if y_test.to_list()[i] == y_pred[i] else "X" for i in range(len(y_pred)) ]
    submit_test = pd.concat([news_test_df['Title'], pd.DataFrame(y_pred_cat_name)], axis=1)
    submit_test.columns=['Title', 'Category']
    submit_test.to_excel("cyber_web/excels/news_categorized.xlsx", index=False)

if __name__ == "__main__":
    main()
