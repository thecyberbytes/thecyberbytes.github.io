import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import feed_file_generator as gen_feed
from datetime import datetime

#filter the warning messages
import warnings
warnings.filterwarnings('ignore')

def generate_news_html(cat_news_filename, blog_file_name, blog_df, news_df):
    # read the news feed
    if news_df.shape[0] == 0:
        print("reading the categorized news file as dataframe is empty")
        news_df = pd.read_excel(cat_news_filename)
    
    # drop empty rows
    news_df.dropna(axis=0, inplace=True)
    # clean the new line character
    news_df['Date Created'] = news_df['Date Created'].apply(lambda x: x.replace('\n',""))
    news_df['Date Created'] = news_df['Date Created'].apply(lambda x: x.strip())
    news_df['Title'] = news_df['Title'].apply(lambda x: x.replace('\n',""))
    news_df['Title'] = news_df['Title'].apply(lambda x: x.strip())
    news_df['URL'] = news_df['URL'].apply(lambda x: x.replace('\n',""))
    news_df['Image'] = news_df['Image'].apply(lambda x: x.replace('\n',""))
    news_df['URL'] = news_df['URL'].apply(lambda x: x.strip())
    news_df['Image'] = news_df['Image'].apply(lambda x: x.strip())
    # clean the quotes
    news_df['Title'] = news_df['Title'].apply(lambda x: x.replace("\'","\\'"))
    news_df['Title'] = news_df['Title'].apply(lambda x: x.replace('\"','\\"'))
    news_df['URL'] = news_df['URL'].apply(lambda x: x.replace("\'","\\'"))
    news_df['URL'] = news_df['URL'].apply(lambda x: x.replace('\"','\\"'))
    news_df['Image'] = news_df['Image'].apply(lambda x: x.replace("\'","\\'"))
    news_df['Image'] = news_df['Image'].apply(lambda x: x.replace('\"','\\"'))
    
    print("Generating htmls")
    print(news_df.head())
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
    
    # generate category cards
    generate_single_category('Data Breach', news_df)
    generate_single_category('Cyber Knowledge', news_df)
    generate_single_category('Ransomware', news_df)
    generate_single_category('Vulnerability', news_df)
    generate_single_category('Crypto Currency', news_df)
    generate_single_category('Hacking', news_df)

    if blog_df.shape[0] == 0:
        print("reading the blog file as dataframe is empty")
        blog_df = pd.read_excel(blog_file_name)
    generate_blog(blog_df)
    
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
      #start_card_index = 0
      generate_card_trending(trending_df, 0, trending_cards_count)
    
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

def generate_blog(df):
    lines = []
    lines.append("document.write(' \\\n")
    
    for i in range(df.shape[0]):
      print(i)
      lines.append('<div class="d-md-flex post-entry-2 small-img"> \\\n')
      lines.append('<a href="' + df.iloc[i]['URL'] + '" class="me-4 thumbnail" target="_blank"> \\\n')
      lines.append('<img src="' + df.iloc[i]['Image'] + '" alt="" class="img-fluid"> \\\n')
      lines.append('</a> \\\n')
      lines.append('<div class="card-body p-0 mx-0" style="letter-spacing: 0.07rem;font-family:serif;color:#ADADAD;font-size:12px"> \\\n')
      lines.append('<h3 class="card-link text-dark font-weight-bold"> \\\n')
      lines.append('<a href="' + df.iloc[i]['URL'] + '" target="_blank"> ' + df.iloc[i]['Title'] + ' </a> \\\n')
      lines.append('</h3> \\\n')
      lines.append('<small class="text-uppercase font-weight-bold">  \\\n')
      lines.append('<span>' + df.iloc[i]['Date Created'] + '</span></small> \\\n')
      lines.append('</div> \\\n')
      lines.append('</div> \\\n')
    
    lines.append("');")
    
    file_name = "cyber_web/js/"+"gen_blogs.js"
    write_file(file_name, lines)

    return

