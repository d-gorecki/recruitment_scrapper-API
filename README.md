

# Implementation of recruitment task for the position of backend dev.
### _Tech-stack: Python, Django, Django REST framework, BS4, Docker, docker-compose_

## Task objective

Collect data from each article from https://teonite.com/blog/ blog, process it and present it in form of statistics.

## Implementation method

The data should be collected by processing individual HTML documents returned by https://teonite.com/blog/ (Web scraping).
The script should find the addresses of subpages with articles and collect the necessary data from them.
The data should go to the database. Statistics should be
calculated on the basis of data from the database.

## Functional requirements

* download the content of articles and their authors from https://teonite.com/blog/
* a REST-type service that returns the following statistics in the form of a JSON document:
  * top 10 words with their count available at /stats/
  * top 10 words with their count per author available at /stats/&lt;author>/
  * authors of posts with their name available at /authors/

## Non-functional requirements
* code written in Python > 3.6
* code posted as a public repository
* data collected in the PostgreSQL database
* use of Docker and docker compose (base and application as separate services)
* data issued in the form of a JSON document in the form of a REST API
* basing the application on the django framework and django-rest-framework
* after cloning the repository and running the docker-compose up command, the application should be available on port 8080
* for optimization reasons, the data needed to generate statistics should not be collected with each request sent to /stats/ or /stats/&lt;author>/,
* the maximum service response time is 1 second
