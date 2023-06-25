import datetime
import psycopg2

def flag():
    start_date = datetime.datetime.strptime('2020-08-28', '%Y-%m-%d').date()

    # Get the current date
    current_date = datetime.date.today() - datetime.timedelta(weeks=1)

    # Establish a database connection
    conn = psycopg2.connect(
        host="database-1.cqmfyvudbg6y.eu-west-1.rds.amazonaws.com",
        port="5432",
        database="users",
        user="postgres",
        password="24Feb2003!!"
    )

    # Create a cursor to execute SQL queries
    cursor = conn.cursor()

    # Iterate over the weeks
    while start_date <= current_date:
        # Define the end date of the week (7 days after the start date)
        end_date = start_date + datetime.timedelta(days=6)

        # Convert the start and end dates to strings in the format expected by the SQL query
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Build the SQL query with the start and end dates
        query = f'''SELECT company_name, ARRAY_AGG("linkedin_job_url_cleaned"), COUNT(*) as "count"
        FROM job_data
        WHERE posted_date BETWEEN '{start_date_str}' AND '{end_date_str}'
        GROUP BY company_name
        HAVING COUNT(*) >= 5
        '''

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        results = cursor.fetchall()
        print("Results for the week:", start_date_str, "-", end_date_str)
        
        

        query = '''INSERT INTO flagged (company_name) VALUES (%s)'''

        for result in results:
            company_name = result[0]
            

            # Check if the company name already exists in the flagged table
            cursor.execute("SELECT COUNT(*) FROM flagged WHERE company_name = %s", (company_name,))
            count = cursor.fetchone()[0]

            # Insert the company name only if it doesn't exist in the flagged table
            if count == 0:
                cursor.execute(query, (company_name,))

        start_date += datetime.timedelta(weeks=1)

    # Commit the changes and close the cursor and database connection
    conn.commit()
    cursor.close()
    conn.close()
