# CineTrack 🎬

**CineTrack** is a personal movie and TV tracking web application built with Python and Flask. Search for movies and TV shows, maintain a watchlist, record ratings, and keep track of your viewing history in one place.

## Features

- **User Authentication** — Register, log in, and log out securely.
- **Media Search** — Search for movies and TV shows using The Movie Database (TMDB).
- **Personal Watchlist** — Save titles you want to watch later.
- **Viewing History** — Keep track of watched media and viewing dates.
- **Reviews & Ratings** — Rate movies and shows and write personal reviews.
- **SQLite Database** — Store user accounts, media information, watchlists, and reviews.
- **Session Management** — Maintain user sessions across requests.

## Tech Stack

- **Python** — Backend programming
- **Flask** — Web framework
- **SQLite** — Database
- **TMDB API** — Movie and TV show search and metadata
- **HTML & CSS** — Web interface using Flask templates

## Getting Started

### Prerequisites

- Python 3
- pip
- A TMDB API key
### 1. Clone the Repository

```bash
git clone https://github.com/Strangerfuture/personal.git
cd personal
```

Replace the repository URL and directory with your actual GitHub repository if they differ.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install flask flask-session requests
```

Install any additional dependencies required by your project.

### 4. Configure TMDB

If your `helpers.py` uses the TMDB API, configure your API key as required by that file. Keep API keys and other secrets out of version control.

### 5. Initialize the Database

The application uses SQLite and connects to `personal.db`. Ensure the database schema has been created before running the application. Check your database initialization script for the required tables:

- `users`
- `media`
- `watchlist`
- `reviews`

### 6. Run the Application

```bash
flask --app app run --debug
```

Replace `app` with your Python filename if the main Flask application is stored in a differently named file.

Open `http://127.0.0.1:5000` in your browser.

## How It Works

1. Create an account and log in.
2. Search for movies or TV shows.
3. Add titles to your watchlist or submit a review.
4. View your saved titles, ratings, reviews, and viewing history from the dashboard.

## Project Structure

```text
project/
├── app.py
├── helpers.py
├── personal.db
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── search.html
└── static/
```

*The structure above is illustrative; adjust it to match your actual repository.*

## Security

- Passwords are stored as hashes rather than plain text.
- Parameterized SQL queries are used for database operations.
- Login-required routes restrict access to authenticated users.

For production use, configure a strong Flask secret key, protect state-changing routes against CSRF, and use secure session cookie settings over HTTPS.

## Future Improvements

- Edit and delete reviews.
- Filter and sort watchlists.
- Display detailed media pages.
- Add viewing statistics and personalized recommendations.


Developed by [Strangerfuture](https://github.com/Strangerfuture).
