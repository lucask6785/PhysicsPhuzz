from openai import OpenAI
import asyncio
import time
from functools import lru_cache

# Default value for user query
user_query = "Can you solve this physics problem (F=6 * 8) what is the force?"

# Create a global client
client = OpenAI(api_key="sk-148cbd347b074031b384462738683ee8", base_url="https://api.deepseek.com")

# Cache for storing previous responses
@lru_cache(maxsize=100)
def get_cached_response(query):
    return process_query(query)

def process_query(query):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a physics expert"},
            {"role": "system", "content": "All messages sent through the user will be about physics, apply all problems and solutions through physics"},
            {"role": "system", "content": "Always state the problem with the first words being 'Problem Statement:' , exactly like this, and the solution as 'Solution:' this will be the case every single time."},
            {"role": "system", "content": "Give everything separately, so the problem statement, you should restate the problem in better terms, outlining to the user what the question is and what it is asking. Next you will provide step by step explanation of how to get from the problem the user gives to the solution in a bullet pointed format with indents and tabs to the next line. This problem and step by step solution will be paired together. Next you give the solution, this solution will be by itself and start with the word solution and then indent again, this will be separately looked at not with the problem and step by step solution."},
            {"role": "user", "content": "Hello"},
            {"role": "user", "content": query}
        ],
        stream=False
    )
    return response.choices[0].message.content

async def process_physics_response_async():
    global user_query
    start_time = time.time()

    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(get_cached_response, user_query),
            timeout=10.0  # 10 second timeout
        )
    except asyncio.TimeoutError:
        print("Request timed out. Please try again later.")
        return user_query, "", ""

    problem_and_step_by_step = ""
    solution = ""
    in_solution = False

    lines = response.replace("---", "").replace("*", "×").replace("###", "").replace("\\", "").replace("times", "×").replace("××", "").split('\n')

    for line in lines:
        line = line.strip()
        if line.startswith("Solution:"):
            in_solution = True
            solution = line.replace("Solution:", "").strip() + '\n'
        elif in_solution:
            solution += line + '\n'
        elif line:
            problem_and_step_by_step += line + '\n'

    problem_and_step_by_step = problem_and_step_by_step.strip()
    solution = solution.strip()

    end_time = time.time()
    print(f"Processing time: {end_time - start_time:.2f} seconds")

    print("Problem Statement:", user_query)

    print(problem_and_step_by_step)

    print(solution)

    return user_query, problem_and_step_by_step, solution

def process_physics_response():
    return asyncio.run(process_physics_response_async())

if __name__ == '__main__':
    process_physics_response()

