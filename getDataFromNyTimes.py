import requests
def getFirstArticle(year):
    my_key = "qIJnp0lno0aUTYCA9uaHcNhAhK4oGmjY"

    url = f"https://api.nytimes.com/svc/archive/v1/{year}/1.json?api-key="+my_key

    r = requests.get(url)
    jsonR = r.json()
    
    response = jsonR['response']

    articles = response['docs']
    first_article = articles[0]
    return first_article

abstract = getFirstArticle(1956)
print(abstract)




