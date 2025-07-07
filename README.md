# Video Game Search

This website was put together for a final project during Fall term at Portland State University, and was started the 28th of November 2023 and completed on the 6th of December 2023.

#### A quick note
The commit history, unfortunately, doesn't reflect the correct commit history on the original repository. I wanted to separate the class work from the final project and wound up with a odd looking commit history when transferring it over.

## Goal of the Project
The purpose behind the project was to experience developing and deploying a web application on the Google Cloud Platform using Python, and (as a graduate student requirement) two different API endpoints and incorporate them in some fashion.

I had come up with the idea of allowing the user to do a search of the [Internet Games Database (IGDB)](https://www.igdb.com/) using their free API, and Python package.

Once the users query is sent and the IGDB endpoint returns some sort of response, the [Google Cloud Vision AI API](https://cloud.google.com/vision?hl=en) kicks in and generates a form of alt-text by using the labels it identifies on the games box art.

## Technologies Used
The following was used to complete this project:

- Python with the following packages
  - flask
  - igdb-api-v4
  - google-cloud-vision
  - gunicorn
  - requests
- Flask - To create and direct the websites pages as well as acting as the backend for the requests made by the user.
- Jinja - To format and act as the templates for the data presented once a successful query is completed by the user.
- Docker - Used to containerize the app to be deployable on the Google Cloud Platform.
- Google Cloud Platform (GCP) - To host and deploy the app through Cloud Run using a docker container that is built and saved on GCP.
- Google Cloud Vision AI - Generates labels to be used in the alt-text for the games cover art.

# Challenges
The hardest part of this project was parsing the data from the IGDB API after receiving it. Initially, I thought it was just getting the app to appear in the dev environment I was using, but the IGDB API is particularly stale.

When retrieving information, some of the endpoints were non-functional, and so there were workarounds that had to be performed to get the exact data I needed. This included, but not limited to: obtaining the exact release date, the ESRB age rating, and only wanting to view actual real and released games.

IGDB allows, seemingly, anyone to upload and add a game to the database. This means there are games that are simply fan creations that don't live on the mainstream. This is fine, but it was interfering with more legitimate results causing these fan creations to have precedence over mainstream releases.

I had to develop this workaround to source legit titles because of the limitations I had to set for both the IGDB API and Google Cloud Vision AI API. If the user attempted too many results, the page would eventually timeout instead of waiting for a response.

# Future Plans
Ideally, I would like to create a very visually interactive website where people can see and filter games at a large monthly calendar view, and providing a way to do explicit filtering to a month/day/year - such as a persons birthday - to see what games were released that day. This was a great first experience in understanding how to deploy such a website, but also gave me ideas on how to better approach the problems I could foresee coming up - such as the previously mentioned limitations from the IGDB API.
