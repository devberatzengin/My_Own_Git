# My_Own_Git

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Version Control](https://img.shields.io/badge/Version%20Control-Core%20System-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

**A custom implementation of Git's core functionality from scratch using Python. Learn how version control actually works under the hood.**

---

## 🎯 Project Overview

This project replicates Git's essential features by building a version control system from the ground up. Instead of using Git's C implementation, this is a pure Python implementation designed to teach and demonstrate how modern VCS (Version Control Systems) work internally.

**What you'll learn:**
- How commits, branches, and merge algorithms work
- Object storage and compression in version control
- DAG (Directed Acyclic Graph) structures
- Content-addressable storage using hashing
- Merge conflict resolution

---

## ✨ Features

- ✅ **Repository initialization** — Create local `.mygit` directories
- ✅ **Commit system** — Store snapshots with SHA-1 hashing
- ✅ **Branching** — Create, switch, and list branches
- ✅ **Merge operations** — Fast-forward and recursive merges
- ✅ **Status tracking** — Monitor staged and unstaged changes
- ✅ **Diff visualization** — Compare versions
- ✅ **Revert functionality** — Undo commits safely

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/devberatzengin/My_Own_Git.git
cd My_Own_Git
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Basic Commands

```bash
# Initialize a repository
python mygit.py init

# Stage changes
python mygit.py add <file>

# Create a commit
python mygit.py commit -m "Your message"

# Create a branch
python mygit.py branch <branch-name>

# Switch branches
python mygit.py checkout <branch-name>

# Merge branches
python mygit.py merge <branch-name>

# View status
python mygit.py status

# View history
python mygit.py log
```

---

## 📁 Project Structure

```
My_Own_Git/
├── mygit.py              # Main entry point
├── core/
│   ├── objects.py        # Commit, Tree, Blob classes
│   ├── repository.py     # Repository management
│   ├── staging.py        # Index/staging area
│   └── merge.py          # Merge algorithms
├── cli/
│   └── commands.py       # CLI interface
├── utils/
│   ├── hash.py           # SHA-1 hashing
│   └── diff.py           # File diffing
├── tests/
│   ├── test_commits.py
│   ├── test_merge.py
│   └── test_branches.py
└── requirements.txt

```

---

## 🔧 Technical Details

### Architecture

**Object Model:**
- **Blob** — File content (immutable)
- **Tree** — Directory snapshot
- **Commit** — Metadata + parent reference + tree
- **Ref** — Pointer to commit (branch/tag)

**Storage:**
```
.mygit/
├── objects/              # Content-addressable storage
│   ├── <hash[0:2]>/
│   │   └── <hash[2:]>   # Zlib-compressed object
├── refs/
│   ├── heads/           # Branch pointers
│   └── tags/            # Tag pointers
└── HEAD               # Current branch reference
```

**Merge Algorithm:**
- Three-way merge for automatic resolution
- Conflict markers for manual cases
- Recursive history traversal using LCA (Lowest Common Ancestor)

---

## 📊 How It Works: Internal Flow

```
User creates file → Add to staging → Commit
                      ↓
              Create blob + tree
                      ↓
           Hash objects + store in .mygit/objects
                      ↓
          Update branch ref to new commit SHA
                      ↓
            Update HEAD if on that branch
```

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_commits.py -v

# With coverage
pytest --cov=core tests/
```

---

## 📚 Key Learning Outcomes

After studying this project, you'll understand:

1. **How Git stores data** — Content-addressable storage model
2. **Commit structure** — Snapshots vs. deltas
3. **Branch mechanics** — Just pointers to commits
4. **Merge algorithms** — Three-way merge + conflict detection
5. **Performance** — Why Git is fast (DAGs, compression)

---

## 🤔 Future Enhancements

- [ ] Remote repositories (push/pull simulation)
- [ ] Rebase functionality
- [ ] Cherry-pick operations
- [ ] Stash management
- [ ] Hook system (pre-commit, post-commit)
- [ ] Performance optimization with C extensions

---

## 💡 References

- [Git Internals - Git Book](https://git-scm.com/book/en/v2/Git-Internals)
- [Linus Torvalds' Original Design](https://www.kernel.org/doc/html/latest/process/applying-patches.html)
- [Mercurial's Revlog Format](https://www.mercurial-scm.org/)

---

## 🤝 Contributing

Found a bug or want to improve the merge algorithm? Pull requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📧 Questions?

Open an issue or reach out on [LinkedIn](https://www.linkedin.com/in/berat-zengin-1a337a294/)
