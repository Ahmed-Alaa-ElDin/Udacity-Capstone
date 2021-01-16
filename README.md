# Casting Team (Udacity-Capstone)
## Getting Started
### Installing Dependencies
You can run the following code to install the dependencies:

    pip install -r requirements.txt

or 

    pip3 install -r requirements.txt
   This will install all of the required packages we selected within the  `requirements.txt`  file.

## Running the server
From within the directory of the project run the server by executing:

    export FLASK_APP=app.py
    flask run

***

# Endpoints:


 - GET `'/'` :
	 - Redirect you to the home page.
---

> ## Movie Section

 
 - GET `'/api/movies'`:
	 - Returns JSON object contains all movies with their details.
 - GET `'movies'`:
	 - Redircet you to the movies page contains all movies.
 - GET `'/movies/create'`:
	 - Redircet you to the form page that creates new movies.
 - POST `'/api/movies/create'`: 
	 - You pass data for inserting new movie and it will return `'Movie with name {movie-name} Inserted Successfully'`
 - POST `'/movies/create'`:
	 -  Gets data from the previous form and insert new movie and redirect you to the movies page.
 - DELETE `'/api/movies/delete/<int:movie_id>'` :
	 - Gets the ID of the movie and remove it and return message `'Movie deleted successfully'` .
 - DELETE `'/movies/delete/<int:movie_id>'`:
	 - Gets the ID of the movie and redirect you to the movies page.
 - POST `'/api/movies/edit/<int:movie_id>'`:
	 - Gets the ID of the movie and gets its data and return message `Welcome to edit page`.
-  POST `'/movies/edit/<int:movie_id>'`:
	-  Gets the ID of the movie and redirect you to the edit page with the data of selected movie.
- PATCH `'/api/movies/edit/<int:movie_id>'`:
	- Takes the data from the request and updates that movie then returns message `Movie edited successfully`.
- PATCH `'/movies/edit/<int:movie_id>'`:
	- Takes the data from the editing form and updates that movie then redirect you to movies page. 
---
> ## Actor Section
- GET `'/api/actors'`:
	 - Returns JSON object contains all actors with their details.
 - GET `'actors'`:
	 - Redircet you to the actors page contains all actors.
 - GET `'/actors/create'`:
	 - Redircet you to the form page that creates new actors.
 - POST `'/api/actors/create'`: 
	 - You pass data for inserting new actor and it will return `'Actor with name {actor-name} Inserted Successfully'`
 - POST `'/actors/create'`:
	 -  Gets data from the previous form and insert new actor and redirect you to the actors page.
 - DELETE `'/api/actors/delete/<int:actor_id>'` :
	 - Gets the ID of the actor and remove it and return message `'Actor deleted successfully'` .
 - DELETE `'/actors/delete/<int:actor_id>'`:
	 - Gets the ID of the actor and redirect you to the actors page.
 - POST `'/api/actors/edit/<int:actor_id>'`:
	 - Gets the ID of the actor and gets its data and return message `Welcome to edit page`.
-  POST `'/actors/edit/<int:actor_id>'`:
	-  Gets the ID of the actor and redirect you to the edit page with the data of selected actor.
- PATCH `'/api/actors/edit/<int:actor_id>'`:
	- Takes the data from the request and updates that actor then returns message `Actor edited successfully`.
- PATCH `'/actors/edit/<int:actor_id>'`:
	- Takes the data from the editing form and updates that actor then redirect you to actors page. 
---

# Premissions
The site has three roles:

 1. **Casting Assistant** has the following premissions:
	 - GET `'/api/movies'`.
	 - GET `'movies'`.
	 - GET `'/api/actors'`.
	 - GET `'actors'`.
2. **Casting Director** has the following premissions:
	- Premissions of *Casting Assistant* plus:
	- POST `'/api/movies/edit/<int:movie_id>'`.
	-  POST `'/movies/edit/<int:movie_id>'`.
	- PATCH `'/api/movies/edit/<int:movie_id>'`.
	- PATCH `'/movies/edit/<int:movie_id>'`.
	- GET `'/actors/create'`.
	- POST `'/api/actors/create'`.
	- POST `'/actors/create'`.
	- DELETE `'/api/actors/delete/<int:actor_id>'`.
	- DELETE `'/actors/delete/<int:actor_id>'`.
	- POST `'/api/actors/edit/<int:actor_id>'`.
	-  POST `'/actors/edit/<int:actor_id>'`.
	- PATCH `'/api/actors/edit/<int:actor_id>'`.
	- PATCH `'/actors/edit/<int:actor_id>'`.
