import jieba
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from merge_challenges_records import ChallengeManager

def chinese_tokenizer(text):
    return list(jieba.cut(text))

def main():
    mgr = ChallengeManager()
    succ_docs = mgr.success_user_msgs
    fail_docs = mgr.fail_user_msgs

    vectorizer = CountVectorizer(
        tokenizer=chinese_tokenizer,
        ngram_range=(2, 5),
        min_df=2
    )
    vectorizer.fit(succ_docs + fail_docs)
    features = vectorizer.get_feature_names_out()

    X_succ = vectorizer.transform(succ_docs)
    X_fail = vectorizer.transform(fail_docs)

    count_succ = np.asarray(X_succ.sum(axis=0)).ravel()
    count_fail = np.asarray(X_fail.sum(axis=0)).ravel()
    score = (count_succ + 1) / (count_fail + 1)

    df = pd.DataFrame({
        'ngram': features,
        'count_succ': count_succ,
        'count_fail': count_fail,
        'score': score
    })

    df = df[df['ngram'].str.contains(r'[\u4e00-\u9fff]')]

    top_succ = df.sort_values('score', ascending=False).head(20)
    top_fail = df.sort_values('score', ascending=True).head(20)

    print("\n=== Top 20 Chinese n-grams Indicating Success ===")
    print(top_succ[['ngram', 'count_succ', 'count_fail', 'score']].to_string(index=False))

    print("\n=== Top 20 Chinese n-grams Indicating Failure ===")
    print(top_fail[['ngram', 'count_succ', 'count_fail', 'score']].to_string(index=False))

if __name__ == '__main__':
    main()