def generate_single_category(cat_name, df):
    cat_df = df[df['Category']==cat_name]
    print(cat_df.shape)
    lines = []
    lines.append("document.write(' \\\n")
    
    for i in range(cat_df.shape[0]):
      print(f"Generating single category {i}")
      lines.append('<div class="d-md-flex post-entry-2 small-img"> \\\n')
      lines.append('<a href="' + cat_df.iloc[i]['URL'] + '" class="me-4 thumbnail" target="_blank"> \\\n')
      lines.append('<img src="' + cat_df.iloc[i]['Image'] + '" alt="" class="img-fluid"> \\\n')
      lines.append('</a> \\\n')
      lines.append('<div class="card-body p-0 mx-0" style="letter-spacing: 0.07rem;font-family:serif;color:#ADADAD;font-size:12px"> \\\n')
      lines.append('<h3 class="card-link text-dark font-weight-bold"> \\\n')
      lines.append('<a href="' + cat_df.iloc[i]['URL'] + '" target="_blank"> ' + cat_df.iloc[i]['Title'] + ' </a> \\\n')
      lines.append('</h3> \\\n')
      lines.append('<small class="text-uppercase font-weight-bold">  \\\n')
      lines.append('<span>' + cat_df.iloc[i]['Date Created'] + '</span></small> \\\n')
      lines.append('</div> \\\n')
      lines.append('</div> \\\n')
    
    if len(cat_df) == 0:
      lines.append('<h3>No relevant news article for this category</h3> \\\n')

    lines.append("');")
    
    file_name = "cyber_web/js/"+"gen_card_cat_"+cat_name+".js"
    write_file(file_name, lines)

    return

def generate_carousel(df, start, end):
  lines = []
  lines.append("document.write(' \\\n")
  print(f"Generating carousel {start}, {end}")
  print(df.head(2))
    
  for i in range(start, end):
      item_status = ""
      if i == 0:
        item_status = "active"

      lines.append('<div class="carousel-item ' + item_status + '"> \\\n')
      lines.append('<a href="' + df.iloc[i]['URL'] + '" target="_blank"> \\\n')
      lines.append('<img src="' + df.iloc[i]['Image'] + '" alt="" class="d-block w-100" style="height:50vh;filter: brightness(50%);"> \\\n')
      lines.append('<div class="carousel-caption"> \\\n')
      lines.append('<h2>' + df.iloc[i]['Title'] + '</h2> \\\n')
      lines.append('<p class="text-uppercase font-weight-bold" style="letter-spacing: 0.07rem;font-family:serif;font-size:12px">' 
                   + df.iloc[i]['Date Created'] + '</p> \\\n')
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
      print(f"Generating card column one--> {i}")
      lines.append('<div> \\\n')
      lines.append('<div class="card mb-5 border-0 rounded zoom" style="background: #fafafa;"> \\\n')
      lines.append('<a href="' + df.iloc[i]['URL'] + '" target="_blank" style="text-decoration:none"> \\\n')
      lines.append('<img src="' + df.iloc[i]['Image'] + '" class="card-img-top img-fluid" alt="..."> \\\n')
      lines.append('<div class="card-body p-0 mx-0 my-3" style="letter-spacing: 0.07rem;font-family:serif;color:#ADADAD;font-size:12px"> \\\n')
      lines.append('<small class="text-uppercase font-weight-bold"><span>' + df.iloc[i]['Category'] 
                   + '</span> <span class="mx-1">&bullet;</span> <span>' + df.iloc[i]['Date Created'] + '</span></small> \\\n')
      lines.append('<h2 class="card-link text-dark font-weight-bold my-3">' + df.iloc[i]['Title'] + '</h2> \\\n')
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
      print(f"Generating card column two and three--> {i}")
      lines.append('<div class="card mb-5 border-0 rounded zoom" style="background: #fafafa;"> \\\n')
      lines.append('<a href="' + df.iloc[i]['URL'] + '" target="_blank" style="text-decoration:none"> \\\n')
      lines.append('<img src="' + df.iloc[i]['Image'] + '" class="card-img-top img-fluid" alt="..."> \\\n')
      lines.append('<div class="card-body p-0 mx-0 my-3" style="letter-spacing: 0.07rem;font-family:serif;color:#ADADAD;;font-size:12px"> \\\n')
      lines.append('<small class="text-uppercase font-weight-bold"><span>' + df.iloc[i]['Category'] 
                   + '</span> <span class="mx-1">&bullet;</span> <span>' + df.iloc[i]['Date Created'] 
                   + '</span></small> \\\n')
      lines.append('<h5 class="card-link text-dark font-weight-bold my-3">' + df.iloc[i]['Title'] + '</h5> \\\n')
      lines.append('</div> \\\n')
      lines.append('</a> \\\n')
      lines.append('</div> \\\n')

    lines.append("');")
    
    write_file(file_name, lines)

    return

