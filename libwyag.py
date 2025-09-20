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


def repo_find(path='.',required=True):
    path = os.path.realpath(path)

    if os.path.isdir(os.path.join(path,'.git')):
        return GitRepository(path)
    
    parent = os.path.realpath(os.path.join(path,".."))

    if parent == path:
        if required:
            raise Exception("No git directory")
        else :
            return None
        
    return repo_find(parent,required)



class GitObject(object):

    def __init__(self,data=None):
        if data !=None:
            pass
        else :
            self.init()
    
    # python object to git object with binary
    def serialize(self,repo):
        raise Exception("Unimplemented")
    
    # binary git bobject to python object
    def deserialize(self ,data):
        raise Exception("Unimplemented")
    
    def init(self):
        pass



    def object_read(repo, sha):
        """
        Belirtilen SHA-1 hash'ine (nesne kimliği) sahip Git nesnesini okur.
        
        Argümanlar:
            repo: GitRepository nesnesi. Depo yollarını yönetmek için kullanılır.
            sha: Okunacak nesnenin 40 karakterlik SHA-1 hash'i.
        
        Döndürür:
            Okunan veriye sahip bir Git nesnesi (örn. GitBlob, GitCommit).
        """

        # 1. Objenin dosya yolunu bul
        # Git, nesneleri SHA-1 hash'inin ilk 2 karakterini klasör adı,
        # kalan 38 karakterini ise dosya adı olarak kullanarak depolar.
        # Örnek: '2a/982181b67d93b3e21079d2b27083049174665'
        path = repo_file(repo, "object", sha[0:2], sha[2:])

        # Dosya mevcut değilse, nesne bulunamadığı için None döner.
        if not os.path.isfile(path):
            return None
        
        # 2. Sıkıştırılmış veriyi oku ve aç
        # Nesne dosyaları zlib kütüphanesi ile sıkıştırılmıştır.
        with open(path, "rb") as f:
            # Dosyayı ikili (binary) modda okur ve zlib ile sıkıştırmasını açar.
            raw = zlib.decompress(f.read())

        # 3. Nesnenin başlık bilgilerini ayrıştır
        # Okunan verinin başında "nesne_tipi boşluk boyut_bilgisi \0" şeklinde bir başlık bulunur.
        # Örnek: b'blob 12\x00merhaba dunya'
        
        # İlk boşluğun konumunu bulur. Bu, nesne tipinin bittiği yerdir.
        x = raw.find(b' ')
        fmt = raw[0:x]  # 'blob', 'tree', 'commit' gibi nesne tipini alır.

        # Boşluktan sonraki ilk null byte'ın (\x00) konumunu bulur.
        # Bu, boyut bilgisinin bittiği yerdir.
        y = raw.find(b'\x00', x)
        
        # Boşluk ile null byte arasındaki veriyi alıp tam sayıya (int) dönüştürür.
        size = int(raw[x:y].decode("ascii"))

        # 4. Veri bütünlüğünü kontrol et
        # Başlıkta belirtilen boyut ile, null byte'tan sonraki gerçek veri boyutunu karşılaştırır.
        # Eğer boyutlar eşleşmiyorsa, dosyanın bozuk olduğu anlamına gelir ve hata fırlatılır.
        if size != len(raw) - y - 1:
            raise Exception(f"Malformed object {sha}: bad length")
        
        # 5. Doğru nesne sınıfını seç ve başlat
        # 'match' ifadesiyle, belirlenen nesne tipine göre doğru Python sınıfını seçer.
        # Örnek: Nesne tipi b'blob' ise, c değişkeni GitBlob sınıfına atanır.
        match fmt:
            case b'commit':
                c = GitCommit
            case b'tree':
                c = GitTree
            case b'tag':
                c = GitTag
            case b'blob':
                c = GitBlob
            case _:
                # Eğer tip tanıdık değilse, desteklenmediği için hata fırlatır.
                raise Exception(f"Unknown type {fmt.decode('ascii')} for object {sha}")
                
        # 6. Nesneyi oluştur ve veriyi yükle
        # Seçilen sınıfın yapıcısını (constructor) çağırarak yeni bir nesne oluşturur.
        # Yapıcıya, null byte'tan sonra başlayan ham veri bloğunu argüman olarak verir.
        return c(raw[y+1:])

    def object_write(obj, repo=None):
        # Serialize object data
        data = obj.serialize()
        # Add header
        result = obj.fmt + b' ' + str(len(data)).encode() + b'\x00' + data
        # Compute hash
        sha = hashlib.sha1(result).hexdigest()

        if repo:
            # Compute path
            path=repo_file(repo, "objects", sha[0:2], sha[2:], mkdir=True)

            if not os.path.exists(path):
                with open(path, 'wb') as f:
                    # Compress and write
                    f.write(zlib.compress(result))
        return sha