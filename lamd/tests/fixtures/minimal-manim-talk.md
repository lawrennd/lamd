---
title: "Minimal Manim Talk"
author:
- family: Test
  given: Author
date: 2026-05-05
---

\newslide{Introduction}{}

\slides{This is a test slide.}

\notes{These are talk notes that should not appear in the slide output.}

\speakernotes{Presenter only: this is a speakernote.}

\newslide{Second Slide}{}

\slides{The quick brown fox jumps over the lazy dog.}

\notes{A longer description that goes in the notes only.}

\slidesincremental{* Item one
* Item two
* Item three}

\fragment{A revealed fragment.}{fade-in}

\slidesmanim{
        # raw manim code only shown in Manim output
        self.play(FadeIn(Text("Manim only")))
}

\htmlmanim{<div class="simulation">interactive widget</div>}{
        self.play(FadeIn(lamd_text(r"""[Manim alt for widget]""")))}

