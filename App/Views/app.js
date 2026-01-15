const API = "http://127.0.0.1:8000";
const panels = document.querySelectorAll(".panel");

const q = id => document.getElementById(id);

function show(id) {
    panels.forEach(p => p.classList.remove("active"));
    document.getElementById(id).classList.add("active");
    q("pageTitle").innerText =
        id.charAt(0).toUpperCase() + id.slice(1);
}

function toast(msg) {
    const t = q("toast");
    t.innerText = msg;
    t.style.opacity = 1;
    t.style.transform = "translateY(0)";
    setTimeout(() => {
        t.style.opacity = 0;
        t.style.transform = "translateY(10px)";
    }, 2500);
}

function setRepo(path) {
    q("activeRepo").innerText = path;
}

function createRepo() {
    const path = q("repoPath").value;
    fetch(`${API}/repositories/?repo_path=${path}`, { method: "POST" })
        .then(r => r.json())
        .then(() => {
            setRepo(path);
            toast("Repository initialized");
        });
}

function createCommit() {
    const repo = q("commitRepo").value;
    fetch(`${API}/repositories/${repo}/commits/?message=${q("commitMsg").value}`,
        { method: "POST" })
        .then(r => r.json())
        .then(() => {
            setRepo(repo);
            toast("Commit created");
        });
}

function getLog() {
    const repo = q("logRepo").value;
    fetch(`${API}/repositories/${repo}/log/`)
        .then(r => r.json())
        .then(d => {
            setRepo(repo);
            q("logOutput").textContent =
                JSON.stringify(d, null, 2);
        });
}

function createBranch() {
    fetch(`${API}/repositories/${q("branchRepo").value}/branches/?branch_name=${q("branchName").value}`,
        { method: "POST" })
        .then(() => toast("Branch created"));
}

function checkout() {
    fetch(`${API}/repositories/${q("checkoutRepo").value}/checkout/?branch_name=${q("checkoutBranch").value}`,
        { method: "POST" })
        .then(() => toast("Switched branch"));
}
