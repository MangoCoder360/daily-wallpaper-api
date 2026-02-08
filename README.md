# daily-wallpaper-api

A Flask API that provides daily and hourly wallpapers with AI-generated descriptions.

## API Endpoints

### Daily Wallpaper
- **GET** `/api/daily-wallpaper` - Returns the current daily wallpaper (updates once per day)
- **GET** `/api/reset-wallpaper` - Manually resets the daily wallpaper

### Hourly Wallpaper
- **GET** `/api/hourly-wallpaper` - Returns the current hourly wallpaper (updates once per hour)
- **GET** `/api/reset-hourly-wallpaper` - Manually resets the hourly wallpaper

## Response Format

All wallpaper endpoints return JSON in the following format:
```json
{
  "url": "https://images.unsplash.com/...",
  "description": "AI-generated description of the wallpaper"
}
```
