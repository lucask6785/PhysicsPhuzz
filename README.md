# Physics Visualization Web App

An educational web application that helps students understand physics concepts through interactive formula solving and visualization.

## Features

- Input physics formulas and variables
- Step-by-step solution guide
- Real-time visualization of formulas
- Physics topic identification
- Interactive variable manipulation

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the backend server:
   ```bash
   python main.py
   ```
4. Open the frontend/index.html in your browser

## What is it?
An educational web application that helps students understand physics concepts through interactive formula solving and visualization.

## Inspiration
We are all taking Physics 1 with Calculus at UF and thought we could create a more streamlined approach to understanding fundamental physics concepts. We were confident that we could find better ways to explore and have fun while learning physics.

## How we built it
We built our website using a Flask framework, using Python for the backend and HTML/CSS/JS for the front end. We wanted to ensure we added interactivity and data visualization with a physics engine (Matter JS) while also keeping an easy-to-deploy implementation. We added a database in SQL with Flask in the backend to allow faster retrieval of previous data.

## Challenges we ran into
The hardest part of our design was visualizing the problem after outputting a solution, and especially showing it dynamically on the web. We had initially tried to implement a Python physics engine that we built with Pygame and Pymunk, however, after hours of work, it turned out to not be able to run smoothly on the web. We quickly had to pivot into a solution through a JavaScipt physics engine. It was a frustrating experience as we also became exhausted over time, but our final result turned out to be something we can be proud of, making it a rewarding experience.

## Accomplishments that we're proud of
Designing a functional prototype of the software and working on the entire process for the full 24 hours. We managed to reach most of the expectations that we set, such as including a functional data visualizer that can be modified by the AI, as well as a proper tool to help us have a better experience while working in our Physics course. We managed to exceed our expectations by learning animations and coordinating a workflow to build our website, expanding our knowledge in web development, AI implementation, prompt engineering, and a rewarding teamwork experience.

## What's next for Physics Phuzz
Even more visualizations for harder problems and a more effective UI! We are planning to make it a tool that covers a broader set of exercise solutions and to make it available to all devices! We believe our team did a great job in completing this project but we believe that there is still a lot of potential to improve.
