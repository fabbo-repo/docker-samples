# Crontab Setup

1. Install requirements

~~~
pip3 install -r requirements.txt
~~~

2. Open crontab editor

~~~
sudo crontab -l
~~~

3. Add task

~~~
0 0 * * 1 cd /<PATH_TO_SCRIPTS>/ && python3 main.py
~~~
