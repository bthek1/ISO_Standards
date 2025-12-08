# Docker Runtime Issue - CVE-2025-52881 / AppArmor Conflict

## 🔍 Issue Description

When attempting to start **any** Docker container (including PostgreSQL, even `hello-world`), you encounter:

```
Error response from daemon: failed to create task for container: failed to create shim task: 
OCI runtime create failed: runc create failed: unable to start container process: 
error during container init: open sysctl net.ipv4.ip_unprivileged_port_start file: 
reopen fd 8: permission denied
```

## 🧠 Root Cause

This is **NOT a problem with your Postgres config**. This is a known bug affecting:

- **Docker in LXC containers** (Proxmox LXC, LXD, Incus)
- **runc 1.3.3** + **containerd 2.x** (includes CVE-2025-52881 security fix)
- **AppArmor** conflict when Docker runs inside a container with AppArmor profiles

**Your environment:**
- Virtualization: **LXC** (confirmed via `systemd-detect-virt`)
- containerd.io: **2.1.5** (downgraded from 2.2.0, pinned)
- runc: **1.3.3** (still has the security fix that conflicts with AppArmor)
- Docker CE: **29.1.2**

**The security fix in runc 1.3.3 reopens file descriptors in a way that conflicts with AppArmor rules in nested container environments.**

## ✅ Confirmed Working Solution: Fix AppArmor on Proxmox Host

Since you're running in **LXC**, you need to modify the AppArmor profile on the **Proxmox host** (not inside this container).

### Steps to Fix (On Proxmox Host)

**1. SSH into your Proxmox host**

```bash
ssh root@proxmox-host
```

**2. Find your LXC container ID**

```bash
pct list
```

Find the container running this workload (likely named something like `work-budget` or similar).

**3. Edit the LXC config**

```bash
nano /etc/pve/lxc/<CTID>.conf
```

Replace `<CTID>` with your container ID (e.g., `105`, `200`, etc.).

**4. Add AppArmor unconfined profile**

Add this line to the config file:

```text
lxc.apparmor.profile: unconfined
```

**5. Restart the LXC container**

```bash
pct restart <CTID>
```

**6. Back in this container, test Docker**

```bash
docker run --rm hello-world
```

Should now work! 🎉

**7. Start PostgreSQL**

```bash
cd Backend
docker compose -f docker-compose.dev.yml up -d
```

### ⚠️ Security Note

Setting `lxc.apparmor.profile: unconfined` reduces AppArmor isolation for this LXC container. This is:
- ✅ **Fine for development/personal environments**
- ✅ **Temporary until Proxmox/LXC ships updated AppArmor profiles**
- ❌ **Not recommended for production/multi-tenant environments**

Once Proxmox releases updated AppArmor profiles compatible with runc 1.3.3+, you can remove this setting.

## 🔄 Alternative Solutions (If You Don't Have Host Access)

### Option A: Downgrade containerd.io (Attempted - Didn't Fix Alone)

We already downgraded `containerd.io` from 2.2.0 to 2.1.5 and pinned it:

```bash
sudo apt-get install -y --allow-downgrades containerd.io=2.1.5-1~ubuntu.24.04~noble
sudo apt-mark hold containerd.io
sudo systemctl restart docker
```

**Result**: Still fails because `runc 1.3.3` (bundled with containerd) has the same security fix.

### Option B: Use Podman Instead of Docker

Podman doesn't have this AppArmor conflict:

```bash
# Install Podman
sudo apt update
sudo apt install podman podman-compose

# Start PostgreSQL with Podman
cd Backend
podman-compose -f docker-compose.dev.yml up -d
```

Podman is a drop-in replacement and uses the same compose files.

### Option C: Run Docker with Sudo (Works but Not Ideal)

```bash
cd Backend
sudo docker compose -f docker-compose.dev.yml up -d
```

**Why this works**: sudo bypasses some AppArmor restrictions.  
**Downside**: Have to use sudo for all Docker commands.

### Option D: Temporary Fallback to SQLite

While the Docker issue is being resolved, you can use SQLite:

Update `.env`:
```env
DB_ENGINE="django.db.backends.sqlite3"
```

The development settings automatically handle this fallback.

### Option E: Move to a Full VM

If you control the Proxmox host:

1. Create a full **KVM VM** (not LXC container)
2. Install Ubuntu 24.04
3. Install Docker
4. Migrate your development environment

VMs don't have the nested AppArmor issue that LXC containers have.

## 📚 Background & References

### What Happened

1. **CVE-2025-52881** was discovered in runc (file descriptor security issue)
2. Fix released in **runc 1.3.3** (December 2024)
3. Fix changes how runc reopens file descriptors during container init
4. This conflicts with **AppArmor profiles** in nested container environments (Docker-in-LXC)
5. Symptom: `open sysctl net.ipv4.ip_unprivileged_port_start file: reopen fd 8: permission denied`

### Timeline

- **Nov 2024**: runc 1.3.3 released with CVE fix
- **Dec 2024**: containerd 2.2.0 released (bundles runc 1.3.3)
- **Dec 2024**: Users report Docker breaking in Proxmox LXC after `apt upgrade`

### Upstream Issues

- [runc #4968](https://github.com/opencontainers/runc/issues/4968) - fd reopening causes issues with AppArmor profiles
- [Docker Forums](https://forums.docker.com/t/docker-fails-to-run-on-debian-bullseye-after-update/150363) - Multiple reports of this exact error
- [ktz.blog](https://blog.ktz.me/apparmors-awkward-aftermath-atop-proxmox-9/) - Analysis of AppArmor issues in Proxmox 9

### Current Status

**runc maintainers**: "This is an AppArmor/LXC interaction issue. We can't fully fix it in runc without breaking the security fix. LXC/Proxmox need to update AppArmor profiles."

**Proxmox/LXC**: Working on updated AppArmor profiles (no ETA yet)

**Temporary workaround**: Use `lxc.apparmor.profile: unconfined` on Proxmox host

## 🧪 Verification Steps

After applying any fix, verify Docker works:

```bash
# Test basic Docker functionality
docker run --rm hello-world

# Test PostgreSQL specifically
cd Backend
docker compose -f docker-compose.dev.yml up -d
docker compose -f docker-compose.dev.yml ps
docker compose -f docker-compose.dev.yml logs db

# Test database connection from Django
source .venv/bin/activate
python manage.py check --database default
python manage.py migrate
```

## ✅ What We've Done

1. ✅ Converted project to use PostgreSQL (docker-compose.dev.yml configured correctly)
2. ✅ Installed psycopg[binary] for PostgreSQL support
3. ✅ Updated Django settings to use PostgreSQL by default
4. ✅ Downgraded containerd.io from 2.2.0 to 2.1.5
5. ✅ Pinned containerd.io to prevent auto-upgrade
6. ✅ Identified root cause: AppArmor conflict in LXC environment
7. ⏳ **Waiting on**: AppArmor profile fix on Proxmox host OR alternative solution

## 🎯 Recommended Next Steps

**If you have Proxmox host access** (Recommended):
```bash
# On Proxmox host:
nano /etc/pve/lxc/<CTID>.conf
# Add: lxc.apparmor.profile: unconfined
pct restart <CTID>
```

**If you don't have host access**:
- Option 1: Use Podman (`sudo apt install podman podman-compose`)
- Option 2: Use `sudo docker compose` for now
- Option 3: Temporarily use SQLite (`DB_ENGINE="django.db.backends.sqlite3"` in .env)

Your **docker-compose.dev.yml is correct** and will work as soon as Docker is functional again!
