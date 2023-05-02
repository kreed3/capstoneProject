# view at http://127.0.0.1:5000/data
# NO LONGER USED be here in terminal: (venv) (base) Kaitlyns-MacBook-Pro:backend kreed$
# NO LONGER USED virtual env command: source venv/bin/activate

from flask import Flask
from flask_cors import CORS
import data
import json
import numpy as np
from json import JSONEncoder

app = Flask(__name__)
CORS(app)

#had issues w numpy matrices passing through to the server, tried this
#class NumpyArrayEncoder(JSONEncoder):
    #def default(self, obj):
        #if isinstance(obj, np.ndarray):
            #return obj.tolist()
        #return JSONEncoder.default(self, obj)

#sending over server for frontend
@app.get('/data')
def listdata():
    #numpyData = {"array": data.main()}
    EntireDict = data.main()
    #good = datastuff[0]
    #bad = datastuff[1]

    return EntireDict
    #return data.main()
   #return {"programming_languages":list(in_memory_datastore.values())}

if __name__ == '__main__':
    app.run(debug=True)