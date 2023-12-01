#!/bin/bash

for file in currentEmployment policy communication healthInternational industrial public communityLeadership otherProfessional previousEmployment education
do
    pandoc ./parts/$file.md -o tex/parts/$file.tex
done
