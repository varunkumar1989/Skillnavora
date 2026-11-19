"""Git and GitHub complete guide. Every terminal block is real output captured by git_capture.py
(git 2.43, fixed dates so hashes are reproducible). GitHub features checked against GitHub docs and changelog, November 2026."""
from md import P, UL, CODE, TERM, TABLE, NOTE, STEPS, MENU, K

CHECKED = "November 2026"
GD = "https://docs.github.com/en"

T1 = {
    "slug": "how-git-works",
    "title": "How Git works: snapshots, commits, branches and the three areas",
    "lead": "The mental model that makes every Git command make sense: snapshots instead of differences, the working folder, staging area and repository, what a commit really contains, and why a branch is only a pointer.",
    "minutes": 18,
    "plain": "Git is a camera for your project folder. Each commit is a photo of every file at that moment, with a caption and a link to the previous photo. A branch is a sticky note that says \"we are here\" on one photo, and it moves forward each time you take a new one.",
    "ideas": [
        ("Repository (repo)", "A project folder plus its full history, stored in a hidden .git folder."),
        ("Commit", "A saved snapshot of the whole project, with an author, date, message and a link to its parent commit."),
        ("Working tree", "The files you see and edit."),
        ("Staging area (index)", "The list of changes you have chosen for the next commit."),
        ("Branch", "A movable name that points to one commit. HEAD tells Git which branch you are on."),
        ("Git vs GitHub", "Git is the free tool on your computer. GitHub is a website that hosts Git repositories and adds pull requests, issues, Actions and more."),
    ],
    "flow": ["Working tree (edit)", "git add", "Staging area", "git commit", "Repository (history)", "git push → GitHub"],
    "body": [
        ("Snapshots, not differences", P("Most people imagine Git stores a list of changes. It actually stores <b>snapshots</b>: each commit points to a full picture of the project. Files that did not change are not copied again; Git simply points to the same stored content. That is why switching branches is fast and why history is reliable.") + P("Every piece of stored content gets an ID (a hash) calculated from the content itself, like <code>5e9b349</code>. If even one character changes, the ID changes, so history cannot be quietly edited.")),
        ("The three areas", TABLE(["Area", "What it is", "Commands that move things"], [
            ["Working tree", "Your files on disk", "edit files; <code>git restore</code> to undo edits"],
            ["Staging area", "Changes chosen for the next commit", "<code>git add</code> to stage; <code>git restore --staged</code> to unstage"],
            ["Repository", "Saved commits in .git", "<code>git commit</code> to save; <code>git log</code> to view"],
        ]) + P("Staging lets you commit only part of your work: fix two bugs, then save them as two clean commits.")),
        ("Look inside a real commit", P("These commands show what Git actually stored for the first commit of a small notes project. A commit points to a <b>tree</b> (the folder), the tree points to <b>blobs</b> (file contents), and the branch file simply holds the latest commit's ID.") + TERM("internals")),
        ("Branches are just pointers", UL([
            "<code>main</code> is a file in .git that contains one commit ID. A new commit on main moves that pointer forward.",
            "Creating a branch creates a new pointer to the same commit. It costs almost nothing, so make branches freely.",
            "<b>HEAD</b> is Git's \"you are here\". Normally it points to a branch (<code>ref: refs/heads/main</code>).",
            "Merging joins two lines of history; when one branch is simply ahead, Git just moves the pointer (a fast-forward).",
        ])),
        ("Where GitHub fits", P("Your computer has the complete repository. GitHub keeps another copy (a <b>remote</b>, usually called <code>origin</code>) so you can back up, share and collaborate. You <code>push</code> commits up, and <code>fetch</code> or <code>pull</code> other people's commits down. Pull requests, reviews, issues and Actions are GitHub features built around that shared copy.")),
    ],
    "mistakes": [
        ("Thinking GitHub and Git are the same", "Git runs on your computer and works offline; GitHub hosts copies and adds collaboration tools."),
        ("Being afraid of branches", "They are just pointers; create one for every change."),
        ("Committing everything at the end of the week", "Commit small, logical steps with clear messages."),
    ],
    "practice": [
        "Draw the three areas on paper and write which command moves a change between each.",
        "In a test repository run git cat-file -p HEAD and find the tree, author and message.",
        "Explain to a friend why a branch costs almost nothing to create.",
    ],
    "quiz": [
        ("Does Git store differences or snapshots?", "Snapshots: each commit points to a full picture of the project; unchanged files are reused, not copied."),
        ("What does the staging area hold?", "The changes you have chosen to include in the next commit."),
        ("What is inside .git/refs/heads/main?", "The ID (hash) of the latest commit on main."),
        ("What is HEAD?", "Git's pointer to where you are, normally the current branch."),
    ],
    "links": [
        ("Pro Git book (free)", "https://git-scm.com/book/en/v2"),
        ("Git internals: objects", "https://git-scm.com/book/en/v2"),
        ("About Git (GitHub docs)", f"{GD}/get-started/using-git/about-git"),
    ],
}

