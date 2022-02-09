# SaveSailor

Project for Tampere Universities: COMP.SE.610/620 * Spring 2022 * Software Engineering Project 1 &amp; 2

## Installation

### Required packages

- docker
- docker-compose

### Building

Clone the repository and build containers

    git clone https://github.com/kakkurij/SaveSailor.git SaveSailor
    cd SaveSailor
    docker-compose build

## Usage

### Starting database

    docker-compose up database

### Running tests

This starts the database and runs tests

    docker-compose run tests
