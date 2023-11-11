#If you are using Intellij or PyCharm, you can use scratch files of type http.
#To create one, double-shift, write 'scratch', choose the create a scratch file option.
#For the type of scratch file, choose 'http'.
#For the content, paste the following. If the api changes, change the content accordingly:

GET http://localhost:8000/sources

###

POST http://localhost:8000/query
Content-Type: application/json

{
  "value": "What is the answer to the universe?"
}

###

POST http://localhost:8000/sources
Content-Type: application/json

{
  "url": "https://www.google.com",
  "title": "Google Source"
}
