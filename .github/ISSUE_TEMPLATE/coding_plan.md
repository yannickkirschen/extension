---
name: Release
about: Coding Plan for a new release
title: ''
labels: ''
assignees: ''

---

This plan contains our work for **MONTH YEAR**. The next release (**VERSION**) will be published on **MONTH DAY, YEAR**.

During this coding period, we will ...

## Final

* Start: **MONTH DAY, YEAR**
* End: **MONTH DAY, YEAR**

## Plan for main development

### General
- [ ] 🏃 

### Documentation
- [ ] ...

## Plan for final

- [ ] Write/Execute tests
- [ ] Update changelog
- [ ] Write wiki pages (but not push them)
- [ ] Merge all relevant branches to `develop`
- [ ] Create `release/VERSION` branch
- [ ] Update `__version__`
- [ ] Merge `release` to master
- [ ] Merge `master` to develop
- [ ] Create tag `VERSION` on `master`
- [ ] Pull all changes on local machine
- [ ] Execute the script for uploading to PyPi
- [ ] Push wiki pages