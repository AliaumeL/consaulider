## Consolidate sparse data using SAT solver



### Built With

* [Python](https://www.python.org/)
* [MiniSat](http://minisat.se/)
* [Python-sat](https://pysathq.github.io/)
* [Python-aiger](https://github.com/mvcisback/py-aiger)

## Usage

```python

import pandas as pd

from consaulider import (
    df_to_circuit,
    find_example,
    possibilities,
    candidate,
    ConstraintCircuit,
    )


# STEP 1, build some business knowledge

cars = pd.DataFrame([
    ["berline", "EU", "citroen"],
    ["4x4", "US", "citroen"],
    ["4x4", "US", "nissan"],
    ["4x4", "EU", "nissan"],
], columns=["type", "location", "producer"])

themes = pd.DataFrame([
    ["urban life", "berline"],
    ["joyride", "berline"],
    ["country", "4x4"]
], columns=["theme", "type"])

# STEP 2, create the circuit

cc = ConstraintCircuit()

cc.circuit = df_to_circuit(cars, cc.pool) & df_to_circuit(themes, cc.pool)

# STEP 3, ask questions

find_example(cc, cc.pool.atom("type", "4x4") & ~cc.pool.atom("producer", "nissan"))
possibilities(cc, {"producer": ["nissan"] })
candidate(cc, {"producer": ["nissan"] })

```

## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
