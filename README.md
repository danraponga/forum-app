

## About project

You can create posts and comments on posts to discuss various topics with other users and share various information.

The main feature for post authors is an AI (Groq) moderator that will respond to comments automatically if you so desire.
The moderator will only respond to comments directly on the post or to replies to the author himself (comments can respond to other comments). The moderator understands the context of the dialogue with each user and responds according to it.

Posts are also checked for obscene language. If it is present, the comment or post will be banned.
The post author can view statistics on total and banned comments for a specified period of time.

## Setup
Clone the project:

```
git clone git@github.com:danraponga/forum-app.git
```

Copy enviroment variables and fill them in `.env`:

```
cp .env.sample .env
```


Go to https://console.groq.com/keys and generate API key for GroqAI or you can try user mine if it works.


Set `AI_PROMPT` in `app.core.config` as you want or leave it as default. The PROMPT serves as system insctruction for AI.


## Run application
Build and run application using Docker:

```
docker compose up --build
```

When containers start, make migrations:

```
docker exec web alembic upgrade head
```


Then run to `https://0.0.0.0:8000/docs/` to use API with Swagger documentation.

And voila :)


## Run tests
To run tests you can use `run_tests.sh` script:
```
chmod +x run_tests.sh

./run_tests.sh
```

Or you can run it manually:
```
pip install pytest

docker compose -f docker-compose.test-db.yml up

pytest app/tests/api/
```

