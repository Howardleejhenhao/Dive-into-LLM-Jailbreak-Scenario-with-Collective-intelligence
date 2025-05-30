import jieba
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from merge_challenges_records import ChallengeManager

def chinese_tokenizer(text):
    return list(jieba.cut(text))

def main():
    mgr = ChallengeManager()
    docs = mgr.success_user_msgs + mgr.fail_user_msgs

    embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    embeddings = embedder.encode(
        docs,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    vectorizer = CountVectorizer(
        tokenizer=chinese_tokenizer,
        min_df=5
    )

    topic_model = BERTopic(
        embedding_model=None,
        language="chinese (traditional)",
        vectorizer_model=vectorizer,
        nr_topics=10
    )

    topics, probs = topic_model.fit_transform(docs, embeddings)

    info = topic_model.get_topic_info()
    print("Top 10 Topics:")
    print(info.head(10).to_string(index=False))

    topic_ids = [tid for tid in info['Topic'].unique() if tid != -1][:5]
    for topic_id in topic_ids:
        print(f"\n--- Topic {topic_id} Keywords ---")
        for word, weight in topic_model.get_topic(topic_id):
            print(f"{word}: {weight:.4f}")

if __name__ == "__main__":
    main()
