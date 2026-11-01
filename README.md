# gamedev-skill

Claude Code ve Codex için oyun hissiyatı, doğru gameplay ve ölçülmüş performans skill'i.
Tek ortak paket: [`skills/gamedev/SKILL.md`](skills/gamedev/SKILL.md).
Motor bağımsız ana akış; Unity için gerektiğinde okunan kısa entegrasyon notları.

34 oyun geliştirme kavramının tamamı
[karar ve doğrulama rehberinde](skills/gamedev/references/concepts.md) kapsanır.
Kavramlar her projeye zorla eklenmez; oyuncunun yaşadığı belirtiye göre seçilir.

## Kurulum

Repoyu klonladıktan sonra **yalnızca `skills/gamedev` klasörünü içeriğiyle birlikte**
istediğiniz proje kökündeki aşağıdaki konumlara kopyalayın:

| Araç | Hedef | Açık çağrı |
| --- | --- | --- |
| Codex | `.agents/skills/gamedev/` | `$gamedev` |
| Claude Code | `.claude/skills/gamedev/` | `/gamedev` |

Her ikisinde de aynı dosyalar kullanılır; API anahtarı, MCP, paket kurulumu veya
araca özgü betik gerekmez. Otomatik seçim açıktır. Güncellemede aynı klasörü yeniden
kopyalayın; referansları atlamayın. Skill görünmüyorsa oturumu yeniden başlatın.
Kişisel kullanım için aynı klasör sırasıyla `~/.agents/skills/` veya
`~/.claude/skills/` altına konabilir.

Kurulum biçimi [Codex](https://learn.chatgpt.com/docs/build-skills) ve
[Claude Code](https://code.claude.com/docs/en/skills) belgelerine dayanır.

## Kullanım

```text
$gamedev Bu oyunda dokunma bazen iki satın alma yapıyor; nedeni bul, en küçük düzeltmeyi yap ve doğrula.
/gamedev Kameranın takip hissini iyileştir; mevcut kamera sistemini koru, düşük FPS ve pause/resume ile sına.
$gamedev Bu Unity projesini yalnızca incele; en önemli üç hissiyat sorununu dosya/satır kanıtıyla raporla.
```

Skill önce gerçek sahneyi, input/state/simulation zincirini ve mevcut testleri okur;
sonra küçük bir davranış sözleşmesiyle ilerler. Ekran sarsıntısı eklemeyi otomatik
olarak iyileşme saymaz, derlenen kodu oynanış testi diye sunmaz ve ölçüm olmadan
performans artışı iddia etmez.

## Doğrulama

[Test kaydı](tests/README.md) ve [WalkingCity'deki 34 kavramın değerlendirmesi](tests/walkingcity-coverage.md)
repo içinde. Codex yüklemesi gerçek araçla, skill davranışı bağımsız değerlendirmelerle
ve Unity EditMode testleriyle sınandı; üç somut gameplay/feedback hatası yeniden üretildi.
Claude uyumluluğu belge/biçim düzeyinde doğrulandı; Claude çalışma oturumu yürütülmedi.
WalkingCity kaynakları kalıcı değiştirilmedi ve oyun reposuna commit atılmadı.
