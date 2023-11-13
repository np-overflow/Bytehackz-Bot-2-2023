FROM python:3.10
WORKDIR /bot

# Create the backup directory
RUN mkdir -p /bot/backup

# Copy your application code
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot

# Create the log file
RUN touch /bot/backup/bytehackzbot2.log

CMD python bot.py