# Assignment 1: Inspecting the Cultural Web

## Site investigated

**By the People** — <https://crowd.loc.gov/>  
**Source repository:** <https://github.com/LibraryOfCongress/concordia>

By the People is the Library of Congress's public platform for crowdsourcing transcription and tags for digitized manuscript and typed materials. I selected it because it connects cultural objects with public participation: volunteers help make handwritten archival materials readable and searchable. The platform's completed text is subsequently published with the associated object records on loc.gov.

## What I found in the browser and source code

I opened the public site in a browser, but the session was stopped at Cloudflare's automated security-verification screen; I did not try to bypass it. I then inspected the linked public repository, which identifies `crowd.loc.gov` as the first Library of Congress implementation of the **Concordia** platform. The repository makes the site's construction much easier to assess than browser inspection alone:

| Technology | Evidence | What it appears to do |
| --- | --- | --- |
| HTML | The repository is reported as including HTML, and its Django application contains page templates. | Provides the document structure and form controls for transcription and tagging work. |
| CSS / SCSS | The project has a `static` folder and style tooling, including Sass and Stylelint. | Controls the page layout, typography, colors, and responsive interface. SCSS is a stylesheet language that is compiled into browser-ready CSS. |
| JavaScript | The repository has a `frontend` folder, `vite.config.js`, and a `package.json`. Its front-end dependencies include Bootstrap, jQuery, Chart.js, CodeMirror, and OpenSeadragon. | Adds interactive controls such as transcription editing, charts, image viewing, and split-pane interfaces. Vite builds the front-end assets. |
| Python / Django | The project's README describes Concordia as a containerized Python–Django application; the repository also includes `manage.py`, `Pipfile`, and `docker-compose.yml`. | Runs the server-side application, stores and serves project data, and connects the public interface to Library of Congress collection metadata. |
| Other files | `Dockerfile`, CloudFormation configuration, CI workflow files, `package-lock.json`, and database-related folders are also present. | These are development, deployment, dependency-locking, and infrastructure files rather than pages viewed directly in a browser. |

The project therefore uses all three core web technologies named in the prompt (HTML, CSS, and JavaScript), but it is not just a static website: it is a server-backed, containerized application. The README says that it uses the public loc.gov API to obtain collection metadata and JPEG images. The published project files also show a recent front-end build process rather than a hand-authored collection of only `.html` files.

## Who built it?

The primary builder is the **Library of Congress**: the repository is published by the `LibraryOfCongress` GitHub organization, and the README says that LOC developed Concordia and launched its first implementation, By the People, in October 2018. The project is supported by the National Digital Library Trust Fund.

It was clearly a multi-person project. A 2019 account by the Concordia team says that, six weeks before launch, the core project team had **seven people**: a Technical Lead, a Product Owner/Program Lead, a Product Manager/Community Manager, a Senior IT Specialist, two additional community managers, and a part-time Designer/UX expert. The project also had a stakeholder group of **six Library representatives** and an outside vendor team whose size is not stated. I can therefore document **at least 13 Library participants, plus the vendor team**, during the launch period. This is a historical launch-team count, not a claim about current staffing.

The repository's thousands of commits and its division into back-end, front-end, infrastructure, testing, and documentation work provide additional evidence of sustained collaboration. The site also depends on many volunteers: according to the README, each completed transcription requires at least one person to transcribe it and at least one other person to review it.

## Sources consulted

- [Concordia / By the People repository README](https://github.com/LibraryOfCongress/concordia)
- [Concordia `package.json`](https://github.com/LibraryOfCongress/concordia/blob/main/package.json)
- [“With One Heart”: Agile approaches for developing Concordia (Code4Lib Journal)](https://journal.code4lib.org/articles/14901)
- [Library of Congress: Rosa Parks Papers collection](https://www.loc.gov/collections/rosa-parks-papers/about-this-collection/)
- [Library of Congress: "Seating arrangements—Mrs. Rosa Parks" item record](https://www.loc.gov/pictures/item/94505572/)
- [Library of Congress: New York World-Telegram and the Sun photograph collection](https://www.loc.gov/pictures/item/94505083/)

## Connection to Assignment 2

The accompanying `index.html` presents the Library of Congress photograph *Seating arrangements—Mrs. Rosa Parks* as a single digitized cultural object. It uses the original item record for the image credit, description, and metadata, and links to that record, the original New York World-Telegram and the Sun photograph collection, and the related Rosa Parks Papers collection.
