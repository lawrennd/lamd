# Teaching Context

The teaching context provides macros for creating educational content like assignments and exercises.

## In-place answer slot

```markdown
\answer{text}{blankheight}
    Prints a worked answer, or leaves blank space of that height in student notes.
    Args:
        text: The lecturer answer (shown in lecturer notes and in all slides)
        blankheight: Height in centimetres for the student writing gap
```

This is not an exercise wrapper. It does not number a question or attach marks. Use it inside existing notes or slides for a derivation that students write in by hand.

Lecturer notes (default) and slides emit `text`. Student notes (`mdpp --student`, or frontmatter `student: true`) emit a blank of `blankheight` cm. Slides keep the answer even when `student` is set, matching lecture-slide sources that always showed worked answers.

`assignment: true` is independent: it selects worksheet chrome and `\writeassignment` numbering, not student blanks.

```markdown
The waiting time in the queue is
\answer{
$$W = \frac{\lambda}{\mu(\mu-\lambda)}.$$
}{6}
```

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
