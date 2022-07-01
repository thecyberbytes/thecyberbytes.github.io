import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def generate_news_html():
    # read the news feed
    news_df = pd.read_excel("cyber_web/excels/Book2.xlsx")#/content/news_articles.xlsx")
    news_df.dropna(axis=0, inplace=True)
    # clean the new line character
    news_df['Title'] = news_df['Title'].apply(lambda x: x.replace('\n',""))
    # clean the quotes
    news_df['Title'] = news_df['Title'].apply(lambda x: x.replace("\'","\\'"))
    news_df['Title'] = news_df['Title'].apply(lambda x: x.replace('\"','\\"'))
    
    # one news per category df
    trending_df = news_df.groupby(['Category']).first()
    
    start_card_index = 0
    carousel_cards_count = 4
    col_1_cards_count = 2
    col_2_cards_count = 3
    col_3_cards_count = 3
    trending_cards_count = 6    # one per category
    total_news = 52
    total_section = 6
    
    # start - 0 and end - 4
    end_card_index = start_card_index + carousel_cards_count
    generate_carousel(news_df, start_card_index, end_card_index)

    # news total 52 (4 in carousel and 48 in 6 sections of 2 news in first col, 3 news in col 2 and col 3 and 6 news in trending)
    for i in range(start_card_index, total_section):
      # generate first column
      file_name = "cyber_web/js/"+"gen_card_col_1"+str(i)+".js"
      start_card_index = end_card_index
      end_card_index = end_card_index + col_1_cards_count
      generate_card_col_1(news_df, start_card_index, end_card_index, file_name)

      # generate second column
      file_name = "cyber_web/js/"+"gen_card_col_2"+str(i)+".js"
      start_card_index = end_card_index
      end_card_index = start_card_index + col_2_cards_count
      generate_card_col_2_and_3(news_df, start_card_index, end_card_index, file_name)

      # generate third column
      file_name = "cyber_web/js/"+"gen_card_col_3"+str(i)+".js"
      start_card_index = end_card_index
      end_card_index = start_card_index + col_3_cards_count
      generate_card_col_2_and_3(news_df, start_card_index, end_card_index, file_name)
        
      # generate trending nres section
      # start - 0 and end - 6
      generate_card_trending(trending_df, start_card_index, trending_cards_count)
    
def write_file(file, data):
  # Writing to file
  print(f"Writing data to file...{file}")
  # Writing to file
  with open(file, "w") as card_file:
    # Writing data to a file
    card_file.writelines(data)
  card_file.close()

def read_file(file, data):
  # Reading from file
  print(f"Reading data to file...{file}")
  with open(file, "r+") as card_file:
      # Reading from a file
      print(card_file.read())
  card_file.close()

def generate_carousel(df, start, end):
  lines = []
  lines.append("document.write(' \\\n")

  for i in range(start, end):
      print(i)
      item_status = ""
      if i == 0:
        item_status = "active"

      lines.append('<div class="carousel-item ' + item_status + '"> \\\n')
      lines.append('<a href="' + df['URL'][i] + '" target="_blank"> \\\n')
      lines.append('<img src="' + df['Image'][i] + '" alt="" class="d-block w-100" style="height:50vh;filter: brightness(50%);"> \\\n')
      lines.append('<div class="carousel-caption"> \\\n')
      lines.append('<h2>' + df['Title'][i] + '</h2> \\\n')
      lines.append('<p class="text-uppercase font-weight-bold" style="letter-spacing: 0.07rem;font-family:serif;font-size:12px">' + df['Date Created'][i] + '</p> \\\n')
      lines.append('</div> \\\n')
      lines.append('</a> \\\n')
      lines.append('</div> \\\n')

  lines.append("');")
    
  file_name = "cyber_web/js/"+"gen_card_carousel.js"
  write_file(file_name, lines)

  return

def generate_card_col_1(df, start, end, file_name):
    lines = []
    lines.append("document.write(' \\\n")
    lines.append('<div class="container-fluid border border-dark border-0 p-0 m-0 align-items-center justify-content-between"> \\\n')
    
    for i in range(start, end):
      print(i)
      lines.append('<div> \\\n')
      lines.append('<div class="card mb-5 border-0 rounded zoom" style="background: #fafafa;"> \\\n')
      lines.append('<a href="' + df['URL'][i] + '" target="_blank" style="text-decoration:none"> \\\n')
      lines.append('<img src="' + df['Image'][i] + '" class="card-img-top img-fluid" alt="..."> \\\n')
      lines.append('<div class="card-body p-0 mx-0 my-3" style="letter-spacing: 0.07rem;font-family:serif;color:#ADADAD;font-size:12px"> \\\n')
      lines.append('<small class="text-uppercase font-weight-bold"><span>' + df['Category'][i] + '</span> <span class="mx-1">&bullet;</span> <span>' + df['Date Created'][i] + '</span></small> \\\n')
      lines.append('<h2 class="card-link text-dark font-weight-bold my-3">' + df['Title'][i] + '</h2> \\\n')
      lines.append('</div> \\\n')
      lines.append('</a> \\\n')
      lines.append('</div> \\\n')
      lines.append('</div> \\\n')
    
    lines.append('</div> \\\n')
    lines.append("');")
    
    write_file(file_name, lines)

    return

def generate_card_col_2_and_3(df, start, end, file_name):
    lines = []
    lines.append("document.write(' \\\n")
    
    for i in range(start, end):
      print(i)
      lines.append('<div class="card mb-5 border-0 rounded zoom" style="background: #fafafa;"> \\\n')
      lines.append('<a href="' + df['URL'][i] + '" target="_blank" style="text-decoration:none"> \\\n')
      lines.append('<img src="' + df['Image'][i] + '" class="card-img-top img-fluid" alt="..."> \\\n')
      lines.append('<div class="card-body p-0 mx-0 my-3" style="letter-spacing: 0.07rem;font-family:serif;color:#ADADAD;;font-size:12px"> \\\n')
      lines.append('<small class="text-uppercase font-weight-bold"><span>' + df['Category'][i] + '</span> <span class="mx-1">&bullet;</span> <span>' + df['Date Created'][i] + '</span></small> \\\n')
      lines.append('<h5 class="card-link text-dark font-weight-bold my-3">' + df['Title'][i] + '</h5> \\\n')
      lines.append('</div> \\\n')
      lines.append('</a> \\\n')
      lines.append('</div> \\\n')

    lines.append("');")
    
    write_file(file_name, lines)

    return

def generate_card_trending(df, start, end):
  lines = []
  lines.append("document.write(' \\\n")

  for i in range(start, end):
      print(i)
      lines.append('<li class="list-group-item" style="background: #fafafa;"> \\\n')
      lines.append('<a href="' + df['URL'][i] + '" target="_blank" style="text-decoration:none"> \\\n')
      lines.append('<div class="card-body p-0 mx-0 my-3" style="letter-spacing: 0.07rem;font-family:serif;color:#ADADAD;;font-size:10px"> \\\n')
      lines.append('<h6 class="card-link text-dark font-weight-bold my-3">' + df['Title'][i] + '</h6> \\\n')
      lines.append('</div> \\\n')
      lines.append('</a> \\\n')
      lines.append('</li> \\\n')
      
  lines.append("');")
    
  file_name = "cyber_web/js/"+"gen_card_trending.js"
  write_file(file_name, lines)

  return
    
def categorize_news():
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
    
def main():
    categorize_news()
    generate_news_html()
        
if __name__ == "__main__":
    main()
