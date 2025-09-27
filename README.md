# WYAG (Write Your Own Git) - Kendi Git Uygulamam

## Proje Hakkında

Bu proje, bir portfolyo çalışmasından öte, Git versiyon kontrol sisteminin **çekirdek mantığını** ve **temel prensiplerini** anlamak amacıyla yazılmış bir uygulamadır. Bu uygulamayı geliştirirken, [wyag.thb.lt](https://wyag.thb.lt/) adresindeki mükemmel rehberden faydalanıyor ve kodun her satırını aşama aşama kendim yazıyorum. **Amacım, Git'i yalnızca komutları ezberlenmiş bir kara kutu olarak kullanmak yerine, derinlemesine kavramaktır. Bu, karmaşık bir aracı sıfırdan inşa etmenin verdiği eşsiz tatmini yaşamak ve problem çözme yeteneklerimi bir sonraki seviyeye taşımak için bir fırsattır.**

Bu proje, Git'in temel mantığını öğrenmek amacıyla Python diliyle geliştirilmiş basit bir Git klonudur. Amacı, Git'in çalışma prensiplerini (commit, tree, blob, branch vb.) düşük seviyede anlamaktır.

## Özellikler
- Temel Git nesnelerini (blob, tree, commit) yönetme
- Repository başlatma (`init`)
- Dosya ekleme ve commit işlemleri
- Branch oluşturma ve checkout
- Commit geçmişini inceleme (`log`)
- Dosya içeriklerini görüntüleme (`cat-file`)
- Object hashleme (SHA-1) mantığı


## Projeyi Çalıştırma

Projeyi kendi terminalinizde denemek için şu adımları izleyebilirsiniz:

1.  Bu depoyu yerel makinenize klonlayın.
2.  Python 3.10 veya üzeri bir sürümün yüklü olduğundan emin olun.
3.  Terminalde `wyag` dosyasının bulunduğu dizine gidin.
4.  Yeni bir depo oluşturmak için aşağıdaki komutu çalıştırın:
    ```bash
    python wyag init <depo_adı>
    ```

## Gereksinimler
- Python 3.7+
- Hashlib (standart kütüphane)

## Lisans
MIT

## Kaynak ve Teşekkür

Bu projenin temelini oluşturan, harika ve anlaşılır rehber için [wyag.thb.lt](https://wyag.thb.lt/) sitesinin yazarına teşekkür ederim.
