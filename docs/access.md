# Documentation

## 🌐 Documentation en ligne
- **[Docsify Documentation](https://jefraudai-docsify.hf.space/)** - Documentation technique complète
- **[Slidev Présentations](https://jefraudai-slidev.hf.space/)** - Slides de présentation

## 📝 Documentation Markdown avec schemas Mermaid

- **[Services/docsify/README.md](../Services/docsify/README.md)** - README du service docsify
- **[Services/slidev/slides.md](../Services/slidev/slides.md)** - Source des présentations Slidev

## 💻 Documentation en accès Local

Si les HuggingFace Spaces sont en pause ou indisponibles, vous pouvez accéder aux services localement:

### Documentation Docsify
```bash
cd Services/docsify
npm install -g docsify-cli docsify-mermaid
docsify serve docs --port 7860 --open
```
Ou avec Docker:
```bash
cd Services/docsify
docker build -t jefraudai-docs .
docker run -p 7860:7860 jefraudai-docs
```
Puis ouvrez: http://localhost:7860

### Présentations Slidev
```bash
cd Services/slidev
npm install
npm run dev
```
Puis ouvrez l'URL affichée (généralement http://localhost:3030)