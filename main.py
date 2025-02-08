from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import math
import requests
import uvicorn

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Root route to check if API is running
@app.get("/")
def home():
    return {"message": "API is working!"}

# Check if a number is prime
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Check if a number is an Armstrong number
def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

# Get fun fact from Numbers API
def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        if response.status_code == 200:
            return response.json().get("text", f"{n} is an interesting number!")
    except requests.RequestException:
        pass
    return f"{n} is an interesting number!"

# Function to classify a number
def classify_number(n: int):
    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    properties.append("odd" if n % 2 != 0 else "even")

    return {
        "number": n,
        "is_prime": is_prime(n),
        "is_perfect": n > 1 and sum(i for i in range(1, n) if n % i == 0) == n,
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(abs(n))),
        "fun_fact": get_fun_fact(n)
    }

# API Endpoint for Classifying Numbers
@app.get("/api/classify-number")
def get_number_info(number: str = Query(..., description="Number to classify")):
    try:
        num = int(number)  # Convert input to integer
        return classify_number(num)  # Return classification result
    except ValueError:
        raise HTTPException(status_code=400, detail={"number": number, "error": True})  # Handle invalid input

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
