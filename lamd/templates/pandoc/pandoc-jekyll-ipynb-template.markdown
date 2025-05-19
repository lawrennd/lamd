::: {.cell .markdown}
# $title$
$for(author)$
### $if(author.url)$[$endif$$author.given$ $author.family$$if(author.url)$]($author.url$)$endif$$if(author.institute)$, $author.institute$ 

$endif$
$endfor$

$if(date)$
### $date$
$endif$
:::

::: {.cell .markdown}
$if(abstract)$
**Abstract**: $abstract$
$endif$
:::

::: {.cell .markdown}
$$$$
$for(include-before)$
$include-before$
$endfor$
$$$$
:::

::: {.cell .markdown}
$body$

$for(include-after)$
$include-after$
$endfor$

:::
