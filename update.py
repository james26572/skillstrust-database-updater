import datetime
from delete import delete_closed_positions
from flagged import flag
from new_jobs import get_new_jobs_data
import schedule

def update_database_for_countries():
    print(datetime.now())
    print("DELETING CLOSED POSITIONS")
    delete_closed_positions()
    countries_in_europe = [
    "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina",
    "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia",
     "Finland",
    "France", "Germany", "Greece", "Hungary", "Iceland",
      "Ireland", "Italy", "Kosovo",
    "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco",
    "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal",
    "Romania", "Russia", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain",
    "Sweden", "Switzerland", "Ukraine", "United Kingdom", "Vatican City"
]
    print(datetime.now())
    print("UPDATING DATABASE WITH NEW JOBS")
    for country in countries_in_europe:
        update_database(country)
        print("Finished for country : ",country)

    # flag companies who have had 5 open positions at some point and currently not in flag table
    print(datetime.now())
    print("FLAGGING COMPANIES")
    flag()



def update_database(country):
    import psycopg2
    conn = psycopg2.connect(
            host="database-1.cqmfyvudbg6y.eu-west-1.rds.amazonaws.com",
            port = "5432",
            database="users",
            user="postgres",
            password="24Feb2003!!"
        )
    
    
    
    cursor = conn.cursor()


    select_query = "SELECT linkedin_job_url_cleaned FROM job_data;"
    cursor.execute(select_query)
    existing_urls = set(row[0] for row in cursor.fetchall())

    new_jobs = get_new_jobs_data(country)
    


    sql_query = """
    INSERT INTO job_data (linkedin_job_url_cleaned, company_name,linkedin_company_url_cleaned, job_title, job_location, posted_date, normalized_company_name,level,category,job_language)
    VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s);
    """
    for job in new_jobs:
        url = job['linkedin_job_url_cleaned']
        if url not in existing_urls:
            cursor.execute(sql_query, (
                job['linkedin_job_url_cleaned'],
                job['company_name'],
                job['linkedin_company_url_cleaned'],
                job['job_title'],
                job['job_location'],
                job['posted_date'],
                job['normalized_company_name'],
                job['level'],
                job['category'],
                job["job_language"],
            ))
            conn.commit()
        else:
            print(f"Job with URL {url} already exists in the database.")
        conn.commit()
    cursor.close()
    conn.close()

def job():
    # Schedule the function to run every Sunday at 9 PM
    schedule.every().monday.at("00:05").do(update_database_for_countries)

if __name__ == "__main__":
    # Schedule the job
    job()

    # Keep the script running
    while True:
        schedule.run_pending()
        