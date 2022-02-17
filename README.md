# SaveSailor

Project for Tampere Universities: COMP.SE.610/620 _ Spring 2022 _ Software Engineering Project 1 &amp; 2

## Installation

### Secrets

Rename `empty_secrets.env` to `secrets.env` and add values to keys

### Required packages

- docker
- docker-compose

### Building

Clone the repository and build containers

    git clone https://github.com/kakkurij/SaveSailor.git SaveSailor
    cd SaveSailor
    cp empty_secrets.env secrets.env
    # Add secrets to secrets.env
    docker-compose build

## Usage

### Starting database

    docker-compose up database

### Add excel data to database

    docker-compose run create_database

### Weather data to database

    docker-compose run weather

### Running tests

This starts the database and runs tests

    docker-compose run tests
