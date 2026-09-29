# Project conventions

## Language
- Write all code in English: identifiers, comments, docstrings, log messages and commit messages.
- Replies to the user in chat can stay in Portuguese.

## Commit messages
Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>(<optional scope>): <description>

<optional body>

<optional footer(s)>
```

- **Types:**
  - `feat`: a new feature
  - `fix`: a bug fix
  - `refactor`: a code change that neither fixes a bug nor adds a feature
  - `perf`: a performance improvement
  - `style`: formatting only, with no change in behavior
  - `test`: adding or updating tests
  - `docs`: documentation only
  - `build`: changes to packaging, dependencies, the PyInstaller spec or version bumps
  - `ci`: CI configuration
  - `chore`: other maintenance
- **Scope** is optional and names the area touched, matching the package layout under `src/holdings_tracker_desktop/`: `ui`, `models`, `repositories`, `services`, `schemas`, `database`, `alembic`, `config`, `utils`. It can also name a specific widget, e.g. `feat(assets-widget): ...`.
- **Description:** imperative mood, lowercase first letter, no trailing period, at most about 72 characters (e.g. `fix(ui): keep table header sizes after refresh`).
- **Body** (optional): explain what changed and why, wrapped at 72 characters and separated from the header by a blank line.
- **Breaking changes:** add `!` after the type/scope (`feat(models)!: ...`) and a `BREAKING CHANGE: <explanation>` footer.
- One logical change per commit. Commit a version bump on its own as `build: bump version to X.Y.Z` instead of mixing it into a feature commit.