T2 = {
    "slug": "setup",
    "title": "Set up Git and GitHub: install, identity, SSH keys, GitHub CLI and your first repository",
    "lead": "Install Git on Windows, macOS or Linux, set your name and email, create a GitHub account with two-factor authentication, connect with SSH or the GitHub CLI, and create and clone your first repository.",
    "minutes": 20,
    "plain": "Setting up Git is like getting a new bank account: install the app, tell it who you are, prove your identity to the bank (GitHub) with a secure key, then open your first account (repository).",
    "ideas": [
        ("git config", "Saves settings such as your name and email, for one repository or globally."),
        ("SSH key", "A key pair on your computer that proves to GitHub it is you, without typing a password."),
        ("Personal access token", "A password-like token for HTTPS; use fine-grained tokens with an expiry date."),
        ("GitHub CLI (gh)", "GitHub's official command-line tool: sign in, create repositories and pull requests from the terminal."),
        ("Two-factor authentication (2FA)", "A second check (app, passkey or security key) when you sign in. Required for code contributors on GitHub."),
    ],
    "flow": ["Install Git", "git config name + email", "GitHub account + 2FA", "SSH key or gh auth login", "Create repo", "Clone and push"],
    "body": [
        ("Install Git", TABLE(["System", "How"], [
            ["Windows", "Download Git for Windows from git-scm.com and keep the defaults (it includes Git Bash and Git Credential Manager). Or run <code>winget install --id Git.Git -e</code>."],
            ["macOS", "Run <code>git --version</code>; macOS offers to install the Command Line Tools. Or <code>brew install git</code>."],
            ["Linux", "<code>sudo apt install git</code> (Ubuntu/Debian) or <code>sudo dnf install git</code> (Fedora)."],
        ]) + P("Check it worked:") + TERM("version")),
        ("Tell Git who you are", CODE("""git config --global user.name "Your Name"
git config --global user.email "you@example.com"     # use the email on your GitHub account
git config --global init.defaultBranch main
git config --global pull.rebase false                 # or true, if your team prefers rebasing
git config --list --show-origin                       # see every setting and where it came from""", "One-time setup") + NOTE("To keep your email private, use the no-reply address from <b>GitHub Settings, Emails</b> (it looks like 12345+name@users.noreply.github.com).", "tip")),
        ("Create your GitHub account safely", STEPS([
            "Sign up at github.com with a professional username (it appears in your portfolio links).",
            f"Turn on two-factor authentication: {MENU('Settings', 'Password and authentication')}. Use an authenticator app or a passkey, and save the recovery codes.",
            "Add a profile photo, bio and a profile README (a repository named exactly like your username).",
        ])),
        ("Connect with SSH (recommended)", CODE("""ssh-keygen -t ed25519 -C "you@example.com"   # press Enter for the default file, add a passphrase
cat ~/.ssh/id_ed25519.pub                    # copy this PUBLIC key
# GitHub: Settings > SSH and GPG keys > New SSH key > paste > Add
ssh -T git@github.com                        # "Hi <username>! You've successfully authenticated" """, "Create and add an SSH key") + P("Never share the private key (the file without .pub). Use one key per computer, and delete keys for computers you no longer use.")),
        ("Or use the GitHub CLI", CODE("""# install: winget install --id GitHub.cli   |   brew install gh   |   see cli.github.com for Linux
gh auth login                 # choose GitHub.com, HTTPS or SSH, and log in with your browser
gh repo create study-notes --public --clone --add-readme
cd study-notes && git log --oneline""", "Sign in and create a repository from the terminal")),
        ("Your first repository from scratch", P("Here is a real first session: create a folder, start Git, and see what status reports.") + TERM("init") + TERM("first_commit", "Stage and commit (real output)") + P("To put it on GitHub, create an empty repository on github.com (no README), then follow Lesson 5 to add the remote and push.")),
    ],
    "mistakes": [
        ("Commits show the wrong name or email", "Set user.name and user.email globally, and fix a single repository with git config (without --global)."),
        ("Typing your GitHub password in the terminal", "GitHub does not accept account passwords for Git; use SSH, the GitHub CLI, or a token via the credential manager."),
        ("Sharing the private SSH key", "Only the .pub file is shared. If a private key leaks, delete it on GitHub and create a new one."),
    ],
    "practice": [
        "Install Git, set your name and email, and run git config --list --show-origin.",
        "Create an SSH key, add it to GitHub and run ssh -T git@github.com.",
        "Create a public repository called study-notes with gh or the website and clone it.",
    ],
    "quiz": [
        ("Which command sets your name for every repository?", "git config --global user.name \"Your Name\""),
        ("Which part of an SSH key do you paste into GitHub?", "The public key (the .pub file)."),
        ("Why turn on 2FA?", "It protects your account and code; GitHub requires it for code contributors."),
    ],
    "links": [
        ("Install Git", "https://git-scm.com/downloads"),
        ("Set up Git (GitHub docs)", f"{GD}/get-started/getting-started-with-git/set-up-git"),
        ("Connecting to GitHub with SSH", f"{GD}/authentication/connecting-to-github-with-ssh"),
        ("GitHub CLI", "https://cli.github.com"),
        ("Configure two-factor authentication", f"{GD}/authentication/securing-your-account-with-two-factor-authentication-2fa"),
    ],
}

