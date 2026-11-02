# gamedev

Claude Code ve Codex için oyun mekaniği tasarlayan, uygulayan ve hissiyatını iyileştiren ortak skill.
Ana dosya: [`skills/gamedev/SKILL.md`](skills/gamedev/SKILL.md).

## Nasıl düşünür?

Önce oyuncunun niyetini ve beklenen deneyimi belirler; sonra input, kural, gerçek sonuç,
geri bildirim ve sonraki karar arasındaki kopukluğu bulur. Yeni mekanikte normal kontrollerle
ulaşılan oynanabilir döngüyü tamamlar; mevcut mekanikte en etkili küçük değişikliği seçer.

“Daha ağır hareket” isteğini input gecikmesine çevirmek yerine hızlanma, durma mesafesi
ve görsel ağırlığı ayırır. “Daha tatmin edici inşa” isteğinde ödeme, yerleşim, tamamlanma ve
tekrar seçim ilişkisini kurar. “Oyun sıkıcı” dendiğinde yeni sistemler eklemeden mevcut
seçimlerin sonraki kararı değiştirip değiştirmediğini inceler.

[Gameplay alıştırmaları](skills/gamedev/references/gameplay.md) bu kararları kısa deneylere
çevirir: oynanış döngüsü, hareket, eylem ritmi, kamera, ekonomi, karşılaşma ve yük altında
kararlılık. [Unity notları](skills/gamedev/references/unity.md) yalnızca Unity işlerinde okunur.
Skill çevrimdışı anlaşılır ve uygulanabilir; bir siteyi açmayı veya bir kavram listesini
tamamlamayı gerektirmez. Başka motorlarda o projenin mevcut araçlarını kullanır.

## Kurulum

`skills/gamedev` klasörünü **bütün içeriğiyle** aşağıdaki hedefe kopyalayın:

| Araç | Proje içindeki hedef | Çağrı |
| --- | --- | --- |
| Codex | `.agents/skills/gamedev/` | `$gamedev` |
| Claude Code | `.claude/skills/gamedev/` | `/gamedev` |

Kişisel kullanım için hedefleri sırasıyla `~/.agents/skills/gamedev/` ve
`~/.claude/skills/gamedev/` kullanın. Tek paket, otomatik seçim; API anahtarı, MCP veya
çalıştırılacak kurulum betiği gerektirmez. Görünmüyorsa oturumu yeniden başlatın.
Kurulum biçimi [Codex](https://learn.chatgpt.com/docs/build-skills) ve
[Claude Code](https://code.claude.com/docs/en/skills) belgeleriyle uyumludur.

## Örnek istekler

```text
$gamedev Ağır ama duyarlı bir hareket istiyorum; mevcut kontrolcüyü koruyup durma ve yön değiştirme hissini iyileştir.
/gamedev İnşa etmek tatmin etmiyor; ödeme, yerleşim, geri bildirim ve sonraki seçim döngüsünü inceleyip küçük bir iyileştirme uygula.
$gamedev Bu prototipte ilk oynanabilir döngüyü tamamla; bir eylem, anlamlı sonucu ve tekrar deneme yolu olsun.
/gamedev Şehir kurma oyunumdaki seçimler birbirine benziyor; dosyaları değiştirmeden mevcut sistemlerle sınanabilecek tek bir tasarım deneyi çıkar.
```

## Doğrulama

[Test kaydı](tests/README.md) gerçek yürütme ile tasarım değerlendirmesini ayırır.
WalkingCity önceki testlerde üç davranış hatasını ortaya çıkardı; oyun kaynakları kalıcı
olarak değiştirilmedi ve oyun reposuna commit atılmadı. Claude Code çalışma oturumu
bu ortamda çalıştırılmadı; uyumluluğu ortak dosya biçimi ve bağımsız yönergeler üzerinden sağlanır.
