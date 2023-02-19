# Memfault Firmware Manager

Requirements can be found here: 
https://memfault.notion.site/Memfault-Take-Home-Backend-Engineer-dddd26d8b34440ffbd277eedd4ab99fb

## Solution and Setup

To setup a development environment:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Project source code is under `firmware_manager` folder. I used python 3.11.1, flask-restful and SQLAlchemy to implement the solution.
I used pytest to write unit tests. 
There are 7 unit tests that test various edge cases and happy paths. To run the unit tests:
```
pytest tests
```

To make running the application easier, I used docker-compose to create 2 two containers. One for the application and one for the database.
`db-seed-files` folder contains the seed data for the database. The database is initialized with the seed data when the application starts up.
This has both the schema and some initial test data.
```
docker-compose up
```

After docker-compose is done setting up the containers, the application should be running on port 8880.

I also used postman to manually test the endpoints. I included the postman collection as well hopefully to make the testing easier.
`memfault.postman_collection.json`. You can check out different api keys for different members and devices in the `db-seed-files/init_db.sql`.



## API Endpoints

There are 2 endpoints one GET and one POST. Both endpoints are under the `/firmware/<device_id>` path.

### GET
This endpoint is used to retrieve firmware events for a device. It checks the callers api key and tries to find all events for the `device_id` in the same project as the caller.

### POST
This endpoint is used to upload firmware events. It accepts a json body with the following format:
```
{
    "firmware": "1.0.3",
    "timestamp": "2023-01-01T00:00:00.000000Z",
    "status": "updated"
}
```
`device_id` is retrieved from the path and the `project_id` is retrieved from the caller device's project_id. They are not included in the body.

## Decisions

To explain some of the decisions I made:

- I chose to use SQLAlchemy ORM. Normally for a project this small, I would just use the raw SQL queries with psycopg2 as it would have been simpler 
however since one of the key points was to design the database schema, I thought SQLAlchemy would make it easier look at the models and understand it in one look. Models are located at ``firmware_manager/db/models.py``. You can also check the `init_db.sql` for the create statements.
- I chose to use docker-compose to make it easier to run the application and the database. I believe this just makes it easier to stand up everything and test quickly.
- I wrote my own `auth` decorator to validate the api_key. However, I chose to keep it very simple so there is no encryption or hashing. I just check if the api_key is in the database.
- I am only accepting the api key in the header as `api_key`. I could have added fallbacks to check for it in the query params or the body but I felt that was not necessary for this project.


## Assumptions
- I assumed only devices can upload firmware events and also they can only upload firmware events for themselves.
- I assumed devices and members can only be in one project at a time. In actual world I probably would have designed it differently but in the example schema project ids were singular, so I did not change it.
- I assumed devices can only upload event for their own projects.
- I assumed devices and members can change projects later on. But since requirement is that they can only access their on projects, if a device has old events from a different project, it will not be able to access them.

## Improvements
- I would have liked to add more unit tests but with time constraints I felt this was enough. I only added 1-2 end to end tests and some other edge case tests. 
- Make the authenticaion more secure. I would have liked to add some encryption and hashing to the api_key checks/storing.