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
> The MeetNEat API allows you to query data about meal requests, proposals and dates.

#### BASE URL  
All URLs reference here have the following base  
`http://35.202.118.81/api/v1`

#### AUTHENTICATION
> All HTTP requests to the REST API are protected Basic HTTP authentication or using an API key. 
  This can be obtained by creating an account.  
 `More on this later`

#### RESOURCES

##### Meal Requests

Query Parameters

| Name        | Type           | Description  |     
| ------------|:-------------:| :-------------|
| token   | String (required) | A long string for validating HTTP requests. You are given one whenever you login|


Data Parameters

| Name        | Type           | Description  |     
| ------------|:-------------:| :-------------|
| meal_type   | String (required) | Eg, `Pizza`, `Coffee` |     
| meal_time   | String (required) | Eg. `Dinner`, `Lunch`, `Breakfast` |     
| location_string | String (required) | Where the date will be. Eg. `Denver, Colorado`, `Queens, New York`|  
| filled | Boolean. Defaults to False| Indicates whether or not the request has been occupied.|   


| Description of the Resource  | HTTP Method   | Parameters  |     
| ------------|:-------------:| :-------------|
| Retrieve all requests. <br> URL `/requests`| `GET` | *Data* <br> `None` <br><br> *Query* <br> `token` |     
| Retrieve one request. <br> URL `/requests/<request_id>`   | `GET` | *Data* <br> `None` <br><br> *Query* <br> `token` |     
| Submit a `meal request`. <br> URL `/requests`| `POST`| *Data* <br> `meal_type` <br> `meal_time` <br>`location_string`  <br><br> *Query* <br> `token` |  
| Edit a `meal request`. <br> URL `/requests/<request_id>` | `PUT` | *Data* <br>`meal_type` <br> `meal_time` <br> `location_string` <br>`filled`  <br><br> *Query* <br> `token` | 
| Delete a `meal request`. <br> URL `/requests/<request_id>` | `DELETE` | *Data* <br>`None` <br><br> *Query* <br> `token` | 



##### Meal Proposals

##### Meal Dates

### Tutorials


### SDKs
