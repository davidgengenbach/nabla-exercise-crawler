# :)

```
pip3 install -r requirements.txt
cp cookies-example.txt cookies.txt
# Get cookies from chrome:
# 1) Go to the Nabla Aufgabengenerator Site
# 2) Open Chrome developer tools
# 3) Go to 'Resources'
# 4) Go to cookies
# 5) Copy all cookies from there (just mark them and copy)
# 6) Paste them in cookies.txt
python3 crawler.py
python3 update_output.py
# the 'output' folder will hold the data now
# start webserver (npm install -g http-server)
http-server output -o
# Enjoy
```

Currently you can only crawl _B-Tree: Remove_, but it should be easily extendable.
The code is a mess, so feel free to make merge requests with improvements.