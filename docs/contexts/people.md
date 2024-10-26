# People Context

The people context provides macros for displaying and referencing people consistently throughout your documents, particularly useful for team pages, acknowledgments, and author credits.

## Core Macro

```markdown
\circleHead{filename}{alttext}{width}{circleurl}
    Creates circular profile display
    Args:
        filename: Path to image file
        alttext: Alternative text/name
        width: Display width (e.g., "15%")
        circleurl: Optional URL for linking
```

## Generated Person Macros

```markdown
\personnamePicture{width}
    Displays person's circular profile
    Args:
        width: Display width (e.g., "15%")
```

Example usage:
```markdown
\neillawrencePicture{15%}
\carlhenrikekPicture{15%}
```

## Multiple People Display

```markdown
\centerdiv{
    \person1Picture{15%}
    \person2Picture{15%}
    \person3Picture{15%}
}
```

Common use cases:
- Team pages
- Author credits
- Conference committees
- Research group members
