# Jupyter Notebook Context

The Jupyter notebook context handles interactive code execution and display. It's particularly useful for teaching programming concepts and creating interactive demonstrations.

## Key Macros

### Code Execution
```markdown
\setupcode{block}
    Initializes the environment with imports and setup code
    Args:
        block: Setup code to run first

\code{block}
    Creates a code cell
    Args:
        block: Code to execute

\pythonblockstart
\pythonblockend
    Delimits a Python code block
```

### Code Loading
```markdown
\loadcode{object}{module}
    Imports specific objects from modules
    Args:
        object: Name of object to load
        module: Module to load from

\loadplotcode{object}{filename}
    Loads plotting code from file
    Args:
        object: Name of plotting function
        filename: Source file
```

### Display Control
```markdown
\displaycode{block}
    Shows code without executing
    Args:
        block: Code to display

\plotcode{block}
    Executes plotting code
    Args:
        block: Code that generates plots
```

### Extended Code Controls

```markdown
\setuphelpercode{block}
    Sets up helper code that runs first
    Args:
        block: Setup code

\loadhelpercode{block}
    Loads helper code from file
    Args:
        block: File to load

\helpercode{block}
    Defines helper code
    Args:
        block: Helper code definition

\setupdisplaycode{block}
    Sets up display code
    Args:
        block: Display setup code

\loaddisplaycode{block}
    Loads display code
    Args:
        block: Code to load

\displaycode{block}
    Defines display code
    Args:
        block: Code to display

\setupplotcode{block}
    Sets up plotting code
    Args:
        block: Plot setup code

\loadplotcode{object}{filename}
    Loads plotting code
    Args:
        object: Object to load
        filename: Source file

\plotcode{block}
    Defines plotting code
    Args:
        block: Plot generation code

\matlabcode{block}
    Defines MATLAB code
    Args:
        block: MATLAB code
```

Example usage:
```markdown
\setuphelpercode{
import numpy as np
import matplotlib.pyplot as plt
}

\helpercode{
def process_data(data):
    return np.mean(data, axis=0)
}

\plotcode{
x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))
}
```

## Example Usage

```markdown
\ifndef{gaussianPlot}
\define{gaussianPlot}

\setuphelpercode{
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
}

\helpercode{
def plot_gaussian(mu=0, sigma=1):
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
    y = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2/(2*sigma**2))
    plt.plot(x, y)
    plt.title(f'Gaussian (μ={mu}, σ={sigma})')
}

\plotcode{
plot_gaussian()
}

\endif
```

## Output Formats

- Jupyter notebooks (.ipynb)
- Google Colab notebooks
- Interactive HTML

## Best Practices

1. Always include necessary imports in \setupcode
2. Use meaningful variable names
3. Add comments for complex operations
4. Consider notebook execution order
5. Handle dependencies explicitly
