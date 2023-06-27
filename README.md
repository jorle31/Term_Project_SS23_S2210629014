A. Setup 

The following will explain how you can set this porject up.

- Installation

To be able to run this project you will need working Python installation. As for the database no further downloads or connections are needed, as this project works with python's own db "SQLite" which comes with your python installation. To install the other project dependencies please simply execute the "requirements.txt" via: `pip install -r requirements.txt`.

- Database

To create the database please simply run the "create_database.py" file located inside the "db" folder. This will create a file "risk.db", also within the "db" folder. This file will house the database. "SQLite" is a local database, meaning that when this file is deleted, the current databse will be gone. With another execute of "create_database.py", however, a new instance can be created.

- Credentials

The last setup step is to load the credentials needed for the APIs to work. For this a folder "credentials" needs to be created at root level. In this folder create a file "credentials.json" and add your keys as key - value pairs:
```json
{
  "OPENAI_API_KEY": "wadwjdi2ej39e37h7f3h3...",
  "SERPAPI_API_KEY": "awdwahdu38e284z32rh3wd...",
  "NEWSAPI_API_KEY": "039939393939393939393...",
  "PINECONE_API_KEY": "921e93ue3jd3d..."
}
```
To add a new API, simply add the key to "credentials.json" and add a new method to the secrets.py to be able to import the API key into the respective file.

B. Run the application

The application is built using Streamlit, a python framework primarily used for scientific visualizations. To run the application run the "app.py" file located at the root of the project.

C. Usage

The application starts out with the default settings. Once feedback is given, the prompts change accordingly. This guarentess, that no two loops result in the same output. This makes the loop truly personalizable.