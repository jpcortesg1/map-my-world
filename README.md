# Map My World API

A REST API for exploring and reviewing locations by categories, built with FastAPI and Hexagonal Architecture.

## Features

- **Locations Management**: Create, retrieve, and filter locations with geographic coordinates
- **Categories Management**: Create and retrieve location categories (restaurants, parks, museums, etc.)
- **Recommendation System**: Get location-category combinations not reviewed in the last 30 days
- **Hexagonal Architecture**: Clean separation of concerns with domain, application, and infrastructure layers
- **Type Safety**: Full type hints throughout the codebase with mypy compatibility
- **Error Handling**: Centralized error handling with structured responses
- **Logging**: Colored logging with different levels and performance tracking
- **SQLite Database**: Lightweight database with optimized queries and indexes
- **Query Parameters**: Pagination, filtering, and Unicode support
- **Comprehensive Testing**: Automated test suites with curl scripts

## Project Structure

```
map-my-world/
├── README.md
├── requirements.txt
├── pyproject.toml
├── env.example
├── .gitignore
├── test_api.sh              # Comprehensive API test suite
├── test_unicode_params.sh   # Unicode query parameters test
├── scripts/
│   └── init_db.py           # Database initialization script
├── config/
│   ├── __init__.py
│   ├── core.py          # Application configuration
│   ├── database.py      # Database configuration
│   └── dependencies.py  # Dependency injection
└── src/
    ├── __init__.py
    ├── app.py                   # FastAPI application factory
    ├── main.py                  # Application entry point
    ├── run.py                   # Development server script
    ├── shared/
    │   ├── exceptions/          # Error handling
    │   ├── logging/             # Logging configuration
    │   └── middleware/          # HTTP middleware
    └── lib/
        ├── locations/           # Locations module
        ├── categories/          # Categories module
        └── recommendations/     # Recommendations module
```

## Architecture

The application follows **Hexagonal Architecture** (Ports and Adapters) with three main layers:

### Domain Layer
- **Entities**: Core business objects (Location, Category, LocationCategoryReview)
- **Value Objects**: Immutable objects with validation (Coordinates)
- **Repository Interfaces**: Abstract contracts for data access
- **Domain Services**: Business logic and validation

### Application Layer
- **Use Cases**: Application-specific business operations
- **DTOs**: Data transfer objects for layer communication

### Infrastructure Layer
- **ORM Models**: SQLAlchemy models for database persistence
- **Repository Implementations**: Concrete implementations of repository interfaces
- **API Schemas**: Pydantic models for request/response validation
- **Routes**: FastAPI route handlers

## API Endpoints

### Locations
- `POST /api/v1/locations` - Create a new location
- `GET /api/v1/locations` - Get all locations with optional filtering and pagination
- `GET /api/v1/locations/{id}` - Get a specific location by ID

**Query Parameters:**
- `limit` (optional): Number of locations to return (1-100)
- `offset` (optional): Number of locations to skip (default: 0)
- `name` (optional): Filter by location name (partial match, supports Unicode)

### Categories
- `POST /api/v1/categories` - Create a new category
- `GET /api/v1/categories` - Get all categories with optional filtering and pagination

**Query Parameters:**
- `limit` (optional): Number of categories to return (1-100)
- `offset` (optional): Number of categories to skip (default: 0)
- `name` (optional): Filter by category name (partial match, supports Unicode)

### Recommendations
- `GET /api/v1/recommendations` - Get location-category recommendations
- `POST /api/v1/recommendations/mark-reviewed` - Mark a combination as reviewed

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd map-my-world
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your configuration
   ```
   
   **Important:** Make sure to configure your `.env` file based on `env.example`. The application requires these environment variables to run properly.

5. **Create and initialize the database**
   ```bash
   # Option 1: Using the initialization script (recommended)
   python scripts/init_db.py
   
   # Option 2: Manual database creation
   python -c "from config.database import create_tables; create_tables()"
   ```
   
   The initialization script will:
   - Create all database tables with proper indexes
   - Populate the database with sample data (categories and locations)
   - Set up the recommendation system tables

### Running the Application

#### Development Mode
```bash
python src/run.py
```

#### Production Mode
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

The project includes comprehensive test suites to verify API functionality:

### Automated API Test Suite
```bash
# Run the complete API test suite
bash test_api.sh
```

This script will:
- Test all API endpoints (locations, categories, recommendations)
- Verify error handling and validation
- Test pagination and filtering
- Check performance and response times
- Generate a detailed JSON report (`api_test_results.json`)

### Unicode Query Parameters Test
```bash
# Test Unicode and special character support
bash test_unicode_params.sh
```

This script verifies:
- Chinese characters (北京) with URL encoding
- Special characters (Café) with URL encoding
- Combined parameters with pagination

### Manual Testing Examples

#### Test Pagination
```bash
# Get first 3 locations
curl -X GET "http://localhost:8000/api/v1/locations/?limit=3"

# Get locations with offset
curl -X GET "http://localhost:8000/api/v1/locations/?limit=2&offset=2"
```

#### Test Filtering
```bash
# Filter locations by name
curl -X GET "http://localhost:8000/api/v1/locations/?name=Park"