T3 = {
    "slug": "daily-commands",
    "title": "The daily Git loop: status, diff, add, commit, log, .gitignore and restore",
    "lead": "The commands you will type every day, with real output: check what changed, stage, commit with a good message, read history, ignore files that should never be committed, and undo edits.",
    "minutes": 20,
    "plain": "Your daily loop is: look (status, diff), choose (add), save (commit), and look back (log). Run git status whenever you are unsure; it always tells you where you are and what to do next.",
    "ideas": [
        ("git status", "Shows the branch, staged changes, unstaged changes and untracked files."),
        ("git diff", "Shows line-by-line changes not yet staged (add --staged for staged ones)."),
        ("git add", "Stages a file's current content for the next commit."),
        ("git commit -m", "Saves staged changes as a commit with a message."),
        ("git log", "Shows history; --oneline, --graph and --stat make it readable."),
        (".gitignore", "A list of files and folders Git should not track, such as secrets and build output."),
    ],
    "flow": ["git status", "git diff", "git add <files>", "git commit -m \"why\"", "git log --oneline"],
    "body": [
        ("A real day of work", P("Edit a file, create another, check, stage, commit and read history:") + TERM("daily")),
        ("Write commit messages people can use", UL([
            "Start with a verb in the present tense: <i>Add</i>, <i>Fix</i>, <i>Update</i>, <i>Remove</i>.",
            "Say what and why in under about 60 characters: <i>Fix login error when email has capitals</i>.",
            "One logical change per commit. If you need \"and\", consider two commits.",
            "For longer explanations, run <code>git commit</code> without -m and write a blank line then a body.",
        ])),
        ("Ignore what should never be committed", P("Secrets (.env files, keys), dependency folders (node_modules, .venv), build output and editor files belong in <code>.gitignore</code>.") + TERM("gitignore") + CODE("""# .gitignore for a Python or data project
.env
*.key
__pycache__/
.venv/
.ipynb_checkpoints/
data/raw/          # large or private data
*.log
.DS_Store""", "A starter .gitignore") + NOTE("If a secret was ever committed, adding it to .gitignore does not remove it from history. Revoke and rotate the secret immediately, then clean history (see Lesson 6).", "warn")),
        ("Undo edits safely", TERM("restore") + TABLE(["You want to", "Command"], [
            ["Throw away unstaged edits in a file", "<code>git restore file</code>"],
            ["Unstage a file but keep the edits", "<code>git restore --staged file</code>"],
            ["See what you are about to commit", "<code>git diff --staged</code>"],
            ["Stage only parts of a file", "<code>git add -p file</code> (answer y or n per change)"],
        ])),
        ("Read history like a pro", TERM("history") + UL([
            "<code>--author</code> filters by person, <code>-S \"text\"</code> finds commits that added or removed that text.",
            "<code>git blame</code> shows which commit last changed each line.",
            "<code>git show</code> shows one commit's message and changes.",
        ])),
    ],
    "mistakes": [
        ("git add . without looking", "Run git status and git diff first; check nothing secret or huge is included."),
        ("Messages like \"update\" or \"final final\"", "Describe what changed and why."),
        ("Committing a .env file", "Add it to .gitignore before the first commit; if it leaked, rotate the secret."),
    ],
    "practice": [
        "Make three small changes and commit them as three separate commits with clear messages.",
        "Create a .gitignore, add a fake .env and confirm git status ignores it.",
        "Use git log -S to find the commit that added a word you choose.",
    ],
    "quiz": [
        ("What does git diff --staged show?", "The changes that are staged and will go into the next commit."),
        ("Which command throws away unstaged edits to a file?", "git restore <file>"),
        ("Does adding a file to .gitignore remove it from earlier commits?", "No. It only stops tracking new changes; committed secrets must be rotated and history cleaned."),
    ],
    "links": [
        ("Recording changes (Pro Git)", "https://git-scm.com/book/en/v2"),
        ("gitignore templates", "https://github.com/github/gitignore"),
        ("git log reference", "https://git-scm.com/docs"),
    ],
}

