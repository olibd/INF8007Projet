# INF8007 Practical Work

## Presentation

The practical sessions will be devoted to the creation of a single project throughout the session.
The goal of the project is to make a script that checks for the presence of a dead link on a website.
To do this, after installing an adequate work environment (session 1),
you will have to find all the links available in a page by web scrapping (session 2).
With this, it will be possible to browse the entire website (session 3).

The second half of the project will increase the usability of the project.
It will be necessary to make the passage of argument possible (session 4).
We can then create a bash script which uses our first script and which allows us to check a website with a Node server and who is installed on a remote git repository (session 5).
The last point will be to revisit our code to transform it into a more functional style (session 6) and finally to add better error handling (session 7).

## Technical specification

The main script can be written in javascript or in python.
Do note that I know javascript more than python, and it will be easier for me to support the first than the second.
I encourage you to use the language you are most comfortable with to spend less time on syntax details and focus on the course material.
The second script, from session 5, must be done in bash.

You should use git during the session with frequent commits and relevant messages. Proper use of git will be checked and evaluated.

The work must be done in teams of 2. In case of an odd number, a team of 3 will be allowed.

The code review will be done individually.

## Evaluation

The first submission will relate to the part planned for sessions 1 to 3. The final submission will assess the entire project.

### First submission (15 points)

 - Web scrapping (5 points)
	- resolves relative links in href.
	- resolves absolute links in href.
	- resolves absolute links in the text.
	- no False negative
	- no false positive
- Web cralling (5 points)
	- Browse the pages of the website
	- Check external links without browsing them
	- Avoid duplicating pages
 - quality of the project (5 points)
	- git
	- consistency in the size of the commits
	- relevant commits message
	- README
		- explains how to use the code
	- Linter
	- code typing
	- comment

### Second submission (30 points)

 - Web scrapping & web cralling (5 points)
 - quality of the project (5 points)
 - argument management (5 points)
 - bash script (5 points)
 - use of functional concept (5 points)
 - error handling (5 points)
 
### Code review (10 points)

- Demonstration of the understanding of the code.
- Demonstration of the understanding of the material seen in class.