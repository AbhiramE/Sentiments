import pandas as pd


def compute_compound_score():
    frame = pd.DataFrame()
    list_ = []

    for i in range(1, 5):
        df = pd.read_csv('Tweets' + str(i) + '.csv')
        list_.append(df)
        print(len(df[(df['Compound'] == 0.0)]))

    frame = pd.concat(list_)

    sentiment = frame['Compound'].sum() / len(frame)

    print(sentiment)

compute_compound_score()