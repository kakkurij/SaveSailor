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
    # Move your excel to data/tehtavat.xlsx
    docker-compose build

## Usage

Start the database, run tests and add all data to database

    docker-compose up --build

## VS Code

These options should be used in addition to user's own settings

```json
{
  "python.linting.flake8Enabled": true,
  "python.linting.enabled": true
}
```
