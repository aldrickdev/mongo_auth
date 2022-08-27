# mongo_auth

This project is a simple API that provides basic Authentication and Authorization.

## Endpoints

`POST /api/v1/user/create` . 
Endpoint used to create a user and returns the users token.


`POST /api/v1/user/token`  
Endpoint used to get a new token from the user credentials provided.


`PUT /api/v1/user/edit`  
Endpoint used to update the users profile details


`GET /api/v1/user/profile`   
Endpoint used to get user details


`PUT /api/v1/user/disable`  
Endpoint used to disable a user

