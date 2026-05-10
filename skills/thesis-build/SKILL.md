# thesis-build — Academix v13.2 Thesis Assembly Pipeline

Builds a complete BTS-format thesis PDF from markdown source with Algerian academic formatting, proper hierarchy, TOC, and user's custom design system.

## When to Load

- Building/rebuilding thesis PDF
- Fixing formatting, table colors, RTL, page de garde
- Adding TOC, list of tables/figures, annexes

## Architecture

```
Source MD → customize-reference.py (user DOCX styles + H1/H2/H3) → pandoc → format-tables.py (post-process) → format-cover.py (cover styling) → Word → PDF
```

## Keywords
thesis, build, pdf, docx, memoire, pipeline, pfe, soutenance

## File Layout

| Path | Purpose |
|------|---------|
| `Thesis_Surgical_Edit/Final_Thesis_Academix_v13_2_FIXED.md` | Master thesis source (2,193 lines, 44 tables) |
| `Thesis_Surgical_Edit/build-thesis.ps1` | Build pipeline (7 steps) |
| `Thesis_Surgical_Edit/style/customize-reference.py` | Style copier from user DOCX + heading styles |
| `Thesis_Surgical_Edit/style/format-tables.py` | Table post-processor |
| `Thesis_Surgical_Edit/style/format-cover.py` | Cover page formatter (colors, fonts from reference DOCX) |
| `Thesis_Surgical_Edit/THESIS_CHAPTER_OUTLINE.md` | Chapter structure outline |
| `Thesis_Surgical_Edit/REVIEW_REPORT.md` | Surgical edit report |
| `Thesis_Surgical_Edit/SESSION_HANDOFF.md` | Full session state for model handoff |
| `Thesis_Surgical_Edit/output/` | Generated DOCX + PDF |

## Ground Truth Constants (NEVER MODIFY)

| Symbol | Value | Meaning |
|--------|-------|---------|
| D | 1,546 | Annual demand (units) |
| Q* | 176 | Economic Order Quantity |
| ROP | 205.6 | Reorder Point |
| SS | 200 | Safety Stock |
| LT | 2 | Lead Time (days) |
| S | 500 DZD | Order cost |
| I | 20% | Holding rate |

## Thesis Structure (20 Components)

1. Cover page (page de garde)
2. Bismillah
3. Dedication (إهداء)
4. Acknowledgments (شكر وتقدير)
5. Arabic abstract (ملخص)
6. French résumé
7. English abstract
8. Keywords (mots-clés)
9. Glossary (جدول المختصرات)
10. Table of contents (الفهرس)
11. List of tables (قائمة الجداول)
12. List of figures (قائمة الأشكال)
13. Chapter 1: الإطار النظري والمفاهيمي
14. Chapter 2: التشخيص والميدان
15. Chapter 3: التصميم والمنهجية
16. Chapter 4: النتائج والتقييم
17. Conclusion (الخاتمة)
18. Recommendations (التوصيات)
19. Bibliography (المراجع + 20 sources)
20. Annexes (6 annexes: file structure, VBA modules, field data, admin docs, LLM deployment, Algerian framework)

## Hierarchy Rules

- فصل → مبحث → مطلب → أولاً، ثانياً، ثالثاً...
- ❌ فرع is FORBIDDEN
- ❌ Database → ✅ السجل الرقمي
- ❌ Python/Backend → ✅ وحدات المعالجة VBA
- ❌ Hybrid System → ✅ نظام إلكتروني متكامل

## Design System (from reference DOCX)

| Element | Rule |
|---------|------|
| **Font** | Traditional Arabic 14pt (docDefaults) |
| **Page** | A4, 4cm margins all sides |
| **Direction** | RTL (dir=rtl metadata) |
| **Line spacing** | 1.5 |
| **Cover republic** | CENTER bold #1A1A1A |
| **Cover ministry** | CENTER bold #1A1A1A |
| **Cover diploma** | CENTER bold 18pt #1A1A1A (مذكرة تخرج) |
| **Cover subtitle** | CENTER bold 18pt #555555 (gray) |
| **Cover English** | CENTER bold 12pt #1F6B2E Times New Roman |
| **Cover student** | LEFT bold 12pt #1A1A1A |
| **Cover date** | LEFT bold 16pt #806000 (gold) |
| **Heading 1** | 22pt #1B2631 Bold (chapter titles) |
| **Heading 2** | 18pt #0C447C Bold (section titles) |
| **Heading 3** | 16pt #0C447C Bold (subsection titles) |
| **Table header** | Fill #0C447C, White bold text |
| **Table body (odd)** | Fill #EBF5FB |
| **Table body (even)** | No fill |

## Pipeline Commands

```powershell
# Full build
.\Thesis_Surgical_Edit\build-thesis.ps1

# Custom output
.\Thesis_Surgical_Edit\build-thesis.ps1 -SourceMD "my_draft.md" -OutputName "Memoire_v3"

# Force style rebuild (delete cached reference.docx)
Remove-Item Thesis_Surgical_Edit/style/reference.docx -Force
.\Thesis_Surgical_Edit\build-thesis.ps1
```

## Cover Colors Reference

| Element | Color | RGB |
|---------|-------|-----|
| Republic/ministry/diploma/section titles | #1A1A1A | 26,26,26 |
| Subtitle (gray) | #555555 | 85,85,85 |
| English title (green) | #1F6B2E | 31,107,46 |
| Date (gold) | #806000 | 128,96,0 |
| Heading 1 (dark navy) | #1B2631 | 27,38,49 |
| Heading 2/3 (deep blue) | #0C447C | 12,68,124 |
| Table headers | #0C447C | 12,68,124 |

## Prose Rules (Algerian Academic Arabic)

1. Formal register — avoid Egyptian/Lebanese colloquialisms
2. Use "المؤسسات العمومية" not "الشركات"
3. Every claim needs evidence (table, calculation, or reference)
4. Logical flow: problem → diagnosis → solution → verification
5. No AI/ML terminology
6. Excel/VBA justified as: "أدوات Office المتاحة مسبقاً في الإدارة الجزائرية"
7. Reference "CNEPD" standards for inventory management
8. Use Algerian dinar (دج) for all monetary values
9. Academic citations: (الاسم، السنة، الصفحة) format
10. No English/French terms without Arabic explanation

## Common Issues

| Issue | Fix |
|-------|-----|
| `{dir="rtl"}` brackets in output | Remove from markdown source |
| Table headers not colored | format-tables.py handles 44 tables |
| Cover formatting wrong | Edit format-cover.py or reference DOCX |
| Metadata artifacts (| chars) | Remove `--metadata` flags from build-thesis.ps1 |
| Heading styles missing | customize-reference.py adds H1/H2/H3; or convert markdown to use `# ` syntax |
| Reference DOCX stale | Delete style/reference.docx and rebuild |
