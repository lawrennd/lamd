#!/bin/bash

cd parts
pandoc header.md currentEmployment.md policy.md communication.md healthInternational.md industrial.md public.md communityLeadership.md otherProfessional.md previousEmployment.md education.md -o ../cv.docx
cd ..
