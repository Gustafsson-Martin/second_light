# Second light

A customizable start page for your browser.
This project is similar to [start.me](https://start.me) but better (or atleast different).

The idea is to have a customizable space where you can add small widgets to it.

## Build
How to build and run this project

### Stage 1
Copy .env.sample into a .env file and **update the variables with your credentials**.

```bash
cp .env.sample .env
```

### Stage 2
Run docker-compose up to start project.

```bash
docker-compose up --build -d
```

### Stopping
Run docker-compose down to stop project.

```bash
docker-compose down
```

## Widget ideas
- TODO-list (shareable between users, have it update for all users when one check-marks an item)
- Website bookmarks
- Stock charts
- Weather
- User supplied background images
- Calendar


## Technical

### Client-side
- [Vue](https://vuejs.org/)
- [TypeScript](https://www.typescriptlang.org/)

### Server-side
- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
- [Supertokens](https://supertokens.com/) - User Authentication
- [Amazon S3](https://aws.amazon.com/s3/) - User supplied image storing
- [MongoDB](https://www.mongodb.com/) - Long term storage of data

## Tools
- [Docker](https://www.docker.com/)
- [Gitlab CI/CD](https://docs.gitlab.com/ee/ci/)
- [Prettier](https://prettier.io/)
- [Material design icons](https://materialdesignicons.com/)
