# The Comical Commit Classifier

### Introduction
Commit Logs From Last Night (http://www.commitlogsfromlastnight.com/) is an external project that aggregates self-deprecating and/or frustrated commit messages for humorous effect. It seems to do a simple search for keywords (usually curse words) to mark a commit message as good material for the website, but we want to take the method a step further and implement a program that takes commit logs from different repos on GitHub to identify whether the contents are “funny” or “serious” based on more complex criteria. We found a good model online of the implementation of a program that identifies “positive” and “negative” tweets, which we can modify for our own needs. We think the commit logs from GitHub will provide us a challenge, given its lack of proper sentence structure, coding-specific language, and repo-specific language. We have already found a few repositories that we can use as development corpuses, and then we can expand to larger ones for further testing.

### Files
1. raw_log_processor.py --> Given an unaltered file of logs, will strip out all commit, author, and dates. Outputs a file called reponame_commits.txt.
2. manual_annotator.py --> Given a processed file of logs (i.e. that only contains commit messages separated by a newline character), allows the user to manually mark each message as "funny" or "serious" in order to create an answer key for the classifier.
3. naive_classifier.py --> Uses nltk's NaiveBayesClassifier to classify a list of commits. Takes in a processed file of logs (i.e. that only contains commit messages separated by a newline character) and outputs a list of tuples of the form: ` [(“commit message”, “funny”), (“commit message 2”, “serious"), …] `
4. commit_classifier.py --> Our customized classifier that we tweak to give better results than the NaiveBayesClassifier. TBD if this is possible to do within our time frame.
5. scoring.py --> Given an answer key and the output from one of our classifiers, calculates the accuracy of the classifier.

### Steps to Run
##### Prepare your commit logs
1. Navigate to the repo you want to analyze and run
`git log > reponame_raw_logs.txt ; mv reponame_raw_logs.txt [path/to/comical-commit-classifier]/data`. This should save the logs in the proper place. Replace the `[path/to/comical-commit-classifier]` with the path to this repo.
2. Run `python raw_log_processor.py -log "data/reponame_raw_logs.txt"`. This should output a file called `reponame_commits.txt`.

##### Create an answer key
1. Run `python manual_annotator.py -f "data/reponame_commits.txt"`. [Don't do this yet; manual_annotator is still a to-do.]
2. As each commit appears, type `s` for serious and `f` for funny, followed by the return key. For extra fun, think of it like swiping left or right on Tinder.

##### Classify the commits
1. Run`naive_classifier.py -coms "reponame_commits.txt"`. [Don't do this yet; naive_classifer is still a to-do.] This should output something TBD.


### Collaborator Setup
In the terminal, navigate to your preferred directory and run the following commands to set up your environment:
```shell
git clone git@github.com:KatyHerrick/comical-commit-classifier.git
sudo easy_install pip    # get pip in case you don't have it
pip install virtualenv
virtualenv --prompt="(ccc)" env    # make your virtualenv
. env/bin/activate    # activate the env
pip install -r requirements.txt    # install all dependencies
```
This will install all needed packages into a per-project environment so you don't pollute your global environment. If when you run the classifier it tells you that you don't have nltk, you probably just forgot to reactivate your virtualenv.

Every time you start work run:
```shell
. env/bin/activate
git pull
```
This will make sure you have the most up-to-date code locally. :)

Test-driven development is cool, so you'll see a /tests folder. To run the tests, use the command:
```shell
nosetests tests/ -v -s
```
Or to run only one set of tests, replace with `tests/file_name.py`.
