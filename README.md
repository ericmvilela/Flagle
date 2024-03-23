# Flagle

Test your skills and try to guess the flag of the secret country! With each guess you make, the common colors between the secret flag and the flag you suggested will be revealed, helping you to uncover it. You have a maximum of 6 attempts per day. Good luck!


## Getting Started

Make sure you have Python and pip installed in your environment.

1. Clone the repository:

   ```bash
   git clone https://github.com/ericmvilela/Flagle.git
   ```

2. Create a virtual environment:

   - In Windows
      
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

   - In Linux/Mac
      
      ```bash
      python -m venv venv
      source venv/bin/activate
      ```

3. Install the dependencies:

   `pip install -r requirements.txt`


## Execution

Start the server:

```bash
flask run
```