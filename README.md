# Multi-Tenant Backend-as-a-Service Platform

A production-style Backend-as-a-Service (BaaS) platform built with FastAPI, PostgreSQL, and Docker Compose.  
It supports developer authentication, project-based API keys, and tenant isolation.

## Features

- User signup and login with JWT authentication
- Protected developer routes
- `/me` endpoint for authenticated user identity
- Multi-tenant project model
- API key generation per project
- API key rotation
- App-level authentication using `X-API-Key`
- Dockerized backend
- PostgreSQL with Docker Compose
- Environment-based configuration using `.env`
- DB startup retry logic for container readiness
- Health check endpoint

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Docker
- Docker Compose

## Project Structure

```bash
app/
  auth.py
  database.py
  main.py
  models.py
  routes.py
  schemas.py
Dockerfile
docker-compose.yml
requirements.txt
README.md
.gitignore