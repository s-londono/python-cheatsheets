# This is the entry point to the webapp. Run the app by: python worldbank.py
# In the Udacity Workspace run:
# env | grep WORK
# URL is: https://{WORKSPACEID}-{PORT}.{WORKSPACEDOMAIN}.com/{ROUTED_PATH}
from .worldbankapp import app

app.run(host='0.0.0.0', port=3001, debug=True)
