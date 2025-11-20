from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# --- PART 1: SUMMARIZATION ---
# Load the summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def generate_summary(text_content):
    """
    Takes a long string of text and returns a summary.
    """
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

# --- PART 2: RECOMMENDATIONS ---
def get_recommendations(user_saved_books, all_books):
    """
    user_saved_books: List of book dictionaries the user likes
    all_books: List of ALL book dictionaries in the database
    """
    # 1. If user hasn't saved anything, return empty
    if not user_saved_books:
        return []

    # 2. Prepare Data
    # We want to recommend books that are NOT already in the saved list
    saved_ids = [str(b['_id']) for b in user_saved_books]
    candidate_books = [b for b in all_books if str(b['_id']) not in saved_ids]

    if not candidate_books:
        return [] # No books left to recommend

    # 3. Build "Content Strings"
    # We combine Title + Genre + Description to create a "profile" for each book
    saved_text = " ".join([f"{b.get('title')} {b.get('genre')} {b.get('description')}" for b in user_saved_books])
    candidate_texts = [f"{b.get('title')} {b.get('genre')} {b.get('description')}" for b in candidate_books]

    # 4. Create the TF-IDF Matrix (Convert text to numbers)
    # This creates a map of words.
    tfidf = TfidfVectorizer(stop_words='english')
    
    # Combine everything to train the vectorizer
    # The first item is the "User Profile", the rest are candidates
    corpus = [saved_text] + candidate_texts
    try:
        tfidf_matrix = tfidf.fit_transform(corpus)
    except ValueError:
        # Happens if not enough text data
        return []

    # 5. Calculate Similarity
    # Compare the User Profile (index 0) with all candidates (indices 1 to end)
    cosine_sim = linear_kernel(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # 6. Get Top 3 Matches
    # Get indices of books with highest scores
    related_docs_indices = cosine_sim.argsort()[:-4:-1] # Top 3
    
    recommended_books = []
    for i in related_docs_indices:
        # Only include if similarity score is greater than 0
        if cosine_sim[i] > 0:
            recommended_books.append(candidate_books[i])

    return recommended_books