import os
import requests
from flask import redirect, render_template, session
from functools import wraps

def login_required(f):
    
    # Decorate routes to require login.

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup(query):
    
    # Search for movies and TV shows using TMDB API.

    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY not set")
        
    url = f"https://api.themoviedb.org/3/search/multi?api_key={api_key}&query={query}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    results = []
    data = response.json()

    for item in data["results"]:
        
        if item["media_type"] in ["movie", "tv"]:
            results.append({
                "tmdb_id": item["id"],
                "title": item.get("title") if item["media_type"] == "movie" else item.get("name"),
                "media_type": item["media_type"],
                "poster": f"https://image.tmdb.org/t/p/w500{item['poster_path']}" if item.get("poster_path") else None,
                "year": item.get("release_date", "")[:4] if item.get("release_date") else (item.get("first_air_date", "")[:4] if item.get("first_air_date") else None)
            })
    return results