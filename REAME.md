# RHG-Server

RHG-Server is a server-side application that provides an interface for parsing and visualizing the RHG (Robot Hacking Game) competition format, as defined by iChunqiu. It currently supports the following APIs:

- `GET /api/get_question_status`: returns the list of all available problems, along with their challengeID, binaryUrl, current_score, vm_ip and question_port.
- `POST /api/sub_answer`: accepts a flag for a given problem, and returns a response indicating whether the flag is correct or not.
- `POST /api/reset_question`: pass in the specified question ID, and then reset the status of the given question.
- `GET /api/machines`: return a list of all machines used in the competition, including their names, corresponding problems, CPU and memory usage information, etc.
- `GET /api/get_ranking`: returns the scoreboard of the competition, showing the scores and rankings of all participants.

## Installation
### Clone and run
To install and run RHG-Server, follow these steps:

Clone the repository to your local machine.
`git clone https://github.com/WinMin/RHG-Server.git`

Install the required packages.
`pip install -r requirements.txt`

Start the server.
`python3 myserver.py --host 127.0.0.1 --port 5001 --user admin --pass admin --download`

### Build Docker
Build the Docker image
`docker build -t rhg-server .`

Start through Docker container
`docker run --rm -p 8080:8080 -v $PWD/chall:/pwn/download --name rhg -it rhg --host 127.0.0.1 --port 5001 --download`

## Usage

Once the server is running, you can access the service by using a browser and going to http://localhost:8080.