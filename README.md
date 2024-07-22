# The Pet Sentinel

**How to navigate**
- the backend folder in the root holds the code for the python server
- the rest of the project follows the normal svelte-kit project routing scheme

**How to Install**
1. Clone the repository: `git clone https://github.com/danielp1218/STEMistHacks-3.0.git`
2. cd into the repository: `cd STEMistHacks-3.0`
3. Install front-end dependencies: `npm install`
4. Move the folder named 'backend' into your device of choice (other laptop, raspberry pi, etc.)
5. cd into the backend folder on that device: `cd backend`
6. Create venv: `python -m venv venv`
7. Activate venv: linux: `source venv/bin/activate` windows: `./venv/Scripts/activate`
8. Install dependencies: `pip -r install requirements.txt` (WARNING: the libraries required are very large ~8 GB)
9. Run the backend: `uvicorn main:app --host 0.0.0.0 --port 80`
10. In the frontend, find and replace 192.168.1.103 with your target device ip address (if on local network, if not, use ngrok/expose)
11. initiate the frontend: `npm run build` & `npm run preview`
