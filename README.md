# Meet N' Eat
REST API backend for a social application for meeting people based on their food interests.

## API Documentation

### Table of Content
* [Getting Started](#Getting_Started)  
* [User Guide](#User_Guide)  
* [API Reference](#API_Reference)
* [Tutorials](#Tutorials)  
* [SDKs](#SDKs)  


### Getting Started


### User Guide


### API Reference
The MeetNEat API allows you to query data about meal requests, proposals and dates.

#### BASE URL  
All URLs reference here have the following base  
`http://localhost:8080/api/v1`

#### AUTHENTICATION
All HTTP requests to the REST API are protected Basic HTTP authentication or using an API key. 
This can be obtained by creating an account.  
`More on this later`

#### RESOURCES

##### Meal Requests
Retrieve one or all `request` resources.

METHOD `GET`  
QUERY PARAMETERS `token`

URL `/requests`  
Retrieve all available meal requests.

URL `/requests/<request_id>`  
Retrieve the meal request corresponding to that id.

### Tutorials


### SDKs
