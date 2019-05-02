# tlimm
Too Large Image for My Model

# usage

```python
import tlimm

width, height = 100, 50
tlimm.Cut(
    input_dir="./input",
    output_dir="./out",
    size=(width, height),
    internal=True,
)
``` 