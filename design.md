# PCRMC Design Document

### MVC pattern
We decided to use an MVC design pattern as follows:

| View | Controller | Model |
|------|------------|-------|
| cli.py: utilizing typer library, communicates with Controller through Contacter instance | pcrmc.py: defines Contacter class, communicates with Model through DatabaseHandler instance | database.py: defines DatabaseHandler class, uses json file to store data |

### Configuration
TODO