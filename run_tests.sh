#!/bin/bash

DOCKER_COMPOSE_FILE="docker-compose.test-db.yml"

function cleanup {
    docker-compose -f $DOCKER_COMPOSE_FILE down
}

docker-compose -f $DOCKER_COMPOSE_FILE up -d

if [ $? -ne 0 ]; then
    echo "Container running failed"
    exit 1
fi

sleep 5


pytest app/tests/
TEST_RESULT=$?

cleanup

exit $TEST_RESULT
