#!/bin/bash

cd includes
pandoc header.md current_employment.md policy.md communication.md health_international.md industrial.md public.md community_leadership.md other_professional.md previous_employment.md education.md -o ../cv.docx
cd ..
