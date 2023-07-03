import requests
from categorize import classify_job_title
from add_language import classify_title_language

def get_new_jobs_data(country):
    
    new_jobs_data = []
    url = "https://linkedin-jobs-search.p.rapidapi.com/"

    payload = {
	"search_terms": "analyst",
	"location": "Chicago, IL",
	"page": "1"
}

    

    headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "4a22bc8221mshb65c02681170b0cp12211djsn1ce0f5676f62",
	"X-RapidAPI-Host": "linkedin-jobs-search.p.rapidapi.com"
}
    

    

    

    
    page = 1
    payload["location"] = country
    payload["page"] = str(page)
    response = requests.post(url, json=payload, headers=headers)

        
    

    

   
    

    while len(response.json())>=1:
            

            #jprint(response.json())
            if not isinstance(response.json(),list):
                
                break
            for job_info in response.json():
            
                if isinstance(job_info,str):
                    
                    break
                job_url = job_info["job_url"]
                level = get_level(job_url)
                job_title = job_info["job_title"]
                job_title = classify_job_title(job_title)
                category = add_category(job_title)
                job_language = classify_title_language(job_title)
                

                job_info["level"] = level
                job_info["category"] = category
                job_info["job_language"] = job_language
                
                new_jobs_data.append(job_info)
                

                
                

                
            page +=1
            
            
            
            

            payload["page"] = str(page)
            
            response = requests.post(url, json = payload, headers = headers)
        
    return new_jobs_data
    
def get_level(url):
    import requests
    from bs4 import BeautifulSoup

    

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    s = soup.find(class_="description__job-criteria-text")

    if s is None:
        return "N/A"

    

    return s.text.strip()


def get_jobs_data():
    import psycopg2
    conn = psycopg2.connect(
            host="database-1.cqmfyvudbg6y.eu-west-1.rds.amazonaws.com",
            port = "5432",
            database="users",
            user="postgres",
            password="24Feb2003!!"
        )
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_data")
    old = cursor.fetchall()
    return old

def add_category(title):
        category = classify_job_title(title)
        return category
