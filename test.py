import os
import html

file = open(os.getcwd() + "/styles.css", "r")
css = file.read()
file.close()
css = html.unescape(css)
print(css)