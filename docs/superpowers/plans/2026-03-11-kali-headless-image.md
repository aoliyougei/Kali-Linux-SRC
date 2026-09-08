# Kali Headless Image Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Kali Linux image containing `kali-linux-headless` and `kali-tools-top10`, tagged with the installed `kali-linux-headless` package version.

**Architecture:** A single reproducible `Dockerfile` extends `kalilinux/kali-rolling:latest`, uses the Tsinghua TUNA Kali mirror, installs both metapackages, and removes APT indexes. Docker API operations build a temporary image, inspect installed packages in a temporary container, and add the final `kali-linux-headless:<version>` tag.

**Tech Stack:** Dockerfile, APT, dpkg-query, pi-docker-api

**Spec:** `docs/superpowers/specs/2026-03-11-kali-headless-image-design.md`

## Global Constraints

- Base image: `kalilinux/kali-rolling:latest`.
- Install `kali-linux-headless` and `kali-tools-top10` non-interactively.
- Final image name: `kali-linux-headless:<installed kali-linux-headless package version>`.
- Use pi-docker-api for builds and runtime verification; do not use the local Docker CLI.
- Use `http://mirrors.tuna.tsinghua.edu.cn/kali` because HTTPS certificate validation failed in the build environment; retain APT repository signature verification.
- Do not add entrypoints, other extra configuration, or package pinning.

---

### Task 1: Build, tag, and verify the image

**Files:**
- Create: `Dockerfile`

**Interfaces:**
- Consumes: `kalilinux/kali-rolling:latest` from the local Docker daemon or registry.
- Produces: daemon-local image `kali-linux-headless:<version>` and a reproducible `Dockerfile`.

- [ ] **Step 1: Create the Dockerfile**

```dockerfile
FROM kalilinux/kali-rolling:latest

RUN printf '%s\\n' 'deb http://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware' > /etc/apt/sources.list \
 && rm -f /etc/apt/sources.list.d/kali.sources \
 && apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      kali-linux-headless \
      kali-tools-top10 \
 && rm -rf /var/lib/apt/lists/*
```

- [ ] **Step 2: Build a temporary image through pi-docker-api**

Build the current project directory with tag:

```text
kali-linux-headless:build
```

Expected: Docker API build completes successfully.

- [ ] **Step 3: Read and validate installed package versions**

Create and start a temporary container from `kali-linux-headless:build`, then execute:

```sh
dpkg-query -W -f='${Package}\t${Version}\t${db:Status-Abbrev}\n' kali-linux-headless kali-tools-top10
```

Expected: both lines end in `ii ` and the `kali-linux-headless` line provides a non-empty version accepted as a Docker tag.

- [ ] **Step 4: Add the final version tag**

Use pi-docker-api to tag the temporary image as:

```text
kali-linux-headless:<version-from-step-3>
```

Expected: the final daemon-local tag exists and refers to the same image ID as `kali-linux-headless:build`.

- [ ] **Step 5: Clean up temporary resources**

Remove the temporary container and remove only the `kali-linux-headless:build` tag. Preserve `kali-linux-headless:<version>`.

Expected: no task-owned container or temporary image tag remains.

- [ ] **Step 6: Commit the reproducible build definition**

```sh
git add Dockerfile docs/superpowers/plans/2026-03-11-kali-headless-image.md
git commit -m "build: add Kali headless tools image"
```