T4 = {
    "slug": "branches-merge-conflicts",
    "title": "Branches, merging, conflicts, rebase and stash",
    "lead": "Work on features without breaking main: create and switch branches, fast-forward and three-way merges, read and resolve a real merge conflict, rebase a branch on main, and park unfinished work with stash.",
    "minutes": 25,
    "plain": "A branch is a parallel draft. You write in your draft while main stays clean. Merging copies your finished draft back. A conflict is Git saying \"you and someone else changed the same sentence; you choose the final wording\".",
    "ideas": [
        ("git switch -c", "Creates a new branch and moves to it."),
        ("Fast-forward merge", "When main has no new commits, Git just moves main's pointer to your branch."),
        ("Three-way merge", "When both branches have new commits, Git creates a merge commit joining them."),
        ("Merge conflict", "Both branches changed the same lines; Git marks them and asks you to decide."),
        ("Rebase", "Replays your branch's commits on top of the latest main, for a straight history."),
        ("Stash", "Temporarily shelves uncommitted changes so you can switch tasks."),
    ],
    "flow": ["git switch -c feature/x", "commit work", "git switch main", "git merge feature/x", "resolve conflicts if any", "delete the branch"],
    "body": [
        ("Branch and fast-forward merge", TERM("branch_ff") + P("Because main had no new commits, Git simply moved main forward (\"Fast-forward\"). No merge commit was needed.")),
        ("A real merge conflict, resolved", P("Here both branches changed the first line of README.md. Read the markers, write the final version, then add and commit:") + TERM("conflict") + TABLE(["Marker", "Meaning"], [
            ["<code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code>", "Start of your current branch's version"],
            ["<code>=======</code>", "Divider"],
            ["<code>&gt;&gt;&gt;&gt;&gt;&gt;&gt; feature/title</code>", "End of the incoming branch's version"],
        ]) + UL([
            "Edit the file so it reads exactly as it should, and delete all three marker lines.",
            "<code>git add</code> the file, then <code>git commit</code> to finish the merge. To give up instead, run <code>git merge --abort</code>.",
            "Editors such as VS Code show buttons: Accept Current, Accept Incoming, Accept Both.",
        ])),
        ("Rebase for a straight history", TERM("rebase") + NOTE("Golden rule: rebase only your own branches that nobody else has pulled. Rebasing rewrites commit IDs; never rebase main or a shared branch.", "warn")),
        ("Merge or rebase?", TABLE(["", "Merge", "Rebase"], [
            ["History", "Keeps exactly what happened, with merge commits", "Straight line, easier to read"],
            ["Safety", "Never rewrites commits", "Rewrites your branch's commits"],
            ["Use when", "Joining shared branches, finishing a pull request", "Updating your own feature branch with the latest main"],
        ]) + P("On GitHub you can choose <b>Create a merge commit</b>, <b>Squash and merge</b> (one commit per pull request) or <b>Rebase and merge</b> for each pull request.")),
        ("Stash unfinished work", TERM("stash")),
        ("Branch naming that teams like", UL([
            "<code>feature/signup-otp</code>, <code>fix/cart-total-rounding</code>, <code>docs/readme-setup</code>.",
            "Lowercase, hyphens, short. Include a ticket number if your team uses one: <code>fix/PAY-142-refund-status</code>.",
            "Delete branches after merging: <code>git branch -d name</code> locally; GitHub can delete them automatically.",
        ])),
    ],
    "mistakes": [
        ("Working directly on main", "Create a branch for every change and merge through a pull request."),
        ("Leaving conflict markers in the file", "Search for <<<<<<< before committing; tests should fail if markers remain."),
        ("Rebasing a branch others use", "Merge instead, or agree with the team first."),
    ],
    "practice": [
        "Create two branches that change the same line, merge them, and resolve the conflict.",
        "Rebase a feature branch on main and compare git log --graph before and after.",
        "Stash a half-finished change, fix something on main, then pop the stash.",
    ],
    "quiz": [
        ("When does Git do a fast-forward merge?", "When the target branch has no new commits since the feature branch started, so Git just moves the pointer."),
        ("How do you finish a merge after fixing a conflict?", "git add the fixed files, then git commit (or git merge --abort to cancel)."),
        ("What is the golden rule of rebasing?", "Never rebase commits that other people have already pulled, such as main or shared branches."),
        ("What does git stash do?", "It shelves uncommitted changes so the working tree is clean; git stash pop brings them back."),
    ],
    "links": [
        ("Branching in a nutshell (Pro Git)", "https://git-scm.com/book/en/v2"),
        ("Resolving a merge conflict (GitHub docs)", f"{GD}/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line"),
        ("git rebase reference", "https://git-scm.com/docs"),
    ],
}

