# $title$
$for(author)$
## $if(author.url)$[$endif$$author.given$ $if(author.prefix)$$author.prefix$ $endif$$author.family$$if author.suffix$ $author.suffix$$if(author.url)$]($author.url$)$endif$
$endfor$
$if(date)$
## $date$
$endif$

$if(abstract)$
**Abstract** "$abstract$"
$endif$

$if(include-before)$
$$$$
$for(include-before)$
$include-before$
$endfor$
$$$$
$endif$

$body$


$for(include-after)$
$include-after$
$endfor$
