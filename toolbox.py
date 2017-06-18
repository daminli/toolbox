'''
Created on 2017骞�5鏈�19鏃�

@author: lidm1
'''
from toolbox import app

app=app

import sys, locale
print(sys.stdout.encoding, locale.getpreferredencoding ())

if __name__ == '__main__':
    app.run(debug=True)