T5 = {
    "slug": "github-collaboration",
    "title": "GitHub collaboration: remotes, push and pull, forks, pull requests, reviews and issues",
    "lead": "Connect a local repository to GitHub, push, fetch and pull with real output, contribute through forks and pull requests, review code, track work with issues and Projects, and protect main with rulesets.",
    "minutes": 25,
    "plain": "GitHub is the shared office. Push is taking your finished pages to the office; fetch is checking what colleagues left; a pull request is asking \"please review my pages before we put them in the master copy\".",
    "ideas": [
        ("Remote / origin", "A named link to the GitHub copy of your repository."),
        ("push / fetch / pull", "Send commits up; download others' commits; download and merge into your branch."),
        ("Fork", "Your own copy of someone else's repository, used to propose changes to projects you cannot write to."),
        ("Pull request (PR)", "A request to merge one branch into another, with discussion, reviews and checks."),
        ("Issue", "A tracked task, bug or idea, which a PR can close (\"Fixes #12\")."),
        ("Ruleset / branch protection", "Rules such as \"main needs one approving review and passing checks\"."),
    ],
    "flow": ["branch", "commit", "push", "open pull request", "review + checks", "merge", "pull main"],
    "body": [
        ("Push to GitHub", P("After creating an empty repository on GitHub, add it as <code>origin</code> and push. A local bare repository stands in for GitHub here so you can see real output; with GitHub the URL looks like <code>git@github.com:you/notes.git</code>.") + TERM("push")),
        ("Get a teammate's work: fetch, then pull", TERM("clone_pull") + P("<code>git fetch</code> downloads safely without changing your files; <code>git status -sb</code> shows you are behind; <code>git pull --ff-only</code> updates only if no merge is needed, which avoids surprise merge commits.")),
        ("The pull request workflow", STEPS([
            "Create a branch: <code>git switch -c fix/typo-in-readme</code>.",
            "Commit your change and push the branch: <code>git push -u origin fix/typo-in-readme</code>.",
            "On GitHub select <b>Compare &amp; pull request</b> (or run <code>gh pr create --fill</code>). Write what changed, why, and how you tested it. Link the issue with <i>Fixes #12</i>.",
            "Reviewers comment line by line, suggest changes, then <b>Approve</b> or <b>Request changes</b>. Automated checks (GitHub Actions) run on every push.",
            "Push more commits to the same branch to address feedback; the PR updates automatically.",
            "Merge with the method your team uses, delete the branch, and run <code>git switch main &amp;&amp; git pull</code>.",
        ])),
        ("Contribute to someone else's project", STEPS([
            "Select <b>Fork</b> on the project's GitHub page to make your copy.",
            "Clone your fork, and add the original as <code>upstream</code>: <code>git remote add upstream https://github.com/owner/project.git</code>.",
            "Keep in sync: <code>git fetch upstream</code> then <code>git merge upstream/main</code> (or use <b>Sync fork</b> on GitHub).",
            "Branch, commit, push to your fork, and open a pull request to the original repository. Read its CONTRIBUTING.md first.",
        ])),
        ("Good reviews and good pull requests", TABLE(["Author", "Reviewer"], [
            ["Small PRs (under ~300 lines changed) with a clear title", "Review within a day; start with the description and tests"],
            ["Explain why, link the issue, add screenshots for UI", "Ask questions rather than demand; separate must-fix from nice-to-have"],
            ["Run tests and lint before asking", "Use <b>suggested changes</b> for small fixes the author can accept in one click"],
        ])),
        ("Issues, Projects and protecting main", UL([
            "<b>Issues</b>: one per bug or task, with labels (bug, enhancement, good first issue) and an assignee. Templates help reporters give the right details.",
            "<b>Projects</b>: boards and tables that track issues and PRs across repositories, with custom fields such as priority and sprint.",
            f"<b>Rulesets</b> ({MENU('Settings', 'Rules', 'Rulesets')}) or branch protection: require pull requests, at least one approval, passing status checks and no force pushes on main.",
            "<b>CODEOWNERS</b>: a file that automatically requests reviews from the right people for each folder.",
        ])),
    ],
    "mistakes": [
        ("git pull creating messy merge commits", "Fetch first, or use git pull --ff-only; rebase your own branch on main when needed."),
        ("Huge pull requests", "Split work into small PRs that each do one thing."),
        ("Pushing directly to main", "Protect main with a ruleset that requires pull requests and checks."),
    ],
    "practice": [
        "Push a project to GitHub and open a pull request from a branch, even if you review it yourself.",
        "Fork a public repository, sync it with upstream, and open a small documentation PR.",
        "Create a ruleset on your own repository that requires a pull request for main.",
    ],
    "quiz": [
        ("What is the difference between fetch and pull?", "fetch downloads commits without changing your files; pull fetches and then merges (or rebases) into your branch."),
        ("Why add an upstream remote to a fork?", "To fetch new commits from the original project and keep your fork in sync."),
        ("What does \"Fixes #12\" in a PR description do?", "It links the PR to issue 12 and closes the issue when the PR is merged into the default branch."),
    ],
    "links": [
        ("About pull requests", f"{GD}/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests"),
        ("Fork a repository", f"{GD}/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo"),
        ("About rulesets", f"{GD}/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets"),
        ("GitHub Projects", f"{GD}/issues/planning-and-tracking-with-projects"),
    ],
}

