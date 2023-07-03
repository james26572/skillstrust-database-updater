


import openai
import os
token = "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"
openai.api_key = os.getenv("OPEN_AI_KEY")
def classify_title_language(job_title):
    prompt = '''State the language that the job title, {job_title} is in. Just state the language,
    e.g 'Senior corporate analyst' would be classified as "English"'''.format(job_title=job_title)
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        
        temperature=0.5  # Adjust the temperature to control randomness
    )
    language = response.choices[0].text.strip()
    return language


import psycopg2

conn = psycopg2.connect(
            host="database-1.cqmfyvudbg6y.eu-west-1.rds.amazonaws.com",
            port = "5432",
            database="users",
            user="postgres",
            password="24Feb2003!!"
        )


cursor = conn.cursor()


query = '''SELECT "job_title" FROM job_data'''

cursor.execute(query)

rows = cursor.fetchall()
for i,row in enumerate(rows):
    job_title = row[0]
    language = classify_title_language(job_title)
    print(language)
    cursor.execute('''UPDATE job_data SET job_language = %s WHERE job_title = %s''',(language,job_title))
    conn.commit()
cursor.close()
conn.close()