from text2vec import Word2Vec
import numpy as np

model = None


def log(*args, **kwargs):
    print("[AOS]", *args, **kwargs)


def compute_emb(words):
    """
    Compute the embedding of a list of words
    
    :param words: a list of tuples, each tuple = (word, weight)
    """
    global model
    if model is None:
        model = Word2Vec("w2v-light-tencent-chinese")

    # Embed a list of sentences
    embeddings = model.encode(list(map(lambda x: x[0], words)), show_progress_bar=False, normalize_embeddings=True)

    emb0 = embeddings[0]
    for i in range(1, len(embeddings)):
        emb0 += embeddings[i] * words[i][1]
    emb0 /= np.linalg.norm(emb0)
    # print("emb0:", emb0, np.linalg.norm(emb0))

    return emb0