T6 = {
    "slug": "undo-mistakes",
    "title": "Undo anything safely: amend, reset, revert, reflog and leaked secrets",
    "lead": "Fix the last commit message, take back a commit you have not shared, undo a commit that is already on GitHub, recover \"lost\" work with the reflog, and what to do when a password is committed.",
    "minutes": 20,
    "plain": "Git almost never loses work. Before you share commits, you can rewrite them freely. After you share them, you add a new commit that undoes the old one, so nobody's copy breaks.",
    "ideas": [
        ("git commit --amend", "Replaces the last commit (message or content). Only for commits not yet pushed."),
        ("git reset --soft / --mixed / --hard", "Moves the branch back; soft keeps changes staged, mixed keeps them in files, hard discards them."),
        ("git revert", "Creates a new commit that undoes an earlier one. Safe for shared history."),
        ("git reflog", "Git's diary of where HEAD has been; finds commits after a bad reset."),
        ("Force push", "Overwrites the remote branch. Use --force-with-lease, and never on shared branches."),
    ],
    "flow": ["Pushed already?", "No → amend / reset", "Yes → revert", "Lost something? → reflog", "Secret leaked → rotate first"],
    "body": [
        ("Which undo do I need?", TABLE(["Situation", "Command", "Safe after push?"], [
            ["Typo in the last commit message", "<code>git commit --amend -m \"...\"</code>", "No"],
            ["Forgot a file in the last commit", "<code>git add file &amp;&amp; git commit --amend --no-edit</code>", "No"],
            ["Undo the last commit but keep the work", "<code>git reset --soft HEAD~1</code>", "No"],
            ["Undo a commit that is on GitHub", "<code>git revert &lt;commit&gt;</code>", "Yes"],
            ["Get back a commit after a bad reset", "<code>git reflog</code>, then <code>git reset --hard HEAD@{n}</code>", "Local fix"],
            ["Discard all local changes", "<code>git restore .</code> (or <code>git reset --hard</code>)", "Local only; cannot be undone"],
        ])),
        ("Fix the last commit message", TERM("amend")),
        ("Reset: soft, mixed and hard", TERM("reset") + UL([
            "<b>--soft</b>: the commit is gone, its changes stay staged.",
            "<b>--mixed</b> (default): changes stay in your files but are unstaged.",
            "<b>--hard</b>: changes are discarded. Check git status and git stash first.",
        ])),
        ("Undo a pushed commit with revert", TERM("revert") + P("Revert adds a new commit, so teammates simply pull it. History stays honest: the mistake and its fix are both visible.")),
        ("Recover \"lost\" commits with reflog", TERM("reflog") + NOTE("The reflog is local and entries expire after weeks or months. Recover soon after the mistake.", "info")),
        ("You committed a password or API key", STEPS([
            "<b>Revoke and rotate</b> the secret first (create a new key, delete the old one). Assume it is already copied.",
            "Remove it from the code, move it to an environment variable or secret store, and add the file to .gitignore.",
            "If it reached GitHub, clean the history with <code>git filter-repo</code> or the BFG tool, force-push with care, and ask collaborators to re-clone.",
            "Turn on GitHub <b>secret scanning</b> and <b>push protection</b> so pushes containing known secret formats are blocked.",
        ])),
    ],
    "mistakes": [
        ("Amending or resetting commits already pushed to a shared branch", "Use git revert instead."),
        ("git reset --hard with uncommitted work you wanted", "Run git status first; stash if unsure."),
        ("Thinking deleting a secret in a new commit is enough", "It stays in history; rotate it and clean history."),
        ("git push --force on main", "Protect main; if you must overwrite your own branch, use --force-with-lease."),
    ],
    "practice": [
        "Make a commit with a typo in the message and fix it with --amend.",
        "Make a commit, reset --soft, then recommit it differently.",
        "Do a reset --hard on purpose in a test repo and recover with reflog.",
    ],
    "quiz": [
        ("Which undo is safe for commits already on GitHub?", "git revert, because it adds a new commit instead of rewriting history."),
        ("What is the difference between reset --soft and --hard?", "--soft keeps the changes staged; --hard discards them."),
        ("What is the first step after committing a secret?", "Revoke and rotate the secret, because it may already be copied."),
    ],
    "links": [
        ("Undoing things (Pro Git)", "https://git-scm.com/book/en/v2"),
        ("Removing sensitive data (GitHub docs)", f"{GD}/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository"),
        ("Push protection", f"{GD}/code-security/secret-scanning/introduction/about-push-protection"),
    ],
}

