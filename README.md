# Tic Tac Toe Simulation API

A simple API for simulating a TicTacToe game using FastAPI, SQLModel, Docker, and Pydantic. 
This project uses random for generating random choices with [random API](https://github.com/brendanmaguire/random?tab=readme-ov-file)

### Run
```bash
docker compose up --build
```
Open your browser and navigate to http://localhost:4000/docs to interact with the API.

To run tests
```bash
docker exec -it tic_tac_toe_api pytest
```

Open your browser and navigate to http://localhost:4000/docs to interact with the API.



### Product Roadmap
- [ ] Implement custom board size generation.
- [ ] Enable 2-player gameplay functionality.
- [ ] Integrate Amplitude for user behavior analysis.
- [ ] Develop user account creation feature.

### Tech Roadmap
- [ ] Add retry logic for RandomAPI in case of service unavailability.
- [ ] Transition RandomAPI calls to an asynchronous queue to improve performance.
- [ ] Integrate PostgreSQL or an alternative database for production use.
- [ ] Format API responses with Pydantic
- [ ] Set up Grafana for service monitoring.
- [ ] Add linter.
- [ ] Logging.
- [ ] Set up CI/CD pipes.
- [ ] Makefile
