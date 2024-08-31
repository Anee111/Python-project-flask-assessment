from flask import Flask, request, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load content data
data = pd.read_csv('data/content.csv')

# Create TF-IDF vectorizer and fit on tags
tfidf = TfidfVectorizer(stop_words='english')
data['tags'] = data['tags'].fillna('')
tfidf_matrix = tfidf.fit_transform(data['tags'])

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Index for quick lookup
indices = pd.Series(data.index, index=data['title']).drop_duplicates()

@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    title = request.form.get('title')
    if title not in indices:
        return render_template('index3.html', recommendation_text="Content not found.")
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:4]  # Get top 3 similar items

    content_indices = [i[0] for i in sim_scores]
    recommended_content = data[['title', 'category']].iloc[content_indices]

    return render_template('index3.html', tables=[recommended_content.to_html(classes='data')], titles=recommended_content.columns.values)

if __name__ == '__main__':
    app.run(debug=True)
