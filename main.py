from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import math
import requests
import uvicorn
import httpx

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route to check API status
@app.get("/")
def home():
    return {"message": "API is working!"}

# Function to check if a number is prime
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6  # Skip even numbers
    return True

# Function to check if a number is an Armstrong number
def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

# Function to get a fun fact about the number
async def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}/math?json"
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return data.get("text", f"{n} is an interesting number!")
    except httpx.RequestError:
        return f"{n} is an interesting number!"
    return f"{n} is an interesting number!"

# Function to classify the number
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
        "fun_fact": get_fun_fact(n),
    }


@app.get("/api/classify-number/{number}")
def get_number_info(number: str):
    try:
        num = int(number)
        return classify_number(num)
    except ValueError:
        raise HTTPException(status_code=400, detail={"number": number, "error": True})

# Run FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
