# Redash_chatbot_add_on.

The aim of this project is to build a novel Redash chat add-on that our team members can use to extract insight from multiple Redash dashboards and from connected databases using natural language. User queries could be about what is already displayed in the dashboard or questions that require generating SQL query using LLMs to be run against our connected databases.

## Data

The data used for this project is a youtube data that contains the following:

- Video metadata for all videos uploaded in 10 Academy youtube channel
- Time Series viewership metadata for all videos uploaded in in 10 Academy youtube channel
- Time Series comments for all our videos uploaded in in 10 Academy youtube channel
- Time Series transcribed text for selected videos uploaded in 10 Academy youtube channel

## Installation

- Navigate to the redash folder and then follow this redash local installation guide [here](https://github.com/getredash/redash/wiki/Local-development-setup) to setup redash up to the `make up` command
- Before running the redash with `make up` make sure to update the .env file in the redash folder to include this additional entries:
  - OPEN_AI_KEY
  - REDASH_API_KEY
- then run `make up`

## Usage

- Check the notebooks folder for the initial view of the csv data as well as an overview of how we interacted with the redash rest api
- Go to http://localhost:5001 to access redash UI where you'll also find the chatbot

## License

MIT License

## References

- [Llms and Sql](https://blog.langchain.dev/llms-and-sql/)
- [Redash Rest API Docs](https://redash.io/help/user-guide/integrations-and-api/api)