T7 = {
    "slug": "actions-pages-releases",
    "title": "GitHub Actions, Pages, releases and security features",
    "lead": "Automate tests with a GitHub Actions workflow, publish a free website with GitHub Pages, tag versions and publish releases, and switch on Dependabot, secret scanning and code scanning.",
    "minutes": 22,
    "plain": "GitHub Actions is a robot that does a chore every time something happens, such as running your tests on every pull request. Pages is free hosting for a website straight from your repository. Releases are labelled boxes of a finished version.",
    "ideas": [
        ("Workflow", "A YAML file in .github/workflows/ that says when to run (on) and what to do (jobs and steps)."),
        ("Runner", "The machine that runs a job (GitHub-hosted Linux, Windows or macOS, or your own)."),
        ("Secrets", "Encrypted values (API keys) available to workflows, never printed in logs."),
        ("GitHub Pages", "Free static website hosting from a repository, at username.github.io or a custom domain."),
        ("Tag and release", "A tag names one commit (v1.0); a release adds notes and downloadable files."),
        ("Dependabot", "Alerts and pull requests that update vulnerable or outdated dependencies."),
    ],
    "flow": ["push or PR", "workflow triggers", "runner checks out code", "install + test", "status check on PR", "merge when green"],
    "body": [
        ("Your first workflow: test every pull request", CODE("""name: tests
on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest -q""", ".github/workflows/tests.yml") + UL([
            "Commit the file; the <b>Actions</b> tab shows each run and its logs.",
            "Make the check required for main in your ruleset, so failing code cannot be merged.",
            f"Store keys in {MENU('Settings', 'Secrets and variables', 'Actions')} and use them as <code>${{{{ secrets.API_KEY }}}}</code>.",
            "Pin actions to a version (or a commit SHA for third-party actions) and give workflows the least permissions they need.",
        ])),
        ("Publish a website with GitHub Pages", STEPS([
            "Put your site files (index.html and assets) in the repository, or build them with a workflow.",
            f"Open {MENU('Settings', 'Pages')}. Under <b>Build and deployment</b>, choose <b>Deploy from a branch</b> (main, root or /docs) or <b>GitHub Actions</b>.",
            "Wait a minute and open <code>https://username.github.io/repository/</code>.",
            "For your own domain, add it under <b>Custom domain</b>, create the DNS records your registrar needs, and tick <b>Enforce HTTPS</b>.",
        ]) + NOTE("Pages sites are public unless your plan includes private Pages. Never publish private data or secrets on a Pages site.", "warn")),
        ("Tags and releases", TERM("tags") + P("On GitHub open <b>Releases</b>, then <b>Draft a new release</b>, pick the tag, and select <b>Generate release notes</b> to list merged pull requests automatically. Use semantic versions: v1.4.2 means major.minor.patch.")),
        ("Security features to switch on", TABLE(["Feature", "What it does", "Where"], [
            ["Dependabot alerts and updates", "Warns about vulnerable dependencies and opens update PRs", "Settings, Code security"],
            ["Secret scanning and push protection", "Finds committed tokens and blocks pushes with known secret patterns", "Settings, Code security"],
            ["Code scanning (CodeQL)", "Finds security bugs in your code on every PR", "Security tab, Code scanning"],
            ["Security policy", "SECURITY.md tells people how to report vulnerabilities", "Repository root or .github/"],
        ])),
        ("Codespaces: a computer in the browser", P("Press <b>.</b> on a repository for a quick web editor, or open <b>Code, Codespaces</b> for a full cloud development environment with a terminal. A <code>.devcontainer/devcontainer.json</code> file sets up the same tools for everyone. Free personal usage is limited each month, so stop codespaces you are not using.")),
    ],
    "mistakes": [
        ("Printing secrets in workflow logs", "Use secrets, never echo them, and keep workflow permissions minimal."),
        ("Using unpinned third-party actions", "Pin to a version or a full commit SHA."),
        ("Expecting Pages to run a server or database", "Pages hosts static files only; use another service for back-end code."),
    ],
    "practice": [
        "Add the tests workflow to a small Python project and make it fail, then pass.",
        "Publish a one-page portfolio with GitHub Pages.",
        "Turn on Dependabot alerts and secret scanning for your repositories.",
    ],
    "quiz": [
        ("Where do workflow files live?", ".github/workflows/ in the repository, as YAML files."),
        ("How do you stop failing code from being merged?", "Make the workflow's status check required in the ruleset or branch protection for main."),
        ("What does push protection do?", "Blocks pushes that contain known secret formats, such as API tokens."),
    ],
    "links": [
        ("GitHub Actions quickstart", f"{GD}/actions/writing-workflows/quickstart"),
        ("GitHub Pages quickstart", f"{GD}/pages/quickstart"),
        ("About releases", f"{GD}/repositories/releasing-projects-on-github/about-releases"),
        ("Dependabot", f"{GD}/code-security/dependabot"),
        ("GitHub Codespaces", f"{GD}/codespaces/overview"),
    ],
}

