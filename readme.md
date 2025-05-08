# set up the script
python3 -m venv venv
source venv/bin/activate   
pip install openai python-dotenv

# OPEN_AI_API_KEY
Find your open ai api key from https://platform.openai.com/settings/organization/api-keys
Create something like this in your ~/.env file
```
OPENAI_API_KEY="xxxx"
```

# Run the script
1. run `source venv/bin/activate` if you havent already
2. save input.csv in the current folder
3. python detect-jd.py 

You should expect to see
```
(venv) 05/8/25|1:45:35  jd-detector  $ python detect-jd.py  
✓ Jobot, LLC: No — Jobot is a staffing and recruiting firm, not a traditional job board. ([salary.com](https://www.sala
✓ Varsity Tutors LLC: No — Provides tutoring services, not a job board.
✓ Dhi Group, Inc.: Yes — Operates job boards for technology professionals.
```

and a output.csv file is created too.

# Tune your prompt
Update the `PROMPT` var with your custom prompt. But remember this script is designed as a one-turn cnoversation with LLM per row from csv.