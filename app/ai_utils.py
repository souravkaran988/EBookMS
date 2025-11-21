# app/ai_utils.py

def generate_summary(text_content):
    return "⚠️ AI Summary is unavailable on the free hosting plan (Memory Limit)."

def get_recommendations(user_saved_books, all_books):
    # Simple random recommendation logic
    saved_ids = [str(b['_id']) for b in user_saved_books]
    recommended = []
    for book in all_books:
        if str(book['_id']) not in saved_ids:
            recommended.append(book)
            if len(recommended) >= 3:
                break
    return recommended