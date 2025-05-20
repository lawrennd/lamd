# Managing People Macros

LAMD provides a system for managing people information and automatically generating the required macros using a Python script.

## Setup

1. Install requirements:
```bash
pip install pyyaml
```

2. Save the macro generator script:
```bash
# In your LAMD root directory
wget https://raw.githubusercontent.com/lawrennd/lamd/main/scripts/create_people_macros.py
chmod +x create_people_macros.py
```

## People Information File

Create a YAML file (`people.yml`) with people information:

```yaml
- name: Neil Lawrence
  image: \diagramsDir/people/neil-lawrence.png
  url: https://inverseprobability.com/
  title: Neil Lawrence

- name: Carl Henrik Ek
  image: \diagramsDir/people/carl-henrik-ek.png
  url: https://carlhenrik.com
  title: Carl Henrik Ek
```

Required fields:
- `name`: Person's full name
- `image`: Path to profile image

Optional fields:
- `url`: Personal webpage
- `title`: Position or title

## Generating Macros

Generate the macros file:
```bash
./create_people_macros.py -i people.yml -o talk-people.gpp
```

Include in your LAMD setup:
```markdown
\include{talk-people.gpp}
```

## Using the Macros

Basic usage:
```markdown
\neillawrencePicture{15%}
```

Multiple people:
```markdown
\centerdiv{
    \neillawrencePicture{15%}
    \carlhenrikekPicture{15%}
}
```

## Best Practices

1. Image Management
   - Use consistent image sizes
   - Store images in `\diagramsDir/people/`
   - Use clear file names

2. Macro Generation
   - Keep YAML file under version control
   - Re-run generator when adding people
   - Test macros after generation

3. Usage Guidelines
   - Use consistent sizing
   - Group related people
   - Include alt text
   - Consider mobile viewing

## Troubleshooting

Common issues and solutions:
- Image not displaying: Check path in YAML
- Macro not found: Ensure generator was run
- Sizing issues: Use percentage widths
