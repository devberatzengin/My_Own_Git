from Services.commit_service import CommitService

commit_service = CommitService()


def create_commit(repo_path: str, message: str):
    return commit_service.create_commit(repo_path, message)


def get_commits(repo_path: str):
    return commit_service.get_commits(repo_path)


def get_commit_by_hash(repo_path: str, commit_hash: str):
    return commit_service.get_commit_by_hash(repo_path, commit_hash)
