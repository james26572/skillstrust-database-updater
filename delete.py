import requests
from bs4 import BeautifulSoup
import psycopg2









def delete_closed_positions():
    closed_positions = 0
    conn = psycopg2.connect(
            host="database-1.cqmfyvudbg6y.eu-west-1.rds.amazonaws.com",
            port = "5432",
            database="users",
            user="postgres",
            password="24Feb2003!!"
        )
    cursor = conn.cursor()

    query = '''SELECT "linkedin_job_url_cleaned" FROM job_data;'''
    cursor.execute(query)

    results = cursor.fetchall()

    for result in results:
        job_url = result[0]
        r = requests.get(job_url)


        if r.status_code == 404 or pos_closed(r):
            query = '''DELETE FROM job_data WHERE "linkedin_job_url_cleaned" = '{job_url}';'''.format(job_url=job_url)
            cursor.execute(query)
            closed_positions +=1
            print("closed pos",closed_positions)
            print(job_url)
            conn.commit()
    cursor.close()
    conn.close()
        

def pos_closed(html_page):
    soup = BeautifulSoup(html_page.content, 'html.parser')

# Search for the desired element that contains the "No longer accepting applications" text
    closed_job_element = soup.find('figcaption', class_='closed-job__flavor--closed')

# Check if the element exists and its text matches the desired string
    if closed_job_element and closed_job_element.get_text(strip=True) == "No longer accepting applications":
    # The job position is closed
    # Add your logic here for handling closed positions
        return True
    return False



