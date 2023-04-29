# Contributing to wechatGameTool


1. [Getting Involved](#getting-involved)
2. [How To Report Bugs](#how-to-report-bugs)
3. [jQuery UI Coding Standards](#jquery-ui-coding-standards)
4. [Tips For Bug Patching](#tips-for-bug-patching)



## Getting Involved

There are a number of ways to get involved with the development of wechatGameTool. Even if you've never contributed code to an Open Source project before, we're always looking for help identifying bugs, writing and reducing test cases and documentation.

This is the best way to contribute to wechatGameTool. Please read through the full guide detailing [How to Report Bugs](#how-to-report-bugs).



## How to Report Bugs

### Make sure it is a wechatGameTool bug

Many bugs reported to our bug tracker are actually bugs in user code, not in wechatGameTool code. Keep in mind that just because your code throws an error and the console points to a line number inside of wechatGameTool, this does *not* mean the bug is a wechatGameTool.




## Tips For Bug Patching



### Build a Local Copy of jQuery UI

Create a fork of the wechatGameTool repo on github at https://github.com/SpiderFZL/wechatGameTool

Change directory to your project root directory, whatever that might be:

```bash
$ cd /path/to/your/www/root/
```

Clone your wechatGameTool fork to work locally

```bash
$ git clone git@github.com:username/wechatGameTool.git
```

Change directory to the newly created dir wechatGameTool/

```bash
$ cd wechatGameTool
```

Add the wechatGameTool main as a remote. I label mine "upstream"

```bash
$ git remote add upstream git://github.com/SpiderFZL/wechatGameTool.git
```

Get in the habit of pulling in the "upstream" main to stay up to date as wechatGameTool receives new commits

```bash
$ git pull upstream main
```




### Fix a bug from a ticket filed at bugs.jqueryui.com:

**NEVER write your patches to the master branch** - it gets messy (I say this from experience!)

**ALWAYS USE A "TOPIC" BRANCH!** Like so (#### = the ticket #)...

Make sure you start with your up-to-date master:

```bash
$ git checkout main
```

Create and checkout a new branch that includes the ticket #

```bash
$ git checkout -b bug_####

# ( Explanation: this useful command will:
# "checkout" a "-b" (branch) by the name of "bug_####"
# or create it if it doesn't exist )
```

Now you're on branch: bug_####

Determine the file you'll be working in...

Next, open the source files and make your changes

Once you're satisfied with your patch...

Stage the files to be tracked:

```bash
$ git add filename
# (you can use "git status" to list the files you've changed)
```


( I recommend NEVER, EVER using "git add . " )

Once you've staged all of your changed files, go ahead and commit them

```bash
$ git commit -m "Component: Brief description of fix. Fixes #0000 - Ticket description."
```

For a multiple line commit message, leave off the `-m "description"`.

You will then be led into vi (or the text editor that you have set up) to complete your commit message.

Then, push your branch with the bug fix commits to your github fork

```bash
$ git push origin -u bug_####
```

Before you tackle your next bug patch, return to the master:

```bash
$ git checkout main
```


