import google.generativeai as genai
from utils import *

genai.configure(api_key = get_key())
model = genai.GenerativeModel('gemini-pro')

already_covered, prompt = create_prompt()
article = model.generate_content(prompt)

send_telegram(article.text)

today_title = model.generate_content('Create a title for this article:\n'+article)
storicize_article(already_covered, today_title.text)
