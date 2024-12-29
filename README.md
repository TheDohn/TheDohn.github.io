# Portfolio Reflective Statement:

If you found this repo, there is a good chance it is because I linked to it in
my resume. As a warning, this is all very old work. But rather than actively
steer people away from it, I have added this short reflective statement to
contextualize these projects within my current workflows and knowledge. My
current projects are generally for the company I work for so I can't post them here,
but they are much more innovative and organized - reach out to me if you would like
to discuss! http://www.linkedin.com/in/don-bunk/

If I had the opportunity to refactor these projects:

1) I would organize my projects much better. For starters, I would make a
   clearer entry point for my scripts. With minimal help from a README a new
   user of your code base should be able to find out where to start running your
   code easily. The bulk of a project should generally contain some sort of
   src/, output/, and scratch/ directories, which is further abstracted into
   project-specific sub-directories (for example: utils, pipeline, training,
   experimentation). Finally, variables needed for running scripts should be
   abstracted into env files.

2) I would version control with Git in a more organized way. New features should be
   carefully tested in appropriate feature and development branches before
   merging into a main branch.

3) I would generally avoid notebooks. Notebooks have a place (exploration), but
   that place is not production level code. Moreover production code should
   really only exist as plain text, since that is IDE agnostic, lighter weight,
   and allows a wider range of people to interact with your code base. Finally,
   I would much rather be able to navigate plain text using Vim keybindings than
   organize my code in notebook chunks. Finally, logging and model artifacts
   should be appropriately stored in their own directories and files, not in
   code itself (I have seen people save all sorts of things in notebooks over
   the years).

4) Have pity on my future self and write maintainable code that I can come back
   to a day, week, month, or year later and understand. Generally my approach
   for the most important code is to come back to it ~ 2 days after I wrote it
   and make sure I can still explain it to myself or to someone else. Sometimes
   I will get a little tripped up, which indicates that I need to refactor the
   code to make it maintainable. Nowadays I seriously reflect on whether code is
   maintainable or not before I commit to certain features. I have gone as far
   as to remove features that I am certain will only create problems in the
   future when they need to be updated. Additionally, I strive to write code
   that is appropriately cohesive (appropriately designed modules) and loosely
   coupled (low interdependence between those modules).

5) Use Docker, Conda, and renv to make my code so that anyone can run it
   anywhere at any time. I highly doubt the more complicated code in my
   portfolio would run, let alone give the same results today as it did when I
   first wrote it 6+ years ago.

6) Program defensively and design projects that a robust to updates and bugs.
   For me this manifests in two main ways: First, writing code that unit tests
   incoming data (often from clients), ensuring it has a reasonable number of
   files and/or observations, and has an acceptable number of NULLs, or
   missing values etc. Secondly, I am always on the search for new ways to make
   updating a project itself more defensive. To this end, I make extensive use
   of Git hooks so that bad code or unintentional changes cannot make it into
   production.

Please reach out to me on linked in if you would like to discuss any of the above!











# Data Science Portfolio

Below is a list of projects I have been working on lately with the goal of developing my data science skills. 

__PLEASE NOTE: most of the iPython notebooks are so large enough that they will not display in Github, and you will have to download them to view them.__

## Kaggle Home Credit Default Risk

-[Original Kaggle Competition Description and Data](https://www.kaggle.com/c/home-credit-default-risk)

-[My project](Kaggle_Home_Credit_Default_Risk/) 

Please note that many csv files are beyond GitHubs upload limitations. In order to preserve the project structure as much as possible I uploaded what I could. If there is a csv file missing, it is because it was above the limit. All essential notebooks and code are in the directory.

## Twitter Elections Integrity Archive

-[Twitter Data](https://about.twitter.com/en_us/values/elections-integrity.html#data)

-[My projects](Twitter_Elections_Integrity_Archive/)

## Comparing long-term weather forecasts

-[My project](Comparing_long-term_weather_forecasts/) 

## Bayesian Analysis of NBA data (Boston 17-18 Season)

-[My project](Bayesian_NBA_Analysis/) 
