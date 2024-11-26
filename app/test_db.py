from database import fetch_data

def test_connection():
    try:
        # Define a simple query to test the connection
        query = "SELECT * FROM annonce LIMIT 5;"
        data = fetch_data(query)

        # Print the data to confirm connection
        print(data)

        print("Database connection successful!")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    test_connection()
