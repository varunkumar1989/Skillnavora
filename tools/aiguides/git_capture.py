"""Runs every Git command shown in the Git & GitHub guide in a throwaway folder and saves the real output.

Run:  python3 tools/aiguides/git_capture.py
Writes tools/aiguides/git_outputs.json  {demo_key: "$ command\\noutput\\n..."}
Dates and names are fixed, so commit hashes are the same on every run. A local bare repository
stands in for GitHub, so push, fetch and pull work without a network or an account.
"""
import json, os, shutil, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "git_outputs.json")

BASE_ENV = {
    "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0", "LANG": "C", "LC_ALL": "C",
    "GIT_PAGER": "cat", "PAGER": "cat", "TZ": "Asia/Kolkata",
}
_clock = [0]


def sh(cwd, cmd, show=True, home=None):
    """Run one shell command. Every command gets the next fixed timestamp, so hashes are stable."""
    _clock[0] += 60
    stamp = f"2026-11-02T10:{_clock[0] // 60 % 60:02d}:00+05:30"
    env = dict(os.environ, **BASE_ENV, GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp, HOME=home or cwd)
    r = subprocess.run(cmd, shell=True, cwd=cwd, env=env, capture_output=True, text=True)
    out = (r.stdout + r.stderr).rstrip()
    return (f"$ {cmd}\n{out}" if out else f"$ {cmd}") if show else out


def demo(lines):
    return "\n".join(x for x in lines if x is not None)


