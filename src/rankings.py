import json
import re
import pandas as pd

def open_path(name, mode, type="json"):
    return open(f"data/{name}.{type}", mode)

def save_json_file(name, data):
    with open_path(name, 'w') as file:
        json.dump(data, file)

def open_json_file(name):
    with open_path(name, 'r') as file:
        json_input = json.load(file)
    return json_input

def normalize_rank(rank):
    """ Normalize the rank to a scale from 0 to 1 """
    return 1 - (int(rank) - 1) / 499.0

def normalize_rank(rank):
    """ Normalize the rank to a scale from 0 to 1 """
    return 1 - (rank - 1) / 499.0

def calculate_gender_score(rank_a, rank_b):
    """ Calculate the weighted score based on normalized ranks and average rank """
    normalized_a = normalize_rank(rank_a)
    normalized_b = normalize_rank(rank_b)


    return (normalized_b - normalized_a) 

def normalize_title(title):
    """ Normalize the title to a format that can be used for comparison """
    title = title.lower()
    return re.sub(r'(\W+)', '', title)

def add_bechdel_params(movie_df):
    url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/bechdel/movies.csv"
    bechdel_df = pd.read_csv(url, encoding='latin-1')
    bechdel_df['title_normalized'] = bechdel_df['title'].apply(normalize_title)
    bechdel_df['year'] = bechdel_df['year'].astype(str)


    merged_df = pd.merge(movie_df, bechdel_df[['year', 'title_normalized', 'binary', 'clean_test', 'test']], 
                     on=['year', 'title_normalized'], how='left')
    merged_df.to_csv('data/bechdel_table_ready.csv', index=False)
    return merged_df

def parse_movies_with_gender_score(input_list):    

    parsed_data = []
    for item in input_list:
        item = item.replace("> 250", "250")
        split_item = item.split()
        year = split_item[0]
        ranking_women, ranking_men = [int(ranking) for ranking in split_item[-3:-1]]
        title = ' '.join(split_item[1:-4])
        title_normalized = normalize_title(title)
        gender_score = calculate_gender_score(ranking_women, ranking_men)

        parsed_data.append([year, title, title_normalized, ranking_women, ranking_men, gender_score])

    df = pd.DataFrame(parsed_data, columns= ['year', 'title', 'title_normalized', 'ranking_women', 'ranking_men', 'gender_score'])
    add_bechdel_params(df)
    return df


def main():
    json_input = open_json_file('preferences_table')
    parsed = parse_movies_with_gender_score(json_input)
    parsed.to_csv('data/preferences_table_ready.csv', index=False)

if __name__ == "__main__":
    main()