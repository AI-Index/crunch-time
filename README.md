**CRUNCH TIME**

This repository contains resources to

- Retrieve US companies from Crunchbase API
- Store retrieved data in a simple relational database.
- Extract plaintext from the websites of listed companies.
- Search for AI-related keywords / phrases in website plaintext

This project is for research purposes as part of the AI Index project, in
compliance with the Research Access policy described on the Crunchbase site. 
Code is shared here so that other with the correct authorization may reproduce 
results. None of the data or access to our API Key is stored in this repository.

**Python Requirements**

`pip install -r requirements.txt`

**SETUP**

If creating the database for the first time, you can run:

```
make build_db 
make add_funding
```

If database has been created but you want to clean / restart it:

```
make reset_db
make add_funding
```

You will need to create a config file with your API Key to run the code here.
Run `make setup_config` and then put your API Key in the generated 
`lib/config.py` file.

NOTE:

Crunchbase describes anything in the "Machine Learning, Predictive Analytics, 
Intelligent Systems, Natural Language Processing, Artificial Intelligence" 
cateogires as being in the super-category of "Artificial Intelligence".

**USAGE**

Review `main.py` and then run it. This will quickly download a list of relevant 
companies and then take 1+ hours to download funding data for each of those
companies.

```
python main.py
```

For quick review of data that has been downloaded to the local Postgresql 
database I recommend a GUI tool such as [PSequel](http://www.psequel.com/) 
(for OSX).
