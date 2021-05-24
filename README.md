# seneca_comenta
## Twitter bot that applies NLP to comment on news stories with Seneca sentences

This bot reads headlines in Spanish newspapers, chooses one that connects with some sentence of Seneca's Letters to Lucilius, and publishes both the headline and the sentence once a day in the Twitter account https://twitter.com/SenecaOpinaBot. The result gives the impression that the stoic philosopher is commenting on current stories in the news.

1. Parse RSS feeds of _El País_, _El Mundo_, _ABC_, and _El Confidencial_ newspapers.
2. Extract title and summary of today's stories.
3. Filter and exclude the ones that include terms like "death", "kill", etc (to avoid playful results with tragic stories).
4. Create embeddings for each summary with sentence-transformers.
5. Compare each one with every sentence of _Letters to Lucilius_, previously turned into embeddings.
6. Put a score to each comparison summary-sentence in order to select the most similar.
7. Create a tweet with Seneca's quote, letter number, and link to the story.
8. Post the tweet once a day using Github Actions.

A first attempt to deploy the bot through Heroku failed because the Bert model used for the embeddings ('distiluse-base-multilingual-cased-v1') was too big.