# Filter categories by name
curl -X GET "http://localhost:8000/api/v1/categories/?name=Restaurant"
```

#### Test Unicode Support
```bash
# Chinese characters (URL encoded)
curl -X GET "http://localhost:8000/api/v1/locations/?name=%E5%8C%97%E4%BA%AC"

# Special characters (URL encoded)
curl -X GET "http://localhost:8000/api/v1/categories/?name=Caf%C3%A9"
```

#### Test Recommendations
```bash
# Get recommendations
curl -X GET "http://localhost:8000/api/v1/recommendations"

# Mark as reviewed
curl -X POST "http://localhost:8000/api/v1/recommendations/mark-reviewed" \
  -H "Content-Type: application/json" \
  -d '{"location_id": 1, "category_id": 1}'
```

## Development

### Code Quality Tools

The project uses several tools to maintain code quality:

#### Type Checking
```bash
mypy src/
```

#### Code Formatting
```bash
black src/
isort src/
```

#### Linting
```bash
flake8 src/
```

#### Testing
```bash
pytest --cov=src --cov-report=html
```

### Database Schema

The application uses SQLite with the following tables:

#### locations
- `id` (Primary Key)
- `name` (String, indexed)
- `longitude` (Float)
- `latitude` (Float)
- `description` (Text, optional)
- `created_at` (DateTime)
- `updated_at` (DateTime)

#### categories
- `id` (Primary Key)
- `name` (String, unique, indexed)
- `description` (Text, optional)
- `created_at` (DateTime)
- `updated_at` (DateTime)

#### location_category_reviewed
- `id` (Primary Key)
- `location_id` (Foreign Key to locations)
- `category_id` (Foreign Key to categories)
- `reviewed_at` (DateTime, nullable)
- `created_at` (DateTime)

### Optimized Queries

The recommendation system uses optimized SQL queries with indexes:

```sql
-- Recommended indexes
CREATE INDEX idx_location_category_reviewed_date ON location_category_reviewed(reviewed_at);
CREATE INDEX idx_location_category_reviewed_composite ON location_category_reviewed(location_id, category_id, reviewed_at);

-- Main recommendation query
SELECT 
    l.id as location_id,
    l.name as location_name,
    l.longitude,
    l.latitude,
    c.id as category_id,
    c.name as category_name,
    lcr.reviewed_at
FROM locations l
CROSS JOIN categories c
LEFT JOIN location_category_reviewed lcr 
    ON l.id = lcr.location_id AND c.id = lcr.category_id
WHERE lcr.reviewed_at IS NULL 
    OR lcr.reviewed_at < datetime('now', '-30 days')
ORDER BY 
    lcr.reviewed_at IS NULL DESC,  -- Never reviewed first
    lcr.reviewed_at ASC            -- Then oldest ones
LIMIT 10;
```

## Error Handling

The application uses a centralized error handling system:

### Error Response Format
```json
{
    "status_code": 404,
    "error": "Location not found",
    "details": [
        {
            "field": "location_id",
            "message": "Location with ID 123 does not exist"
        }
    ]
}
```

### Error Types
- **4xx Errors**: BadRequestError, NotFoundError, ConflictError, etc.
- **5xx Errors**: InternalServerError, ServiceUnavailableError, etc.
- **Domain Errors**: LocationNotFoundError, DuplicateLocationError, etc.

## Logging

The application uses structured logging with different levels:

- **DEBUG**: Development information (blue)
- **INFO**: General information, requests/responses (green)
- **WARNING**: Warnings (yellow)
- **ERROR**: Manageable errors (red)
- **CRITICAL**: Critical system errors (bright red)

### Log Format
```
2024-01-01 12:00:00 | INFO     | module:function:line - Message
```

## Configuration

Configuration is managed through environment variables. **Copy `env.example` to `.env` and configure as needed:**

```bash
# Database
DATABASE_URL=sqlite:///./map_my_world.db

# Server
HOST=127.0.0.1
PORT=8000
DEBUG=true

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=colored

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
CORS_CREDENTIALS=true
CORS_METHODS=["*"]
CORS_HEADERS=["*"]
```

## API Examples

### Create a Location
```bash
curl -X POST "http://localhost:8000/api/v1/locations" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Central Park",
    "longitude": -73.935242,
    "latitude": 40.782865,
    "description": "A large urban park in Manhattan"
  }'
```

### Create a Category
```bash
curl -X POST "http://localhost:8000/api/v1/categories" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Parks",
    "description": "Public parks and recreational areas"
  }'
```

### Get Recommendations
```bash
curl -X GET "http://localhost:8000/api/v1/recommendations"
```

### Mark as Reviewed
```bash
curl -X POST "http://localhost:8000/api/v1/recommendations/mark-reviewed" \
  -H "Content-Type: application/json" \
  -d '{
    "location_id": 1,
    "category_id": 1
  }'
```

## Troubleshooting

### Common Issues

1. **Database not found**: Run `python scripts/init_db.py` to create and populate the database
2. **Environment variables missing**: Copy `env.example` to `.env` and configure
3. **Unicode characters in URLs**: Use URL encoding (e.g., `%E5%8C%97%E4%BA%AC` for `北京`)
4. **Port already in use**: Change the port in `.env` or kill the existing process

### Reset Database
```bash
# Remove existing database
rm -f map_my_world.db

# Recreate with sample data
python scripts/init_db.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and code quality checks
5. Submit a pull request

## License

This project is licensed under the MIT License. 