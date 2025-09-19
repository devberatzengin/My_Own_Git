import argparse
import configparser
from datetime import datetime
import grp, pwd
from fnmatch import fnmatch
import hashlib
from math import ceil
import os
import re
import sys
import zlib

# Argparse objesini başlatır.
# Bu, komut satırı argümanlarını (örneğin 'init', 'add') ayrıştırmak için kullanılır.
argparser = argparse.ArgumentParser(description="The stupidest content tracker")

# Alt ayrıştırıcıları (subparsers) ekler. Bu, farklı komutları tanımlamamızı sağlar.
# Örneğin, 'wyag init' ve 'wyag add' gibi.
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

# 'init' komutu için bir alt ayrıştırıcı oluşturur.
# Bu, 'wyag init' komutunun argümanlarını yönetmek için kullanılır.
argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")
argsp.add_argument("path",
                   metavar="directory",
                   nargs="?", # Kullanıcının 'path' argümanını isteğe bağlı yapmaya yarar.
                   default=".", # Eğer 'path' belirtilmezse, varsayılan olarak mevcut dizini kullanır.
                   help="Where to create the repository.")


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    # 'match' ifadesi, Python 3.10 ve üzeri sürümlere özeldir.
    # Bu, 'args.command' değerine göre ilgili fonksiyonu çağırmak için kullanılır.
    match args.command:
        case "add"          : cmd_add(args)
        case "cat-file"     : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash-object"  : cmd_hash_object(args)
        case "init"         : cmd_init(args)
        case "log"          : cmd_log(args)
        case "ls-files"     : cmd_ls_files(args)
        case "ls-tree"      : cmd_ls_tree(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"           : cmd_rm(args)
        case "show-ref"     : cmd_show_ref(args)
        case "status"       : cmd_status(args)
        case "tag"          : cmd_tag(args)
        case _              : print("Bad command.")


class GitRepository(object):
    """Bir git deposu"""

    worktree = None # Çalışma dizinini (kullanıcının proje dosyalarının bulunduğu yer) tutar.
    gitdir = None # Git'in kendi verilerini (.git klasörü) tutar.
    conf = None # Deponun ayar dosyasını (config) tutar.

    def __init__(self, path, force=False):
        # Gerçek dosya yolunu alır ve 'worktree' değişkenine atar.
        self.worktree = os.path.realpath(path)
        # '.git' dizininin yolunu oluşturur.
        self.gitdir = os.path.join(self.worktree, '.git')

        # 'force' (zorla oluşturma) modu aktif değilse VE '.git' klasörü yoksa hata verir.
        # Bu, var olan bir depoyu açmaya çalışırken kullanılır.
        if not force and not os.path.isdir(self.gitdir):
            raise Exception(f"Not a git repository {path}")

        self.conf = configparser.ConfigParser()
        # repo_file fonksiyonu ile '.git/config' dosyasının yolunu alır.
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            # Eğer config dosyası varsa, onu okur.
            self.conf.read(cf)
        elif not force:
            # 'force' modu aktif değilse ve config dosyası yoksa hata verir.
            raise Exception("Config file missing")

        if not force:
            # Depo format sürümünü kontrol eder. Sadece versiyon 0'ı kabul eder.
            # Bu, gelecekteki format değişikliklerinden etkilenmemizi sağlar.
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(f"Unsupported repositoryformatversion: {vers}")

def repo_path(repo, *path):
    """Deponun git dizini altındaki bir dosyanın yolunu hesaplar."""
    return os.path.join(repo.gitdir, *path)

def repo_file(repo, *path, mkdir=False):
    """Bir dosyanın yolunu hesaplar ve isteğe bağlı olarak eksik üst dizinleri oluşturur."""
    
    # path'in son elemanı dosya adı olduğu için, *path[:-1] ile dizin yolunu alırız.
    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)

def repo_dir(repo, *path, mkdir=False):
    """Bir dizinin yolunu hesaplar ve isteğe bağlı olarak oluşturur."""
    path = repo_path(repo, *path)

    # Yol zaten varsa, bir dizin olup olmadığını kontrol eder.
    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            raise Exception(f"Not a directory {path}")

    # mkdir True ise, eksik dizinleri oluşturur.
    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None

def repo_create(path):
    """Belirtilen yolda yeni bir depo oluşturur."""

    # Depoyu 'force=True' ile başlatır, çünkü henüz '.git' dizini yok.
    repo = GitRepository(path, force=True)

    # Depo yolunun var olup olmadığını ve boş olup olmadığını kontrol eder.
    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception(f"{path} is not a directory!")
        if os.listdir(repo.worktree):
            raise Exception(f"{path} is not empty!")
    else:
        os.makedirs(repo.worktree)

    # Gerekli alt dizinleri oluşturur. assert ifadesi, dizinlerin başarıyla oluşturulduğunu kontrol eder.
    assert repo_dir(repo, "branches", mkdir=True)
    assert repo_dir(repo, "objects", mkdir=True)
    assert repo_dir(repo, "refs", "tags", mkdir=True)
    assert repo_dir(repo, "refs", "heads", mkdir=True)

    # .git/description dosyasını yazar.
    with open(repo_file(repo, "description"), "w") as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

    # .git/HEAD dosyasını yazar. Bu, mevcut branch'i gösterir.
    with open(repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    # .git/config dosyasını varsayılan ayarlarla yazar.
    with open(repo_file(repo, "config"), "w") as f:
        config = repo_default_config()
        config.write(f)

    return repo

def repo_default_config():
    """Varsayılan depo yapılandırmasını oluşturur."""
    ret = configparser.ConfigParser()

    ret.add_section("core")
    ret.set("core", "repositoryformatversion", "0") # Format versiyonu.
    ret.set("core", "filemode", "false") # Dosya izinleri değişikliklerini takip etmeyi kapatır.
    ret.set("core", "bare", "false") # Bu deponun bir çalışma ağacına sahip olduğunu belirtir.

    return ret

def cmd_init(args):
    """'init' komutunun köprü fonksiyonu."""
    # repo_create fonksiyonunu argparse'dan gelen yol argümanı ile çağırır.
    repo_create(args.path)




    """ ---------- 3.3 ile devam et"""