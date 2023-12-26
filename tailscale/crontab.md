# Crontab Setup

1. Open crontab editor

~~~
sudo crontab -e
~~~

3. Add task

~~~
0 0 * * 1 cd /<PATH_TO_SCRIPTS>/ && python3 scripts/main.py
~~~
