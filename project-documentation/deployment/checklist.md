Here’s your deployment checklist as a **Markdown file** (`deployment-checklist.md`):

````markdown
# Deployment Checklist – LLM Chatbot Service on EC2 (`c7i-flex.large`)

## 1. EC2 Setup
- [ ] **Launch EC2 Instance**
  - Type: `c7i-flex.large` (2 vCPU, 4GB RAM)
  - OS: Ubuntu 22.04 LTS
  - Storage: 30–50 GB gp3
  - Key pair: Created and downloaded
  - Security group:
    - [ ] Allow SSH (22) from **your IP only**
    - [ ] Allow HTTP (80)
    - [ ] Allow HTTPS (443)

- [ ] **SSH into EC2**
  ```bash
  ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
````

* [ ] **Update Packages**

  ```bash
  sudo apt update && sudo apt upgrade -y
  ```

* [ ] **Install Essentials**

  ```bash
  sudo apt install -y git make curl unzip
  ```

* [ ] **Set Up SSH Keys for Git**

  * Generate key:

    ```bash
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```
  * Add the public key (`~/.ssh/id_ed25519.pub`) to GitHub/Bitbucket SSH keys.
  * Test connection:

    ```bash
    ssh -T git@github.com
    ```

---

## 2. Docker & Compose

* [ ] **Install Docker**

  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker $USER
  ```

  *(Log out & log back in to apply group change)*

* [ ] **Install Docker Compose Plugin**

  ```bash
  DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
  mkdir -p $DOCKER_CONFIG/cli-plugins
  curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
    -o $DOCKER_CONFIG/cli-plugins/docker-compose
  chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
  ```

* [ ] **Verify Installation**

  ```bash
  docker --version
  docker compose version
  ```

---

## 3. Application Deployment

* [ ] **Clone Repo via SSH**

  ```bash
  git clone git@github.com:username/repo.git
  cd repo
  ```

* [ ] **Configure Environment Variables**

  * Copy `.env.example` to `.env`
  * Set production API keys & DB credentials

* [ ] **Set Docker Resource Limits** (in `docker-compose.yml`)

  ```yaml
  deploy:
    resources:
      limits:
        cpus: '0.5'
        memory: 512M
  ```

* [ ] **Start Services**

  ```bash
  docker compose up -d --build
  ```

* [ ] **Check Logs**

  ```bash
  docker compose logs -f
  ```

---

## 4. Security & Monitoring

* [ ] **Enable UFW Firewall**

  ```bash
  sudo ufw allow OpenSSH
  sudo ufw allow 80
  sudo ufw allow 443
  sudo ufw enable
  ```

* [ ] **Set Swap (2GB)**

  ```bash
  sudo fallocate -l 2G /swapfile
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
  ```

* [ ] **Install CloudWatch Agent** for CPU/memory monitoring

---

## 5. Post-Deployment

* [ ] Test all API endpoints
* [ ] Test DB connectivity
* [ ] Check logs for errors
* [ ] Create snapshot/AMI backup

```

---

Do you want me to **also create the one-shot bash installer** that executes *most of this checklist automatically* so you can deploy without doing each step manually? That way you’d just upload the `.md` for docs and run the `.sh` for setup.
```
