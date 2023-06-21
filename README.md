# WOPED-Wordnet Microservice

This microservice is designed to support the WOPED/Text2Process service. It exposes two endpoints: one to retrieve the synonyms of a word, and another to find the base form of a word given its part of speech.

## Building the Docker Image

1. Install Docker on your system.
2. Navigate to the directory containing the Dockerfile and your application code.
3. Run `docker build -t wordnet-microservice .` to build the Docker image.

## Running the Docker Container

Run `docker run -p 5000:5000 wordnet-microservice` to start the microservice. The service will be available at `http://localhost:5000`.

## API Endpoints

### POST /baseform

This endpoint accepts a JSON payload with a word and its part of speech, and returns the base form of the word.

#### Parameters:

- `word` - The word for which you want to find the base form.
- `pos` - The part of speech of the word. It should be one of 'n' (noun), 'v' (verb), 'a' (adjective) or 'r' (adverb).

#### Example:

Request: `POST /baseform`
Payload: 
```json
{
    "word": "running",
    "pos": "v"
}
```
Response:
```json
{
    "word": "run"
}
```

### GET /healthcheck

This endpoints returns a success message if the service is reachable

### Example:

Request: `GET /healthcheck`

Response:
```json
{
    "Success": "Todo bien"
}
```

Please note that this service uses the WordNet lexical database and the NLTK lemmatizer to process the requests. The synonyms and base forms returned by the service are based on the data in WordNet.