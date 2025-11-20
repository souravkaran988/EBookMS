# app/ai_utils.py

# 1. Try to import AI libraries. If they don't exist, we set flags to False.
try:
    from transformers import pipeline
    has_transformers = True
except ImportError:
    has_transformers = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import linear_kernel
    has_sklearn = True
except ImportError:
    has_sklearn = False

# 2. Attempt to load the Summarizer (Only if library exists)
if has_transformers:
    try:
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    except Exception as e:
        print(f"Could not load AI model: {e}")
        has_transformers = False

# --- FUNCTION 1: SUMMARIZATION ---
def generate_summary(text_content):
    """
    Takes a long string of text and returns a summary.
    """
    if not has_transformers:
        return "AI Summary is unavailable on this server (Low Memory Mode)."

    if not text_content or len(text_content) < 50:
        return "Not enough text to generate a summary."

    try:
        clean_text = text_content[:2000]
        summary_list = summarizer(
            clean_text, 
            max_length=150, 
            min_length=50, 
            do_sample=False, 
            truncation=True 
        )
        return summary_list[0]['summary_text']
    except Exception as e:
        print(f"AI Error: {e}")
        return "An error occurred while generating the summary."

# --- FUNCTION 2: RECOMMENDATIONS ---
def get_recommendations(user_saved_books, all_books):
    # Fallback if Scikit-Learn is missing
    if not has_sklearn:
        return all_books[:3] if all_books else []

    if not user_saved_books:
        return []

    # Prepare Data
    saved_ids = [str(b['_id']) for b in user_saved_books]
    candidate_books = [b for b in all_books if str(b['_id']) not in saved_ids]

    if not candidate_books:
        return []

    # Build Content Strings
    saved_text = " ".join([f"{b.get('title')} {b.get('genre')} {b.get('description')}" for b in user_saved_books])
    candidate_texts = [f"{b.get('title')} {b.get('genre')} {b.get('description')}" for b in candidate_books]

    # Create Matrix
    try:
        tfidf = TfidfVectorizer(stop_words='english')
        corpus = [saved_text] + candidate_texts
        tfidf_matrix = tfidf.fit_transform(corpus)
    except ValueError:
        return []

    # Calculate Similarity
    cosine_sim = linear_kernel(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Get Top 3
    related_docs_indices = cosine_sim.argsort()[:-4:-1]
    
    recommended_books = []
    for i in related_docs_indices:
        if cosine_sim[i] > 0:
            recommended_books.append(candidate_books[i])

    return recommended_books