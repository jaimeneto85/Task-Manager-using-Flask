# Branching & CI/CD (GitFlow)

The same code runs in every environment — only configuration (`APP_ENV` + secrets)
differs. Branches are **promotion stages**; you never edit code per-branch.

## Long-lived branches (these deploy)

| Branch        | Role            | On push                                            |
|---------------|-----------------|----------------------------------------------------|
| `main`        | Production      | CI + CD → deploy to **production** (manual approval)|
| `staging`     | Pre-production  | CI + CD → deploy to **staging**                    |
| `development` | Integration     | CI + CD → deploy to **development**                |

## Short-lived branches (CI only — they never deploy)

These are **naming prefixes**, one branch per task, branched off `development`
and deleted after merge. `feature` and `bugfix` are *not* single branches.

| Prefix      | Use                                         | Example                      |
|-------------|---------------------------------------------|------------------------------|
| `feature/*` | New functionality                           | `feature/security-headers`   |
| `bugfix/*`  | Bug fixes (the "bugs" branches)             | `bugfix/idor-task-delete`    |
| `hotfix/*`  | Urgent production fix (branched off `main`) | `hotfix/login-crash`         |

## Flow

```
feature/* , bugfix/*  ──PR──►  development  ──►  staging  ──►  main
                                (deploy dev)    (deploy stg)  (deploy prod, approval)
```

## Working on a change

```bash
git checkout development && git pull
git checkout -b feature/my-thing          # or bugfix/my-thing
# ...commit your work...
git push -u origin feature/my-thing
# open a Pull Request into development
```

Every push and PR runs the full pipeline: **tests + coverage, Bandit (SAST),
OWASP Dependency-Check (SCA), OWASP ZAP (DAST)**. The deploy jobs run only on
`development` / `staging` / `main`.

## Promoting & releasing

Promote by merging forward (`development → staging → main`), then tag on `main`:

```bash
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

The version flows: **git tag → `APP_VERSION` build arg → `app_info` metric → Grafana**,
so each environment reports the exact version it is running.

## Continuous Delivery

On a push to a deploy branch, the reusable workflow `.github/workflows/deploy.yml`:

1. builds the versioned Docker image (`--build-arg APP_VERSION=$(git describe --tags)`),
2. pushes it to **GHCR** as
   `ghcr.io/<owner>/task-manager-using-flask:<version>` and `:<environment>`,
3. rolls it out (placeholder — wire your real target: k8s / compose / ssh).

Production is gated by the **`production`** GitHub Environment's required reviewer,
so prod deploys pause for manual approval — Continuous *Delivery*.

### One-time setup

- Create the GitHub **Environments** `development`, `staging`, `production`
  (Settings → Environments); add a **required reviewer** to `production`.
- Add the environment-scoped secrets **`SECRET_KEY`** and **`DATABASE_URI`**.
- Add the repository secret **`NVD_API_KEY`** (for Dependency-Check).
