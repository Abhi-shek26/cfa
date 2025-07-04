# Stock Technical Analysis API

This project is a high-performance backend API for stock technical analysis, built with FastAPI. It features a tiered subscription model, Docker-based deployment, and efficient data processing.

## Architecture Design

### High-Level Component Diagram

The application is containerized using Docker Compose, which orchestrates the different services.

```
+-----------------+      +---------------------+      +---------------------+
|   User Client   |<---->|   FastAPI via     |<---->|  API Service        |
| (Browser/cURL)  |      |   Uvicorn Server    |      |  (Python/FastAPI)   |
+-----------------+      +---------------------+      +---------------------+
                                                          |
                 (Reads stock data)                       | (User/Subscription data)
                                                          |
+--------------------------+                              |
| stocks_ohlc_data.parquet |<-----------------------------+
| (Local file)             |
+--------------------------+                              |
                                                          |
                                                          v
                                                    +---------------------+
                                                    |  PostgreSQL DB      |
                                                    |  (User/Tier Data)   |
                                                    +---------------------+
```

### Technology Justification

*   **FastAPI**: Chosen for its high performance, asynchronous capabilities, and automatic generation of interactive API documentation (Swagger UI), which is ideal for building modern, fast APIs.
*   **Pandas/Pandas-TA**: Used for their powerful and efficient data manipulation and analysis capabilities. `Pandas-TA` simplifies the calculation of technical indicators.
*   **Docker & Docker Compose**: Selected to create a reproducible, isolated, and portable environment. This ensures that the application and its database run consistently across any machine, simplifying setup and deployment.
*   **PostgreSQL**: A robust, open-source relational database ideal for storing structured user and subscription data.
*   **Uvicorn**: A lightning-fast ASGI server, required to run the asynchronous FastAPI application.

### Key Architectural Decisions

*   **Data Loading Strategy**: The `stocks_ohlc_data.parquet` file is loaded into memory on the first request and then cached using Python's `@lru_cache`. This "load-once, read-many" approach drastically reduces I/O and improves response times for subsequent requests.
*   **Subscription Model Implementation**: Tiered access is managed through FastAPI's dependency injection system. A custom dependency authenticates the user via their API key and then a separate function authorizes their access to specific indicators and data date ranges based on their subscription tier.
*   **Scalability**: The application is horizontally scalable. You can run multiple instances of the API container behind a load balancer. The use of a connection-pooled PostgreSQL database also ensures that database connections are managed efficiently under load.
*   **Security**: Authentication is handled via API keys, which are checked against the database for each request. Authorization logic is strictly enforced to prevent users from accessing data outside their subscription plan.

## Setup and Running Instructions (Docker)

These instructions will guide you through setting up and running the project locally using Docker.

### Prerequisites

*   **Docker Desktop**: Ensure you have Docker and Docker Compose installed and running on your system.

### Running the Application

1.  **Clone the Repository**
    ```
    git clone <your-repository-url>
    cd <repository-name>
    ```

2.  **Create the Environment File**
    Create a file named `.env` in the root of the project and copy the contents from `.env.example`. You can modify the default database credentials if you wish.

3.  **Build and Run with Docker Compose**
    Open a terminal in the project root and run the following command:
    ```
    docker-compose up --build
    ```
    This command will build the Docker images and start the FastAPI application and the PostgreSQL database.

4.  **Access the API**
    *   The API will be available at `http://localhost:8000`.
    *   The interactive documentation (Swagger UI) is available at `http://localhost:8000/docs`.

5.  **Test the Tiers**
    *   Use a database tool like pgAdmin or DBeaver to connect to the local PostgreSQL database (host: `localhost`, port: `5432`, credentials from your `.env` file).
    *   Manually add users with different API keys and subscription tiers (`free`, `pro`, `premium`) to the `users` table.
    *   Use the Swagger UI to test the API with the different keys and verify that the permissions and rate limits are working correctly.

## Testing Strategy

Our testing approach combines unit and integration tests to ensure correctness and reliability.

*   **Unit Tests**: These would focus on the pure business logic, primarily the technical indicator calculation functions in `app/services/analysis.py`. Each function would be tested with known input data to verify that the output is mathematically correct.

*   **Integration Tests**: These would be written using a testing framework like `pytest` and FastAPI's `TestClient`. The goal is to test the complete request-response cycle. This includes:
    *   Testing successful authentication with a valid API key.
    *   Testing failed authentication with an invalid key (`401` error).
    *   Testing the authorization logic for each subscription tier (e.g., ensuring a `free` user cannot access a `pro` indicator, resulting in a `403` error).
    *   Verifying that rate limiting works correctly (`429` error).
```

### 3. Leverage and Enhance API Documentation

This deliverable is already mostly complete thanks to FastAPI's powerful features.

*   **Primary Documentation**: Your API documentation is the interactive Swagger UI located at `http://localhost:8000/docs`. This is the deliverable.
*   **Enhance with Examples**: You can make the documentation even better by adding descriptions and examples directly in your code. FastAPI will automatically pick them up.

    **Example in `app/routers/stocks.py`:**
    ```python
    @router.get(
        "/{indicator}/{symbol}",
        response_model=stock_schema.IndicatorResponse,
        summary="Get Technical Indicator Data", # Add a summary
        description="Calculates a technical indicator for a given stock symbol over a date range determined by the user's subscription tier." # Add a description
    )
    def get_indicator_data(
        # ... function parameters
    ):
        # ...
    ```

By following these steps, you will have a complete, well-documented, and professional project that fulfills all the requirements of the assignment.
