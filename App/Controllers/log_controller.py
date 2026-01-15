from Services.log_service import LogService

leg_service = LogService()

def get_log(repo_path : str, commit : str):
    return LogService.get_log(repo_path=repo_path,commit=commit)