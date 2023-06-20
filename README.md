   ## Rest API for Booking Rooms
Rest Api built with Django Rest Framework. The main functionalities are to save and represent data about rooms and available free time slots to book a room.
Validations are in use while ordering a room.

----

## How to use it
`GET` List of registrated rooms:
```
http://localhost:8000/api/rooms/
```
Parameters: `page_size` , `type` , `search`

Response: http 200
```json
{
    "page": 1,
    "count": 2,
    "page_size": 2,
    "results": [
        {
            "id": 1,
            "name": "Express24",
            "type": "team",
            "capacity": 1
        },
        {
            "id": 2,
            "name": "Metaverse",
            "type": "focus",
            "capacity": 2
        }
    ]
}
```
----
`GET` Room detail:
```
http://localhost:8000/api/rooms/<room id>/
```
Response: http 200
```json
{
    "id": 1,
    "name": "Express24",
    "type": "team",
    "capacity": 1
}
```
Response: http 404
```json
{
    "detail": "Not found."
}
```
----

`GET` List of Available time slots for specific room:
```
http://localhost:8000/api/rooms/<room id>/availability
```
Payload: `date`

Response: http 200
```json
[
    {
        "start": "18-05-2023 09:00:00",
        "end": "18-06-2023 09:00:00"
    },
    {
        "start": "18-06-2023 11:00:00",
        "end": "18-06-2023 11:30:00"
    }
]
```
Response: http 400
```json
{
    "success": false,
    "message": "Invalid date format. Please provide date in the format year-month-day"
}
```

---

`POST` Book the room
```
http://localhost:8000/api/rooms/<room id>/book
```

Payload:
```json
{
  "resident": {
    "username": "Anvar Sanayev",
    "phone_number": "998998065999"
  },
  "start": "19-06-2023 9:30:00",
  "end": "19-06-2023 12:00:00"
}
```

Response: http 201
```json
{
    "resident": {
        "username": "Anvar Sanayev"
    },
    "start": "21-06-2023 09:30:00",
    "end": "21-06-2023 12:00:00"
}
```

Response: http 400
```json
{
    "success": "False",
    "message": "The room is booked for the given time"
}
```

```json
{
    "start": {
        "success": "False",
        "message": "Invalid date format. Please provide date in the format \"day-month-year hour:minute:second\""
    }
}
```

```json
{
    "end": {
        "success": "False",
        "message": "Invalid date format. Please provide date in the format \"day-month-year hour:minute:second\""
    }
}
```

```json
{
    "success": [
        "False"
    ],
    "message": [
        "start date cannot be greater or equal to end date"
    ]
}
```

```json
{
    "success": [
        "False"
    ],
    "message": [
        "starting date and time must be at least one hour later from current time"
    ]
}
```
 















