![header](https://github.com/RS-Blayten-Jones/Team-White/blob/main/static/header.png)
# All the Buzz  
Joke database application with a RESTful front-end and a NoSQL back-end.
## Overview  
All the Buzz is an API that allows users (and other systems) to store, retrieve, and manage jokes, trivia, bios, and quotes via a REST API. On the back end it uses a NoSQL database; on the front end it exposes endpoints for CRUD operations on content.
## Key Features  
- Store recreational content in a structured NoSQL database (create, read, update, delete)  
- REST API interface for interacting with the content  
- Lightweight and suitable as a starting point for a larger joke / content-library service  
- MIT licensed (see LICENSE file)  
## Getting Started  
### Prerequisites  
- Python (version 3.x)  
- SQL database (e.g., PostgreSQL, MySQL, SQLite) configured and accessible  
- (Optional) Virtual environment tool, e.g., `venv` or `virtualenv`  
### Installation  
1. Clone the repository:  
  ```bash
  git clone https://github.com/RS-Blayten-Jones/Team-White.git
  cd Team-White
2. Set up a virtual environment and install dependencies:
python3 -m venv venv
source venv/bin/activate      # on Linux/Mac
venv\Scripts\activate         # on Windows
pip install -r requirements.txt

3. Configure the database connection (via environment variables, config file, etc). For example:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=teamwhite_jokes
DB_USER=myuser
DB_PASSWORD=mypassword

4. Apply database migrations (if applicable) or run the SQL script to create the necessary tables.
5. Start the application:
python app.py   # or however the entry point is defined
The API should now be running (e.g., at http://localhost:5000).
Usage
Example API Endpoints
• This is for Kassidy :)
Payload Sample
Also for Kassidy

Project Structure (example)
Team-White/
├── THIS IS FOR CHRISTY
├── models.py             # Database models / ORM definitions
├── routes.py             # REST API endpoint definitions
├── static/               # Static files (if any)
├── templates/            # Front-end templates (if any)
├── requirements.txt      # Python dependencies
└── LICENSE
Contributing
Contributions are welcome!
• Fork the repository
• Create a feature branch (git checkout -b feature-yourFeature)
• Commit your changes (git commit -m "Add some feature")
• Push to the branch (git push origin feature-yourFeature)
• Open a Pull Request
Please ensure your code follows the existing style, includes relevant tests (if applicable), and updates documentation accordingly.
Roadmap & TODO
• Add authentication/authorization for jokes API
• Add pagination and filtering (by tag, author)
• Add frontend UI for browsing/adding jokes
• Expand database schema with ratings, categories, user accounts
• Dockerise the application + provide deployment scripts
License
This project is licensed under the MIT License — see the LICENSE file for details.
⸻
Acknowledgements
Thanks to everyone who has contributed.
And a special thanks to Jonathan Earl!!!  
⸻
