# WOPED-Wordnet Microservice

This microservice is designed to support the WOPED/Text2Process service. It exposes several endpoints for various WordNet related functionalities like retrieving the base form of a word, checking a word's hypernym tree, and deriving a verb from a noun.
After cloning this repository, it's essential to [set up git hooks](https://github.com/woped/woped-git-hooks/blob/main/README.md#activating-git-hooks-after-cloning-a-repository) to ensure project standards.

## Building the Docker Image

1. Install Docker on your system.
2. Navigate to the directory containing the Dockerfile and your application code.
3. Run `docker build -t wordnet-microservice .` to build the Docker image.

## Running the Docker Container

Run `docker run -p 5000:5000 wordnet-microservice` to start the microservice. The service will be available at `http://localhost:5000`.

## Alternative

Run the `start.sh`. This script builds and runs an instance of the microservice docker container.

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

### POST /check_hypernym_tree

This endpoint accepts a JSON payload with a word, its part of speech, and a list of words to check. It checks whether any of the words in the list is a hypernym of the given word.

#### Parameters:

- `word` - The word for which you want to check the hypernym tree.
- `pos` - The part of speech of the word. It should be one of 'n' (noun), 'v' (verb), 'a' (adjective) or 'r' (adverb).
- `words_to_check` - The list of words to check in the hypernym tree.

#### Example:

Request: `POST /check_hypernym_tree`
Payload: 
```json
{
    "word": "dog",
    "pos": "n",
    "words_to_check": ["mammal", "insect"]
}
```

Response:
```json
{
    "status": "success"
}
```

### POST /derive_verb

This endpoint accepts a JSON payload with a noun, and returns a verb that is derived from the noun.

#### Parameters:

- `word` - The noun from which you want to derive a verb.

#### Example:

Request: `POST /derive_verb`
Payload: 
```json
{
    "word": "communication"
}
```

Response:
```json
{
    "word": "communicate"
}
```

### GET /healthcheck

This endpoint returns a success message if the service is reachable

#### Example:

Request: `GET /healthcheck`

Response:
```json
{
    "Success": "Todo bien"
}
```

Please note that this service uses the WordNet lexical database and the NLTK lemmatizer to process the requests. The returned values are based on the data in WordNet.
