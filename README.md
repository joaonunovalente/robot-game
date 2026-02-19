# Robot Game  

A simple **pygame-based arcade game** where you control a robot, collect coins, avoid monsters, and use hearts to restore health.  
The game was built with **pygame**, packaged for the web with **pygbag**, and deployed inside a **Docker container**.  

---

## Features
- Robot character that can move left and right.  
- Falling **coins** to collect for score.  
- **Monsters** to avoid (lose health on collision).  
- **Hearts** to restore lost health.  
- Game states:  
  - **Menu** → Start screen  
  - **Playing** → Core gameplay  
  - **Game Over** → When health reaches 0  
  - **Win** → When all coins are collected  

---

## Installation & Running Locally  

1. Clone the Repository  
```bash
git clone https://github.com/yourusername/robot-game.git
cd robot-game
```

2. Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate

pip install requirements.txt
```

3. Run the Game Locally
```bash
cd deploy && python main.py
```

4. Running in Browser with pygbag

To export and run the game in the browser:
```bash
pygbag main.py
```

This will build the web export inside a folder (usually build/web/).
Open the generated link in your browser to play the game online.

## Docker Deployment

A Dockerfile is included for hosting the game on the web.

1. Build the Docker Image
```bash
docker build -t robot-game .
```
2. Run the Container
```bash
docker run -p 8080:80 robot-game
```

The game will now be available at http://localhost:8000

## Docker Hub Image
The Docker image for this project is available on Docker Hub:
- [DockerHub | JoaoNunoValente/robot-game](https://hub.docker.com/r/joaonunovalente/robot-game)

You can pull and run the image directly using:
```bash
docker pull joaonunovalente/robot-game
docker run -p 8080:80 joaonunovalente/robot-game
```

Then, access [http://localhost:8080](http://localhost:8080)

## Live Demo
The game is live and playable at:
- [robot-game.joaonunovalente.com](http://robot-game.joaonunovalente.com)

This project was developed as the **final project** for the [University of Helsinki | Introduction to Programming course and Advanced Course in Programming](https://programming-25.mooc.fi/).