def main():
    tmp = tempfile.mkdtemp(prefix="gitguide-")
    home = os.path.join(tmp, "home")
    os.makedirs(home)
    subprocess.run(["git", "config", "--file", os.path.join(home, ".gitconfig"), "init.defaultBranch", "main"], check=True)
    for k, v in (("advice.detachedHead", "false"), ("user.name", "Asha Learner"), ("user.email", "asha@example.com")):
        subprocess.run(["git", "config", "--file", os.path.join(home, ".gitconfig"), k, v], check=True)
    H = lambda cwd, cmd, show=True: sh(cwd, cmd, show, home)
    out = {}
    try:
        # ---------------------------------------------------------------- 1. first repository
        p = os.path.join(tmp, "notes")
        os.makedirs(p)
        out["init"] = demo([
            H(p, "git init"),
            H(p, "git config user.name \"Asha Learner\""),
            H(p, "git config user.email \"asha@example.com\""),
            H(p, "echo '# My study notes' > README.md"),
            H(p, "git status"),
        ])
        out["first_commit"] = demo([
            H(p, "git add README.md"),
            H(p, "git status --short"),
            H(p, "git commit -m \"Add README with the course title\""),
            H(p, "git log --oneline"),
        ])
        # how Git stores things
        out["internals"] = demo([
            H(p, "git cat-file -t HEAD"),
            H(p, "git cat-file -p HEAD"),
            H(p, "git cat-file -p HEAD^{tree}"),
            H(p, "git cat-file -p HEAD:README.md"),
            H(p, "cat .git/HEAD"),
            H(p, "cat .git/refs/heads/main"),
        ])
        # ---------------------------------------------------------------- 2. daily loop
        out["daily"] = demo([
            H(p, "printf '# My study notes\\n\\n## Git\\n- commit = snapshot\\n' > README.md"),
            H(p, "echo 'print(\"hello\")' > hello.py"),
            H(p, "git status --short"),
            H(p, "git diff"),
            H(p, "git add README.md hello.py"),
            H(p, "git diff --staged --stat"),
            H(p, "git commit -m \"Add Git notes and a hello script\""),
            H(p, "git log --oneline --stat -1"),
        ])
        out["gitignore"] = demo([
            H(p, "mkdir -p __pycache__ && echo x > __pycache__/hello.cpython-312.pyc && echo 'API_KEY=secret' > .env"),
            H(p, "git status --short"),
            H(p, "printf '__pycache__/\\n.env\\n' > .gitignore"),
            H(p, "git status --short"),
            H(p, "git add .gitignore && git commit -q -m \"Ignore cache files and .env\""),
            H(p, "git check-ignore -v .env"),
        ])
        out["restore"] = demo([
            H(p, "echo 'oops, wrong line' >> README.md"),
            H(p, "git status --short"),
            H(p, "git restore README.md"),
            H(p, "git status --short"),
            H(p, "echo 'draft' > draft.txt && git add draft.txt"),
            H(p, "git restore --staged draft.txt"),
            H(p, "git status --short"),
            H(p, "rm draft.txt"),
        ])
        # ---------------------------------------------------------------- 3. branches, merge, conflict, rebase
        out["branch_ff"] = demo([
            H(p, "git switch -c feature/quiz"),
            H(p, "echo 'Q1: What is a commit?' > quiz.md && git add quiz.md && git commit -q -m \"Add quiz question 1\""),
            H(p, "git log --oneline --all"),
            H(p, "git switch main"),
            H(p, "git merge feature/quiz"),
            H(p, "git branch -d feature/quiz"),
        ])
        H(p, "git switch -q -c feature/title", show=False)
        H(p, "printf '# Asha study notes\\n\\n## Git\\n- commit = snapshot\\n' > README.md && git commit -q -am \"Rename notes title\"", show=False)
        H(p, "git switch -q main", show=False)
        H(p, "printf '# My Git and GitHub notes\\n\\n## Git\\n- commit = snapshot\\n' > README.md && git commit -q -am \"Change title on main\"", show=False)
        out["conflict"] = demo([
            H(p, "git log --oneline --graph --all -4"),
            H(p, "git merge feature/title"),
            H(p, "git status --short"),
            H(p, "cat README.md"),
            H(p, "printf '# Asha: Git and GitHub notes\\n\\n## Git\\n- commit = snapshot\\n' > README.md"),
            H(p, "git add README.md"),
            H(p, "git commit -q -m \"Merge feature/title: keep both ideas in the title\""),
            H(p, "git log --oneline --graph -5"),
        ])
        H(p, "git branch -q -d feature/title", show=False)
        H(p, "git switch -q -c feature/glossary", show=False)
        H(p, "echo 'branch = movable pointer to a commit' > glossary.md && git add glossary.md && git commit -q -m \"Add glossary\"", show=False)
        H(p, "git switch -q main", show=False)
        H(p, "echo 'Q2: What does git add do?' >> quiz.md && git commit -q -am \"Add quiz question 2\"", show=False)
        out["rebase"] = demo([
            H(p, "git log --oneline --graph --all -3"),
            H(p, "git switch feature/glossary"),
            H(p, "git rebase main"),
            H(p, "git log --oneline --graph -3"),
            H(p, "git switch main && git merge --ff-only feature/glossary"),
        ])
        H(p, "git branch -q -d feature/glossary", show=False)
        out["stash"] = demo([
            H(p, "echo 'half-written idea' >> glossary.md"),
            H(p, "git stash push -m \"glossary draft\""),
            H(p, "git status --short"),
            H(p, "git stash list"),
            H(p, "git stash pop"),
            H(p, "git status --short"),
            H(p, "git restore glossary.md"),
        ])
        # ---------------------------------------------------------------- 4. remote (a bare repo stands in for GitHub)
        remote = os.path.join(tmp, "github", "notes.git")
        os.makedirs(os.path.dirname(remote))
        H(tmp, f"git init -q --bare {remote}", show=False)
        out["push"] = demo([
            H(p, "git remote add origin ../github/notes.git"),
            H(p, "git remote -v"),
            H(p, "git push -u origin main"),
            H(p, "git branch -vv"),
        ]).replace(tmp, "/home/asha")
        team = os.path.join(tmp, "ravi")
        out["clone_pull"] = demo([
            H(tmp, "git clone -q github/notes.git ravi && echo cloned"),
            H(team, "git config user.name \"Ravi Teammate\" && git config user.email ravi@example.com && echo 'Q3: What is a remote?' >> quiz.md && git commit -q -am \"Add quiz question 3\" && git push -q && git log --oneline -1"),
            H(p, "git fetch"),
            H(p, "git status -sb"),
            H(p, "git log --oneline main..origin/main"),
            H(p, "git pull --ff-only"),
        ]).replace(tmp, "/home/asha")
        # ---------------------------------------------------------------- 5. undo
        out["amend"] = demo([
            H(p, "echo 'tag = a name for one commit' >> glossary.md && git commit -q -am \"Add tag defnition\""),
            H(p, "git log --oneline -1"),
            H(p, "git commit --amend -q -m \"Add tag definition\""),
            H(p, "git log --oneline -1"),
        ])
        out["reset"] = demo([
            H(p, "echo 'temp line' >> quiz.md && git commit -q -am \"Temporary commit\""),
            H(p, "git log --oneline -2"),
            H(p, "git reset --soft HEAD~1"),
            H(p, "git status --short"),
            H(p, "git reset --mixed HEAD"),
            H(p, "git status --short"),
            H(p, "git restore quiz.md && git status --short && echo clean"),
        ])
        out["revert"] = demo([
            H(p, "echo 'wrong fact: git is a GitHub product' >> glossary.md && git commit -q -am \"Add a wrong fact\" && git push -q"),
            H(p, "git revert --no-edit HEAD"),
            H(p, "git log --oneline -3"),
        ])
        out["reflog"] = demo([
            H(p, "git reset --hard HEAD~2"),
            H(p, "git log --oneline -1"),
            H(p, "git reflog -4"),
            H(p, "git reset --hard HEAD@{1}"),
            H(p, "git log --oneline -1"),
        ])
        # ---------------------------------------------------------------- 6. tags and history
        out["tags"] = demo([
            H(p, "git tag -a v1.0 -m \"First complete set of notes\""),
            H(p, "git tag"),
            H(p, "git show v1.0 --stat --format='%h %s'"),
            H(p, "git push -q origin v1.0 && git ls-remote --tags origin"),
        ]).replace(tmp, "/home/asha")
        out["history"] = demo([
            H(p, "git log --oneline --graph -8"),
            H(p, "git log --oneline --author=Ravi"),
            H(p, "git log --oneline -S \"remote\""),
            H(p, "git blame -s quiz.md"),
            H(p, "git show --stat --format='%h %an %s' HEAD~1"),
        ])
        out["version"] = sh(tmp, "git --version", True, home)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    out = {k: v.replace(tmp, "/home/asha") for k, v in out.items()}
    json.dump(out, open(OUT, "w"), indent=1)
    print("captured", len(out), "demos ->", OUT)


if __name__ == "__main__":
    main()
