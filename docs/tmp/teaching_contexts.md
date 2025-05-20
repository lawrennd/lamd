# Teaching Context

The teaching context provides macros for creating educational content like assignments and exercises.

## Assignment Macros

```markdown
\writeassignment{text}{marks}{answer}
    Creates a written assignment
    Args:
        text: Assignment text
        marks: Points available
        answer: Model answer

\codeassignment{text}{codestub}{marks}{answer}
    Creates a coding assignment
    Args:
        text: Assignment description
        codestub: Starting code
        marks: Points available
        answer: Solution code

\exercise{text}{answerstub}{codestub}
    Creates an exercise
    Args:
        text: Exercise description
        answerstub: Answer template
        codestub: Code template
```

Example usage:
```markdown
\writeassignment{
Explain the backpropagation algorithm.
}{10}{
Backpropagation works by...
}

\codeassignment{
Implement a simple neural network.
}{
def neural_network(X):
    # Your code here
    pass
}{20}{
def neural_network(X):
    return np.dot(X, W) + b
}

\exercise{
Train a linear regression model.
}{
# Steps:
1. Load the data
2. Initialize parameters
}{
import numpy as np
# Your code here
}
```
