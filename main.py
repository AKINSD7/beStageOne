from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import math
import requests
import uvicorn

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def home():
    return {"message": "API is working!"}



def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True



def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}/math?json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json().get("text", f"{n} is an interesting number!")
    except requests.RequestException:
        pass
    return f"{n} is an interesting number!"

def classify_number(n: int):
    is_armstrong_num = is_armstrong(n)
    is_odd = n % 2 != 0

    if is_armstrong_num and is_odd:
        properties = ["armstrong", "odd"]
    elif is_armstrong_num and not is_odd:
        properties = ["armstrong", "even"]
    elif not is_armstrong_num and is_odd:
        properties = ["odd"]
    else:
        properties = ["even"]

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
