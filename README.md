# Django Currency Exchange

A currency conversion web application built with Django, PostgreSQL, and Docker.

## Features

- User registration, login, and logout
- Custom user model (`AbstractBaseUser`) with roles: guest / staff / admin
- Currency conversion (EUR, RUB, USD, BYN) via [apilayer.com](https://apilayer.com) API
- Stores each user's last conversion request and displays it on their profile
- Fully containerized: Docker + docker-compose (Django + Postgres)

## Tech Stack

- **Backend:** Python 3.11, Django 4.2
- **Database:** PostgreSQL 15
- **Infrastructure:** Docker, docker-compose
- **External API:** apilayer.com (Currency Data API)