3. **Executive Producer** has all premissions to access all endpoints.
---

# Postman Testing
**I exported 2 JSON collections:**
- Casting Website.postman_collection.json for local testing in port 5000.
- Casting Website After Deploying.postman_collection.json for testing it using https://casting-team.herokuapp.com/.
- there are the JWT for the current logins:
	- {{executive_producer}} --> eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdqdHBLZVpXUDZBd25zZGo0U0VPRCJ9.eyJpc3MiOiJodHRwczovL2Rldi03Z28xYmU3aS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhYzQ1YTAyODg3MzQwMDc1ZjAxOGFkIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxMDc2MTE5OCwiZXhwIjoxNjEwODQ3NTk4LCJhenAiOiJrNm5kNFVVdGo5empoWmxYMnlXWmk3SG5DcWVjNmV1NiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.hvE5clGqLJBJCkrAYU4Qb3OpVU9tRTCIew8CBBvCxjCuKeHixLe_7ow9tMDhkDpMBQ0_nb2kocH3PCkxdA09H9nqehkBNv50vh9y2De5Ekh3bGAYAULkS9yJj57zGnV-cryM51zYWhbmFPH93y7sIp1RXoMJeBfPZGYuHtcqPtYxui-KPqakaKcFuG2LpMZPcSRJl1S18kAQuD7UBQ_PLiuL5uvpEsr5CQ6KLnhxASvtdMaekfXX_INfQKFWN_Ojy5W_In1yWRIO3GsN3sZYReoANXfAT9QPQyEXfBJDq7rTalt47k3N9gibcVYSQICaoQcBjw811vJu9UITBuAL7A
	- {{casting_director}} --> eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdqdHBLZVpXUDZBd25zZGo0U0VPRCJ9.eyJpc3MiOiJodHRwczovL2Rldi03Z28xYmU3aS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhYzQ2N2IzYzhmYTcwMDY4ZTYxMTcyIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxMDc2MTQxOSwiZXhwIjoxNjEwODQ3ODE5LCJhenAiOiJrNm5kNFVVdGo5empoWmxYMnlXWmk3SG5DcWVjNmV1NiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.dtIz8stPpf3TJrpr5Kxf-eux8GNlRqWCr26g0NaBStGnejlpvgp3_y7L4kxJpw9oMw6_NslyDkSt9kXEP7TEKB-EfUKiLAh6KhUPi9TgwfB5oVT3fC-T-TeBxNmQTaFKkRhRr6H9j5kaFPFnu5MLCGlnOiLxp45T6atdlF6MQGv1FrCJyjC7feOPgzypQxptgLt23Hp3tE4ytNrHngyeq3nCAnjjkgIna6ASQbrTEIQWsWxK7mbM6t5y_f0ksXkWnnafsFu0ZIaer4egcxYdKa3yMoYHgQLShHwnEU0RqdYg8fHleEa4Ar43c2qaMcPcMyzS0B8VIstBFxo7Pa9imQ.
	- {{casting_assistant}} --> eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdqdHBLZVpXUDZBd25zZGo0U0VPRCJ9.eyJpc3MiOiJodHRwczovL2Rldi03Z28xYmU3aS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZmOGVjZTlhMzNjNjAwMDY4NzFiMmE3IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxMDc2MTQ4MSwiZXhwIjoxNjEwODQ3ODgxLCJhenAiOiJrNm5kNFVVdGo5empoWmxYMnlXWmk3SG5DcWVjNmV1NiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.czsPgrhc7NlHyYSzdCcg7MHw6ruvN6Lq0UG8yx-bXh9NMMxAveG5d-HNF_ugRxS6BgDdMLac9EZiDCIHzWKfzYv9jvr7vSXHi8e73ig4siId-HskyksieCiCHymaxPrV8-v07uUIwHeB1pk-TeLUKJI0A4PtMX9rw_K6YhonpbmZISb7ricF3YP7XUMygEmW1QFTz1j-377wnApsqg3FA299yrfHPnFRYeb23AT7F8EDyl5D7Qrqz7mToyGp_fMOPlziiMMQIRgw_UDjrg32_N_2z7LcK_OLV6ira7ffaQOaP2Sbg9eb6m8XIwsmnLeGBHHmSv8X1rtBP_J_WIrPHA.
---
```Thank you for visiting this page``` 
