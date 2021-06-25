- If you missed the introduction, you can [view it here](introduction.md)
- If you want to return to the README, [press here](../README.md)


After you complete a run of polyga, you can load all polymers that evolved on
your planet. First, import any packages you might want to use to analyze
the results. You'll also need to load sqlite3, as all data is saved in a 
sqlite database.

```Python
from polyga import polygod
import pandas as pd
import numpy as np
from sklearn import preprocessing
import sqlite3
```

Note that the database is saved in a folder named after your planet.

```
.  
+-- script.py  
+-- models  
|   +-- exp_Tg  
|       +-- model.pkl  
|   +-- exp_Eg  
|       +-- model.pkl  
+-- polyland
|   +-- planetary_database.sqlite
```

Next, let's connect to and query the database of our planet.
We can use pandas to easily extract the database as a dataframe.

```Python
conn = sqlite3.connect('polyland/planetary_database.sqlite')
query = "SELECT * FROM planetary_database"
df = pd.read_sql(query, conn)
# Don't forget to close the connection.
conn.close()
```

Now, you can perform an analysis of all polymers you generated. In this case,
we are observing the evolution of the average Tg of polymers over 15
generations.

```Python
for i in range(15):
    tdf = df.loc[df['generation'] == i]
    peptland = tdf.loc[tdf['nation'] == 'Polypeptland']
    mean_tg_pept = peptland['exp_Tg'].mean()
    print("Polymers had an average Tg value of {} for generation {}".format(
          mean_tg_pept, i))
```

The full script is below.

```Python
from polyga import polygod
import pandas as pd
import numpy as np
from sklearn import preprocessing
import sqlite3

conn = sqlite3.connect('polyland/planetary_database.sqlite')
query = "SELECT * FROM planetary_database"
df = pd.read_sql(query, conn)
# Don't forget to close the connection.
conn.close()

for i in range(15):
    tdf = df.loc[df['generation'] == i]
    peptland = tdf.loc[tdf['nation'] == 'Polypeptland']
    mean_tg_pept = peptland['exp_Tg'].mean()
    print("Polymers had an average Tg value of {} for generation {}".format(
          mean_tg_pept, i))
```
