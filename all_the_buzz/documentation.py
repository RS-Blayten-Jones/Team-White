"""
Get All Jokes
-------------
**GET** http://localhost:8080/jokes

**Headers:**
    - Authorization: Bearer <token>

**Parameters:**
    - level = 1,2 or 3
    - language

**Returns:**
    Dictonary of all public jokes

    

Create New Joke
---------------

**POST** http://localhost:8080/jokes

**Headers:**
    - Authorization: Bearer <token>

**Request Body (application/json):**
    .. code-block:: javascript

        {
            "level": int,
            "language": str,
            "content": {
                "type": "one_liner" | "qa",
                "text": str,        // required if type == "one_liner"
                "question": str,    // required if type == "qa"
                "answer": str       // required if type == "qa"
            }
        }

**Returns:**
    - Adds joke to public table if manager
    - Adds joke to private table if employee

Update Joke
-----------
**PUT** http://localhost:8080/jokes/<string:joke_id>

**Headers:**
    - Authorization: Bearer <token>

**Request Body (application/json):**
    .. code-block:: javascript

        {
            "level": int,
            "language": str,
            "content": {
                "type": <either "one_liner" or "qa">,
                "text": str (required if "one_liner"),
                "question": str (required if "qa"),
                "answer": str (required if "qa")
                }
        }

**Returns:**
    - If employee, adds new joke record in private table pending
    approval by manager.
    - If manager, updates existing record in private table.

    
Get All Pending Jokes
----------------------
**GET** http://localhost:8080/pending-jokes

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    - If manager, returns all jokes in private table

    
Approve Joke
------------
**POST** http://localhost:8080/jokes/<string:joke-id>/approve

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    - If manager updates or adds joke to public table
    - Deletes joke from private table 
    
Deny Joke
---------
**POST** http://localhost:8080/jokes/<string:joke-id>/deny

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    - If manager, deletes joke from private table

    
Get Random Jokes
----------------
**GET** http://localhost:8080/random-jokes/<int:amount>

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    - The specified amount of random jokes from
    the public table

    
Get All Quotes
--------------
**GET** http://localhost:8080/quotes

**Headers:**
    - Authorization: Bearer <token>

**Parameters:**
    - content 
    - category 
    - language
    - author

**Returns:**
    - Dictonary of all public quotes


Create New Quote
----------------

**POST** http://localhost:8080/quotes

**Headers:**
    - Authorization: Bearer <token>

**Request Body (application/json):**
    .. code-block:: javascript

        {
            "content": str,
            "category": str,
            "author": str,
            "language": str
        }

**Returns:**
    - Adds quote to public table if manager
    - Adds quote to private table if employee

    
Update Quote
------------
**PUT** http://localhost:8080/quotes/<string:quote_id>

**Headers:**
    - Authorization: Bearer <token>

**Request Body (application/json):**
    .. code-block:: javascript

        {
            "content": str,
            "category": str,
            "author": str,
            "language": str
        }

**Returns:**
    If employee, adds new quote record in private table pending
    approval by manager.
    If manager, updates existing record in private table.

    
Get All Pending Quotes
----------------------
**GET** http://localhost:8080/pending-quotes

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    If manager, returns all quotes in private table

    
Approve Quote
-------------
**POST** http://localhost:8080/quotes/<string:quote-id>/approve

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    If manager updates or adds quote to public table
    Deletes quote from private table 
    

Deny Quote
----------
**POST** http://localhost:8080/quotes/<string:quote-id>/deny

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    If manager, deletes quote from private table

Get Random Quotes
-----------------
**GET** http://localhost:8080/random-quotes/<int:amount>

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    - The specified amount of random quotes from
    the public table


Get Short Quote
---------------
**GET** http://localhost:8080/short-quotes/<int:amount>

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    Returns the specified number of quotes shorter than 80 characters


Get Daily Quote
---------------
**GET** http://localhost:8080/daily-quotes

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    Returns the daily quote and updates the last used date

    
Get All Bios
------------
**GET** http://localhost:8080/bios

**Headers:**
    - Authorization: Bearer <token>

**Parameters:**
    - birth_year
    - death_year
    - name
    - summary
    - language

**Returns:**
    Dictonary of all public bios


Create New Bio
--------------

**POST** http://localhost:8080/bios

**Headers:**
    - Authorization: Bearer <token>

**Request Body (application/json):**
    .. code-block:: javascript

        {
            "birth_year": int,
            "death_year": int,
            "name": str,
            "paragraph: str,
            "summary": str,
            "source_url": str,
            "language": str 
        }

**Returns:**
    - Adds bio to public table if manager
    - Adds bio to private table if employee

    
Update Bio
----------
**PUT** http://localhost:8080/bios/<string:bio_id>

**Headers:**
    - Authorization: Bearer <token>

**Request Body (application/json):**
    .. code-block:: javascript

        {
            "birth_year": int,
            "death_year": int,
            "name": str,
            "paragraph: str,
            "summary": str,
            "source_url": str,
            "language": str 
        }

**Returns:**
    If employee, adds new bio record in private table pending
    approval by manager.
    If manager, updates existing record in private table.

    
Get All Pending Bios
--------------------
**GET** http://localhost:8080/pending-bios

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    If manager, returns all bios in private table

    
Approve Bio
-----------
**POST** http://localhost:8080/bios/<string:bio-id>/approve

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    If manager updates or adds bio to public table
    Deletes bio from private table 
    

Deny Bio
--------
**POST** http://localhost:8080/bios/<string:bio-id>/deny

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    If manager, deletes bio from private table


Get Random Bios
---------------
**GET** http://localhost:8080/random-bios/<int:amount>

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    - The specified amount of random bios from
    the public table


Get All Trivia
--------------
**GET** http://localhost:8080/trivia

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    Dictonary of all public trivia

    
Create New Trivia
-----------------

**POST** http://localhost:8080/trivia

**Headers:**
    - Authorization: Bearer <token>

**Parameters:**
    - question
    - answer
    - language

**Request Body (application/json):**
    .. code-block:: javascript

        {
            "question": str,
            "answer": str,
            "language": str
        }

**Returns:**
    - Adds trivia to public table if manager
    - Adds trivia to private table if employee

    
Update Trivia
-------------
**PUT** http://localhost:8080/trivia/<string:trivia_id>

**Headers:**
    - Authorization: Bearer <token>

**Request Body (application/json):**
    .. code-block:: javascript

        {
            "question": str,
            "answer": str,
            "language": str
        }

**Returns:**
    If employee, adds new trivia record in private table pending
    approval by manager.
    If manager, updates existing record in private table.

    
Get All Pending Trivia
----------------------
**GET** http://localhost:8080/pending-trivia

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    If manager, returns all trivia in private table

    
Approve Trivia
--------------
**POST** http://localhost:8080/trivia/<string:trivia-id>/approve

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    If manager updates or adds trivia to public table
    Deletes trivia from private table 
    

Deny Trivia
-----------
**POST** http://localhost:8080/trivia/<string:trivia-id>/deny

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    If manager, deletes trivia from private table


Get Random Trivia
-----------------
**GET** http://localhost:8080/random-trivia/<int:amount>

**Headers:**
    - Authorization: Bearer <token>

**Returns:**
    - The specified amount of random trivia from
    the public table
"""