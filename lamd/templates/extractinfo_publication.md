{%-assign title=include.entry.title-%}
{%-if include.entry.pdf -%}
{% assign pdf=include.entry.pdf -%}
{%-else-%}
{% assign pdf=false %}
{%-endif-%}
{%-if include.entry.html -%}
{% assign html=include.entry.html -%}
{%-else-%}
{% assign html=false %}
{%-endif-%}
{%-if include.entry.url -%}
{%-capture url-%}
{{ "" | relative_url }}{{include.entry.url}}
{%-endcapture-%}
{%-else-%}
{% assign url=false %}
{%-endif-%}
{%-if include.entry.authors-%}
  {% assign authors=include.entry.authors %}
{%-elsif include.entry.author-%}
  {% assign authors=include.entry.author %}
{%-else-%}
  {% assign authors=false %}
{%-endif-%}
{%-if include.entry.abstract-%}
  {% assign abstract=include.entry.abstract %}
{%-else-%}
  {% assign abstract=false %}
{%-endif-%}
{%-if include.entry.editor-%}
  {% assign editors=include.entry.editor %}
{%-elsif site.editor-%}
  {% assign editors=site.editor %}
{%-else-%}
  {% assign editors=false %}
{%-endif-%}
{%-if include.entry.journal-%}
  {% assign journal=include.entry.journal %}
{%-else-%}
  {% assign journal=false %}
{%-endif-%}
{%-if include.entry.container-title-%}
  {%-assign container-title=include.entry.container-title-%}
{%-elsif site.container-title-%}
  {%-assign container-title=site.container-title-%}
{%-elsif include.entry.booktitle-%}
  {%-assign container-title=include.entry.booktitle-%}
{%-else-%}
  {% assign container-title=false %}
{%-endif-%}
{%-if include.entry.publisher-%}
  {% assign publisher=include.entry.publisher %}
{%-else-%}
  {% assign publisher=false %}
{%-endif-%}
{%-if include.entry.series-%}
  {% assign series=include.entry.series %}
{%-elsif site.series-%}
  {% assign series=site.series %}
{%-else-%}
  {% assign series=false %}
{%-endif-%}
{%-if include.entry.volume-%}
  {% assign volume=include.entry.volume %}
{%-elsif site.volume-%}
  {% assign volume=site.volume %}
{%-else-%}
  {% assign volume=false %}
{%-endif-%}
{%-if include.entry.number-%}
  {% assign number=include.entry.number %}
{%-elsif site.number-%}
  {% assign number=site.number %}
{%-else-%}
  {% assign number=false %}
{%-endif-%}
{%-if include.entry.address-%}
  {% assign address=include.entry.address %}
{%-elsif site.address-%}
  {% assign address=site.address %}
{%-else-%}
  {% assign address=false %}
{%-endif-%}
{%-if include.entry.firstpage-%}
  {% assign firstpage=include.entry.firstpage %}
{%-else-%}
  {% assign firstpage=false %}
{%-endif-%}
{%-if include.entry.lastpage-%}
  {% assign lastpage=include.entry.lastpage %}
{%-else-%}
  {% assign lastpage=false %}
{%-endif-%}
{%-if include.entry.arxiv-%}
  {% assign arxiv=include.entry.arxiv -%}
{%-else-%}
  {% assign arxiv=false %}
{%-endif-%}
{%-if include.entry.doi-%}
  {% assign doi=include.entry.doi -%}
{%-else-%}
  {% assign doi=false %}
{%-endif-%}
{%-if include.entry.software-%}
  {% assign software=include.entry.software %}
{%-else-%}
  {% assign software=false %}
{%-endif-%}
{%-if include.entry.source-%}
  {% assign source=include.entry.source %}
{%-else-%}
  {% assign source=false %}
{%-endif-%}
{%-if include.entry.website-%}
  {% assign website=include.entry.website %}
{%-else-%}
  {% assign website=false %}
{%-endif-%}
{%-if include.entry.openreview-%}
  {% assign openreview=include.entry.openreview %}
{%-else-%}
  {% assign openreview=false %}
{%-endif-%}
{%-if include.entry.supplementary-%}
  {% assign supplementary=include.entry.supplementary %}
{%-else-%}
  {% assign supplementary=false %}
{%-endif-%}
{%-if include.entry.video-%}
  {% assign video=include.entry.video %}
{%-else-%}
  {% assign video=false %}
{%-endif-%}
{%-if include.entry.doi-%}
  {% assign doi=include.entry.doi %}
{%-else-%}
  {% assign doi=false %}
{%-endif-%}
{%-if include.entry.note-%}
  {% assign note=include.entry.note %}
{%-else-%}
  {% assign note=false %}
{%-endif-%}
{%-if include.entry.issued-%}
  {% assign issued=include.entry.issued %}
  {%-if issued.date-parts-%}
    {%-if issued.date-parts.size==1-%}
      {%-capture date-%}{{ issued.date-parts[0] }}-01-01{%-endcapture-%}
    {%-elsif issued.date-parts.size==2-%}
      {%-capture date-%}{{ issued.date-parts[0] }}-{{ issued.date-parts[1] }}-01{%-endcapture-%}
    {%-elsif issued.date-parts.size==3-%}
      {%-capture date-%}{{ issued.date-parts[0] }}-{{ issued.date-parts[1] }}-{{ issued.date-parts[2] }}{%-endcapture-%}
    {%-endif-%}
  {%-else-%}
    {% assign date=issued %}
  {%-endif-%}
{%-elsif include.entry.date-%}
  {% assign date=include.entry.date %}
{%-else-%}
  {% assign date=false %}
{%-endif-%}
{%-if include.entry.layout-%}
  {% assign layout=include.entry.layout %}
{%-else-%}
  {% assign layout=false %}
{%-endif-%}
{%-if include.entry.key-%}
  {% assign id=include.entry.key %}
{% elsif include.entry.id-%}
  {% assign id=include.entry.id | remove_first: '/' %}
{%-else-%}
  {% assign id=false %}
{%-endif-%}
{%if site.style=='pmlr' %}
  {%-capture id-%}
    pmlr-v{{ volume }}-{{ id }}
  {%-endcapture-%}
{%endif%}
