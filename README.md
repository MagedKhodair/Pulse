# Pulse

Pulse is a smart consumer application that automatically tracks user purchases, detects price drops, and helps users save money through real-time notifications and intelligent price monitoring. The system combines receipt ingestion, web scraping, and backend automation to provide a unified purchase history and active price tracking service.

## Features
- User account registration and authentication  
- Subscription management and payment processing  
- Service overview and onboarding flow  
- Transaction history retrieval  
- Item-level transaction queries  
- Secure authentication using Firebase / JWT  
- PostgreSQL-backed persistent storage  

### For user testing
To use the Pulse application, users only need:
- A web browser with internet access
- Login FlutterFlow
- Choose the Pulse app
  <img width="1910" height="899" alt="image" src="https://github.com/user-attachments/assets/a46dcba9-59fd-40ce-aa5c-2ec2583ccbb8" />
- View the application in Test Mode using the top right corner flashbolt icon
  <img width="1914" height="908" alt="image" src="https://github.com/user-attachments/assets/e1001929-f9e2-4549-a8d8-bb9015cc3a95" />

### To access the hosted backend service
Please visit: https://pulseapi-csf6duh4bmfad2af.canadacentral-01.azurewebsites.net/docs

## Project Structure

```
Pulse/
├── api.py                # FastAPI routers
├── auth.py               # Authentication and Firebase integration
├── db.py                 # Database connection and query utilities
├── main.py               # FastAPI app entry point
├── schemas.py            # Pydantic models for request/response
├── pyproject.toml        # Project dependencies and metadata
├── README.md             # Project documentation
```

## Requirements
- Python 3.13+
- PostgreSQL database
- Firebase project
- The following Python packages (see `pyproject.toml`):
  - fastapi
  - uvicorn
  - asyncpg
  - email-validator
  - pydantic
  - firebase-admin
  - python-dotenv

## Setup

1. **Clone the repository**  
   ```sh
   git clone <your-repo-url>
   cd Pulse
   ```

2. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```
   Or, if using Poetry:
   ```sh
   poetry install
   ```

3. **Configure environment variables**  
   Create a `.env` file with your database and Firebase settings.

4. **Add Firebase credentials**  
   Place your `serviceAccountKey.json` in the project root.

5. **Run database migrations**  
   (Create tables and schema as needed in your PostgreSQL database.)

6. **Start the application**  
   ```sh
   python main.py
   ```
   Or with Uvicorn:
   ```sh
   uvicorn main:app --reload
   ```

7. **Access the API docs**  
   Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI.

## API Endpoints

- `POST /users/create_profile` - Register a new user
- `GET /users/get_profile` - Get current user profile
- `PATCH /users/membership_status_update` - Update membership status
- `GET /purchases/transaction/{transaction_id}` - Get transaction details
- `GET /purchases/transactions` - List all user transactions
- `GET /purchases/items/{transaction_id}` - List items in a transaction

## License

See [LICENSE](LICENSE) for details.