def generate_card_trending(df, start, end):
  lines = []
  lines.append("document.write(' \\\n")
  
  print(df.shape)
  
  for i in range(start, df.shape[0]):
      print(f"Generating card trending--> {i}")
      print(df['Title'][i])
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
    
def categorize_news(news_filename, feed_filename, news_test_df):
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
    if news_test_df.shape[0] == 0:
        print("reading the news file as dataframe is empty")
        news_test_df = pd.read_excel(feed_filename)

    # perform TFIDF 
    news_test_df_tfidf = loaded_tfidf.transform(news_test_df['Title'].str.lower())

    y_pred_cat = loaded_model.predict(news_test_df_tfidf)
    y_pred_cat_name = []
    for cat_pred, cat_pred_val in enumerate(y_pred_cat):
      y_pred_cat_name.append([cat for cat, cat_id in loaded_category_to_id.items() if cat_id == cat_pred_val][0])

    news_test_df['Category'] = y_pred_cat_name
    
    # load the test data
    print("reading the previous categorized news file ")
    # use the try statement where error may occur
    try:
        prev_news_df = pd.read_excel(news_filename)

        print(f"Total news earlier-->{prev_news_df.shape}")
        print(f"Total news to add-->{news_test_df.shape}")
        # A continuous index value will be maintained
        # across the rows in the new appended data frame.
        print(f"Total news to add-->{news_test_df.shape}")
        #news_test_df = news_test_df.append(prev_news_df, ignore_index=True)    # to collect data for retraining
        news_test_df = pd.concat([news_test_df, prev_news_df], ignore_index=True)    # append is deprecated
        print(f"Dropping duplicates")
        news_test_df.drop_duplicates(inplace=True)      #drop the duplicates
        print(f"Total news later-->{news_test_df.shape}")
    except FileNotFoundError:
        print("No file!!")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    
    # convert the 'Date Created' column to datetime format
    news_test_df['Date Created'] = pd.to_datetime(news_test_df['Date Created'])

    news_test_df = news_test_df.sort_values(by=['Date Created'], ascending=False).reset_index(drop=True)

    # convert the 'Date Created' column to string format
    news_test_df['Date Created'] = news_test_df['Date Created'].astype(str)

    # date format 2022-08-01 want July 01, 2022
    news_test_df['Date Created'] = news_test_df['Date Created'].apply(lambda date : 
                                    datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y"))
    print(news_test_df.head())
    
    # write all records to file
    news_test_df.to_excel(news_filename, index=False)
    
    return news_test_df
    
def main():
    news_categorized_file = "cyber_web/excels/news_categorized.xlsx"
    blogs_file = "cyber_web/excels/blog_feed.xlsx"
    news_feed_file = "cyber_web/excels/news_feed.xlsx"
    print(f"Executing gen_feed_file method")
    blog_df, news_df = gen_feed.gen_feed_file(news_feed_file, blogs_file)
    print(f"Executed gen_feed_file method")
    print(f"Executing categorize_news method")
    news_df = categorize_news(news_categorized_file, news_feed_file, news_df)
    print(f"Executed categorize_news method")
    print(f"Executing generate_news_html method")
    generate_news_html(news_categorized_file, blogs_file, blog_df, news_df)
    print(f"Executed generate_news_html method")
        
if __name__ == "__main__":
    main()
