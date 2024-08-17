# Stock Management Application

## Overview
This Stock Management Application allows users to track and manage stock data. Users can register, log in, and select stocks to monitor their price data. The application fetches stock data from Yahoo Finance and provides an intuitive dashboard for viewing selected stocks.

## Features
- User registration and authentication
- Stock selection and management
- Fetching and displaying stock price data
- API endpoints for stock and user stock data
- Token-based authentication for API access

## Technologies Used
- Django
- Django REST Framework
- PostgreSQL (or your preferred database)
- yfinance (for fetching stock data)
- HTML/CSS/JS for frontend
- Swagger for API documentation

## Installation

### Prerequisites
- Python 3.x
- Docker
- Docker Compose (if applicable)

### Running the Application with Docker

#### Step 1: Clone the Repository
First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/stock-management-app.git
cd stock-management-app
```

#### Step 2: Build the Docker Image
To build the Docker image, run the following command:

```bash
docker build -t stock_management_app .
```

#### Step 3: Run the Docker Container
After building the image, you can run the Docker container:

```bash
docker run -d -p 8000:8000 stock_management_app
```

#### Step 4: Access the Application
Once the container is running, you can access the application by navigating to:

```
http://localhost:8000/
```

### Using Docker Compose (Optional)
If you have a `docker-compose.yml` file, you can use Docker Compose to simplify the process:

1. **Run Docker Compose**:

   ```bash
   docker-compose up
   ```

2. **Access the Application**:

   Navigate to:

   ```
   http://localhost:8000/
   ```

### Traditional Installation Steps (Optional)
If you prefer to run the application without Docker, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stock-management-app.git
   cd stock-management-app
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a PostgreSQL database and update the `DATABASES` setting in `settings.py`.

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at `http://127.0.0.1:8000/`.

## Usage

### User Registration and Login
- Navigate to the home page to register or log in.
- After logging in, you can select stocks to monitor.

### Dashboard
- The dashboard displays selected stocks and their price data.
- You can fetch new stock data by providing the stock symbol, date range, and period.

### API Access
- The application provides RESTful API endpoints for stock data.
- **Important**: The API is accessible at `http://127.0.0.1:8000/api/`, but it is not publicly available without proper authentication.

### Swagger Documentation
- The API is documented using Swagger. Access it at `http://127.0.0.1:8000/swagger/`.
- **Authorization**: To use the API in Swagger, you need to provide a token in the following format:
  ```
  Token <your_token>
  ```
  Replace `<your_token>` with your actual token, which can be generated from the "Generate Token" option in the navbar after logging in.

### Example API Requests
You can access the API using tools like `curl`. Here are some examples:

1. To access the stocks endpoint:
   ```bash
   curl -H "Authorization: Token <your token>" http://localhost:8000/api/stocks/
   ```

2. To access the user stocks endpoint:
   ```bash
   curl -H "Authorization: Token <your token>" http://localhost:8000/api/user-stocks/
   ```

## Acknowledgements
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [yfinance](https://pypi.org/project/yfinance/)
