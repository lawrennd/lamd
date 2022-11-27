{%if person%}{%-include 'extractperson' -%}{% assign person=false%}{%endif%}{{given}} {%if prefix%}{{prefix}} {%endif%}{{family}}{%if suffix %} {{suffix}}{%endif%}
