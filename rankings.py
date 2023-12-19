import json
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
    # replace all non-alphanumeric characters with empty string regex
    # return re.sub(r'\W+', '', title).lower()
    return title.lower().replace(" ", "_").sub(r'(\W+|_)', '', title).lower()

def parse_movies_with_gender_score(input_list):    

    parsed_data = []
    for item in input_list:
        item = item.replace("> 250", "250")
        split_item = item.split()
        year = split_item[0]
        ranking_women, ranking_men = [int(ranking) for ranking in split_item[-3:-1]]
        title = ' '.join(split_item[1:-4])
        gender_score = calculate_gender_score(ranking_women, ranking_men)

        parsed_data.append([year, title, ranking_women, ranking_men, gender_score])

    df = pd.DataFrame(parsed_data, columns= ['year', 'title', 'ranking_women', 'ranking_men', 'gender_score'])
    return df


def main():
    json_input = open_json_file('preferences_table')
    parsed = parse_movies_with_gender_score(json_input)
    parsed.to_csv('data/preferences_table_ready.csv', index=False)

if __name__ == "__main__":
    main()