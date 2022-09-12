db = db.getSiblingDB("weatherdata");
db.users.drop();

db.users.insertMany([
    {
        "id": 1,
        "email": "ivanmoreno1998@gmail.com",
        "password": "calabacin",
        "key":"Djdj0skoandinsmoaoju"
    },
    {
        "id": 2,
        "email": "ivanmoreno@gmail.com",
        "password": "calabaza",
        "key":"Djdj0skoandi2c54moaoju"
    }
]);