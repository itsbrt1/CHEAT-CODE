import subprocess
import uuid
import json

from pathlib import Path
from datetime import datetime

PROBLEMS = [
    {
        "id": 1,
        "title": "Add Two Numbers",
        "description": "Read two integers and print their sum.",
        "starter": "a, b = map(int, input().split())\nprint(a+b)",
        "tests": [
            {"input": "2 3", "expected": "5"},
            {"input": "10 20", "expected": "30"}
        ]
    },

    {
        "id": 2,
        "title": "Print Numbers",
        "description": "Print numbers from 0 to 4.",
        "starter": "for i in range(5):\n    print(i)",
        "tests": [
            {
                "input": "",
                "expected": "0\n1\n2\n3\n4"
            }
        ]
    },
    
    {
        "id": 3,
        "title": "Square Number",
        "description": "Read integer n and print square.",
        "starter": "n = int(input())\nprint(n*n)",
        "tests": [
            {"input": "5", "expected": "25"},
            {"input": "8", "expected": "64"}
        ]
    },
    {
        "id": 4,
        "title": "Multiply Two Numbers",
        "description": "Read two integers and print their product.",
        "starter": "",
        "tests": [
            {"input": "2 3", "expected": "6"},
            {"input": "5 5", "expected": "25"}
        ]
    },
    {
        "id": 5,
        "title": "Even or Odd",
        "description": "Print Even if number is even else Odd.",
        "starter": "",
        "tests": [
            {"input": "4", "expected": "Even"},
            {"input": "7", "expected": "Odd"}
        ]
    },

    {
        "id": 6,
        "title": "Maximum Number",
        "description": "Read two numbers and print maximum.",
        "starter": "",
        "tests": [
            {"input": "5 8", "expected": "8"},
            {"input": "10 3", "expected": "10"}
        ]
    },

    {
        "id": 7,
        "title": "Factorial",
        "description": "Print factorial of a number.",
        "starter": "",
        "tests": [
            {"input": "5", "expected": "120"},
            {"input": "3", "expected": "6"}
        ]
    },

    {
        "id": 8,
        "title": "Reverse String",
        "description": "Reverse the given string.",
        "starter": "",
        "tests": [
            {"input": "hello", "expected": "olleh"},
            {"input": "python", "expected": "nohtyp"}
        ]
    },

    {
        "id": 9,
        "title": "Palindrome Number",
        "description": "Check if number is palindrome.",
        "starter": "",
        "tests": [
            {"input": "121", "expected": "Palindrome"},
            {"input": "123", "expected": "Not Palindrome"}
        ]
    },

    {
        "id": 10,
        "title": "Sum of Digits",
        "description": "Print sum of digits.",
        "starter": "",
        "tests": [
            {"input": "123", "expected": "6"},
            {"input": "999", "expected": "27"}
        ]
    },

    {
        "id": 11,
        "title": "Count Vowels",
        "description": "Count vowels in string.",
        "starter": "",
        "tests": [
            {"input": "hello", "expected": "2"},
            {"input": "aeiou", "expected": "5"}
        ]
    },

    {
        "id": 12,
        "title": "Prime Number",
        "description": "Check if number is prime.",
        "starter": "",
        "tests": [
            {"input": "7", "expected": "Prime"},
            {"input": "8", "expected": "Not Prime"}
        ]
    },

    {
        "id": 13,
        "title": "Fibonacci",
        "description": "Print first n Fibonacci numbers separated by space.",
        "starter": "",
        "tests": [
            {"input": "5", "expected": "0 1 1 2 3"},
            {"input": "3", "expected": "0 1 1"}
        ]
    },

    {
        "id": 14,
        "title": "Count Words",
        "description": "Count number of words in sentence.",
        "starter": "",
        "tests": [
            {"input": "hello world", "expected": "2"},
            {"input": "I love python", "expected": "3"}
        ]
    },

    {
        "id": 15,
        "title": "Largest in List",
        "description": "Print largest number from list.",
        "starter": "",
        "tests": [
            {"input": "1 2 3 4 5", "expected": "5"},
            {"input": "9 4 1", "expected": "9"}
        ]
    },

    {
        "id": 16,
        "title": "Sort Numbers",
        "description": "Sort numbers in ascending order.",
        "starter": "",
        "tests": [
            {"input": "3 1 2", "expected": "1 2 3"},
            {"input": "9 7 8", "expected": "7 8 9"}
        ]
    },

    {
        "id": 17,
        "title": "Character Frequency",
        "description": "Print frequency of character a.",
        "starter": "",
        "tests": [
            {"input": "banana", "expected": "3"},
            {"input": "apple", "expected": "1"}
        ]
    },

    {
        "id": 18,
        "title": "Armstrong Number",
        "description": "Check if number is Armstrong.",
        "starter": "",
        "tests": [
            {"input": "153", "expected": "Armstrong"},
            {"input": "123", "expected": "Not Armstrong"}
        ]
    },
    
    
]

DATA = Path("app/data/history.json")
DATA.parent.mkdir(parents=True, exist_ok=True)

SUB_DIR = Path("submissions")
SUB_DIR.mkdir(exist_ok=True)

def get_problems():

    return [
        {
            "id": p["id"],
            "title": p["title"],
            "description": p["description"],
            "starter": p["starter"]
        }

        for p in PROBLEMS
    ]

def get_history():

    if not DATA.exists():
        return []

    return json.loads(DATA.read_text())

def save(problem, status):

    arr = []

    if DATA.exists():

        try:
            arr = json.loads(DATA.read_text())

        except:
            arr = []

    arr.insert(0, {
        "problem": problem,
        "status": status,
        "time": str(datetime.now())
    })

    DATA.write_text(json.dumps(arr, indent=2))

def judge_submission(problem_id, code):

    problem = next(
        (p for p in PROBLEMS if p["id"] == problem_id),
        None
    )

    file = SUB_DIR / f"{uuid.uuid4()}.py"

    file.write_text(code)

    for test in problem["tests"]:

        try:

            result = subprocess.run(
                ["python", str(file)],
                input=test["input"],
                text=True,
                capture_output=True,
                timeout=3
            )

            out = result.stdout.strip()

            if out != test["expected"]:

                save(problem["title"], "Wrong Answer")

                return {
                    "status": "Wrong Answer",
                    "expected": test["expected"],
                    "got": out
                }

        except subprocess.TimeoutExpired:

            save(problem["title"], "Time Limit Exceeded")

            return {
                "status": "Time Limit Exceeded"
            }

    save(problem["title"], "Solved")

    next_problem = None

    for p in PROBLEMS:

        if p["id"] == problem_id + 1:

            next_problem = {
                "id": p["id"],
                "title": p["title"],
                "description": p["description"],
                "starter": p["starter"]
            }

    return {
        "status": "Solved",
        "next_problem": next_problem
    }