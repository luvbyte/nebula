

run:
	~/myenv/bin/python3 nebula/main.py

serve:
	cd nebula && ~/myenv/bin/uvicorn main:server --reload
	

install:
	~/myenv/bin/python3 -m pip install -r requirements.txt

