import pandas as pd

import preprocess
import questions

if __name__ == '__main__':
    data = pd.read_csv('./data.csv')
    data.drop(preprocess.irrelevant_column, axis=1, inplace=True)

    # question 6, 7
    group1 = questions.preprocessing6_7(data)
    questions.draw6_7(group1)

    # question 8
    group2 = questions.preprocessing8(data)
    questions.draw8(group2)
