import openai

openai.api_key = "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"

def generate_prompt(job_title, category_list):
    category_options = ', '.join([f'"{category}"' for category in category_list])
    prompt = f"Pick one of the follwing categories from the list {category_list} which best match the job title: {job_title}"
    return prompt

def classify_job_title(job_title):
    categories = ["Finance Analyst", "Data Analyst", "Risk Analyst",  "Business Analyst", "Customer Analyst", "Marketing Analyst", "Product Analyst", "Technical Analyst", "Investment Analyst", "QC Analyst", "Tax Analyst",
                ]
    prompt = generate_prompt(job_title,categories)
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        
        temperature=0.5  # Adjust the temperature to control randomness
    )
    category = response.choices[0].text.strip()

    if category in categories:
        return category
    return 'Other'