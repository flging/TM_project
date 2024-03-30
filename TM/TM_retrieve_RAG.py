import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from openai import OpenAI

client = OpenAI()

def get_embeddings(texts, model="text-embedding-3-small"):
    RAGs = []
    
    for text in texts:
        response = client.embeddings.create(
            input=[text],
            model=model
        )
        RAGs.append(response.data[0].embedding)
    
    return RAGs

def retrieve_RAG(query_text):
    df = pd.read_csv("TM/text_embeddings.csv")

    def string_to_array(s):
        return np.array([float(item) for item in s.strip("[]").split(",")])

    df['Embedding'] = df['Embedding'].apply(string_to_array)

    def find_top_similar_texts(query_text, embeddings_df, top_n=5, model="text-embedding-3-small"):
        query_embedding = get_embeddings([query_text], model=model)[0]
        
        similarities = cosine_similarity([query_embedding], np.stack(embeddings_df['Embedding'].values)).flatten()
        
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        top_texts = embeddings_df.iloc[top_indices]['Text'].values
        top_similarities = similarities[top_indices]
        
        return top_texts, top_similarities

    
    index = []
    top_texts, top_similarities = find_top_similar_texts(query_text, df, top_n=5)

    for i, (text, similarity) in enumerate(zip(top_texts, top_similarities), 1):
        index.append(text)

    return index
