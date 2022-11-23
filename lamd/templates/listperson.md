{%-if include.person.website-%}
[
{%-endif-%}
{{ include.person.given }}
{%if-include.person.prefix-%}
{{ include.person.prefix }}
{%-endif-%}
 {{ include.person.family}}
{%-if include.person.suffix-%}
 {{suffix}}
{%-endif-%}
{%-if include.person.website-%}
]({{ website }})
{%-endif-%}