T8 = {
    "slug": "github-with-ai",
    "title": "GitHub with AI: Copilot, the coding agent, Claude Code and Codex",
    "lead": "Use GitHub Copilot in your editor and on github.com, assign issues to the Copilot coding agent, ask @copilot to fix a pull request, review AI pull requests safely, and connect Claude Code or Codex to your repositories.",
    "minutes": 20,
    "plain": "AI coding agents are fast junior developers who never get tired. They can open pull requests on their own, but a human still reviews, tests and decides what gets merged. Your repository's rules (tests, rulesets, AGENTS.md) are how you keep quality high.",
    "ideas": [
        ("GitHub Copilot", "GitHub's AI assistant: completions and chat in editors, chat on github.com, code review, CLI and a cloud coding agent."),
        ("Copilot coding agent (cloud agent)", "Works on an issue or request in its own environment using GitHub Actions and opens a pull request for review."),
        ("@copilot in a PR", "Mention Copilot in a pull request comment to have it make the changes you ask for, including fixing failing checks."),
        ("Copilot code review", "Automatic or requested AI review comments on pull requests."),
        ("AGENTS.md / CLAUDE.md", "Repository files that tell AI agents how to build, test and follow your conventions."),
    ],
    "flow": ["Write a clear issue", "Assign an agent", "Agent opens PR", "Checks run", "Human reviews", "Merge or ask for changes"],
    "body": [
        ("Copilot in four places", TABLE(["Where", "What you do"], [
            ["Editor (VS Code, JetBrains, Visual Studio)", "Accept suggestions with Tab; use chat to explain, refactor or write tests; agent mode edits several files"],
            ["github.com", "Chat about a repository, file or pull request; ask \"what does this PR change?\""],
            ["Pull requests", "Request a Copilot review; mention @copilot to make changes"],
            ["Terminal", "Copilot CLI for commands and code tasks, including a security review command"],
        ]) + P("Plans and limits change; check github.com/features/copilot for what your plan includes (premium requests are counted for heavier features).")),
        ("Hand an issue to the coding agent", STEPS([
            "Write the issue like a ticket for a new teammate: goal, files involved, acceptance criteria, how to test.",
            "Assign the issue to <b>Copilot</b> (or start a task from the agents panel). It works in its own environment powered by GitHub Actions and opens a draft pull request.",
            "By default its workflow runs wait for a person to approve them; repository admins can choose to skip that approval.",
            "Review the PR like any other: read the diff, run it, check tests. Comment <code>@copilot please add a test for the empty-cart case</code> to ask for changes.",
            "Merge only when checks pass and a human approves.",
        ]) + NOTE("Pull requests from forks are not supported for @copilot changes. Keep agent PRs small by writing small issues.", "info")),
        ("Claude Code and Codex with GitHub", UL([
            "<b>Claude Code</b>: works in your local clone or in cloud sessions (claude.ai/code) on repositories you connect; it commits on a branch and can open pull requests. The Claude GitHub app lets you mention <code>@claude</code> in issues and PRs where your organisation has set it up.",
            "<b>Codex</b>: connect GitHub in Codex (desktop app, web, IDE or CLI); it works on a copy of the repository and proposes a pull request.",
            "Both read repository instructions: <code>CLAUDE.md</code> for Claude Code and <code>AGENTS.md</code> for Codex and many other agents. Import AGENTS.md from CLAUDE.md to keep one source.",
            "The Claude GitHub connector also lets Claude chat read your repositories and issues (Claude guide, Lesson 6).",
        ])),
        ("Rules that keep AI pull requests safe", TABLE(["Rule", "Why"], [
            ["Required status checks (tests, lint, CodeQL)", "Agents cannot merge broken or insecure code"],
            ["At least one human approval; CODEOWNERS for sensitive folders", "A person who knows the code decides"],
            ["Least-privilege tokens and workflow permissions", "Agents get only the access the task needs"],
            ["Secret scanning with push protection", "Stops keys being committed by anyone, human or AI"],
            ["Small issues with clear acceptance criteria", "Smaller, reviewable pull requests"],
        ])),
        ("Show your work: a portfolio that gets interviews", UL([
            "Pin 3 to 5 repositories with clear READMEs: problem, approach, results, how to run.",
            "Use issues and pull requests on your own projects; recruiters can see a real workflow.",
            "Add a GitHub Actions badge and a live demo link (GitHub Pages).",
            "Say which parts used AI and how you checked them; this is increasingly asked in interviews.",
        ]) + P("More on portfolios: SkillNavora lesson <a href=\"data-science/lessons/career-01-portfolio-github-and-resume-for-data-roles.html\">Portfolio, GitHub and resume for data roles</a>.")),
    ],
    "mistakes": [
        ("Merging an agent PR because the description sounds right", "Read the diff and run the tests yourself."),
        ("Vague issues assigned to an agent", "Write acceptance criteria and test steps."),
        ("Giving an agent admin tokens", "Use least-privilege access and required reviews."),
    ],
    "practice": [
        "Write an issue with acceptance criteria and assign it to an AI agent (Copilot, Claude Code or Codex); review its PR.",
        "Add AGENTS.md to a repository and import it from CLAUDE.md.",
        "Set a ruleset on main that requires passing checks and one approval.",
    ],
    "quiz": [
        ("What does the Copilot coding agent produce?", "A pull request (often a draft) for a human to review."),
        ("How do you ask Copilot to change an open pull request?", "Mention @copilot in a PR comment with the change you want."),
        ("Which file do Codex and many agents read for repository rules?", "AGENTS.md (Claude Code reads CLAUDE.md, which can import AGENTS.md)."),
        ("Name two repository settings that keep AI PRs safe.", "Required status checks and required human approval (also CODEOWNERS, secret scanning, least-privilege tokens)."),
    ],
    "links": [
        ("GitHub Copilot docs", f"{GD}/copilot"),
        ("About the Copilot coding agent", f"{GD}/copilot/concepts/coding-agent/about-coding-agent"),
        ("GitHub changelog (Copilot)", "https://github.blog/changelog/label/copilot/"),
        ("Claude Code GitHub Actions", "https://code.claude.com/docs/en/overview"),
        ("AGENTS.md", "https://agents.md"),
    ],
}

GUIDE = {
    "id": "git",
    "title": "Git & GitHub Complete Guide",
    "subtitle": "How Git works, daily commands, branches, collaboration, undo, Actions, Pages and AI agents",
    "checked": CHECKED,
    "hue": 22,
    "pdf": "handbook/Git-and-GitHub-Complete-Guide.pdf",
    "intro": "Git and GitHub from zero to confident: the mental model, setup with SSH and the GitHub CLI, the daily loop, branches and conflicts, pull requests and reviews, undoing mistakes, Actions, Pages and releases, and working with AI coding agents. Every terminal block is real output from Git 2.43, captured when this guide was built.",
    "lessons": [T1, T2, T3, T4, T5, T6, T7, T8],
    "sources": [("Pro Git book", "https://git-scm.com/book/en/v2"), ("GitHub Docs", "https://docs.github.com"), ("GitHub changelog", "https://github.blog/changelog/")],
}
