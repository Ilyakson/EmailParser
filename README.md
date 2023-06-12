# Email Parser
This script is designed to parse incoming and outgoing messages from Outlook using Selenium WebDriver. It can log in to an Outlook account, navigate through the inbox and sent items, and extract relevant information from the messages, such as subject, sender, recipient, text.
## Installation

```shell
git clone https://github.com/Ilyakson/EmailParser.git
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
