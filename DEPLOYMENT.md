# TTCP Worldwide - Deployment Guide

This guide covers deploying TTCP Worldwide to various cloud platforms.

## 📋 Pre-Deployment Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Generate a secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up a PostgreSQL database
- [ ] Configure `CSRF_TRUSTED_ORIGINS` for HTTPS
- [ ] Run `python manage.py collectstatic`
- [ ] Run `python manage.py migrate`
- [ ] Create a superuser for admin access

---

## 🔐 Generate a Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🚀 Deployment Options

### Option 1: Render.com (Recommended - Free Tier Available)

1. **Push code to GitHub**
2. **Create a new Web Service on Render**
   - Connect your GitHub repo
   - Render will auto-detect `render.yaml`
3. **Set Environment Variables** in Render dashboard:
   ```
   SECRET_KEY=your-generated-secret-key
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com,yourdomain.com
   ```
4. **Database**: Render will create a PostgreSQL database automatically

**Manual Deploy:**
```bash
# render.yaml is already configured
git push origin main
```

---

### Option 2: Railway.app

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Initialize Project**
   ```bash
   railway init
   railway link
   ```

3. **Add PostgreSQL**
   ```bash
   railway add --plugin postgresql
   ```

4. **Set Environment Variables**
   ```bash
   railway variables set SECRET_KEY="your-secret-key"
   railway variables set DEBUG="False"
   railway variables set ALLOWED_HOSTS=".railway.app,yourdomain.com"
   ```

5. **Deploy**
   ```bash
   railway up
   ```

---

### Option 3: Fly.io

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   fly auth login
   ```

2. **Create App**
   ```bash
   fly launch --no-deploy
   ```

3. **Create PostgreSQL Database**
   ```bash
   fly postgres create --name ttcp-db
   fly postgres attach ttcp-db
   ```

4. **Set Secrets**
   ```bash
   fly secrets set SECRET_KEY="your-secret-key"
   fly secrets set DEBUG="False"
   ```

5. **Deploy**
   ```bash
   fly deploy
   ```

---

### Option 4: Heroku

1. **Install Heroku CLI**
   ```bash
   # Windows
   winget install Heroku.HerokuCLI
   
   heroku login
   ```

2. **Create App**
   ```bash
   heroku create ttcp-worldwide
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:essential-0
   ```

4. **Set Config Vars**
   ```bash
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DEBUG="False"
   heroku config:set ALLOWED_HOSTS=".herokuapp.com,yourdomain.com"
   ```

5. **Deploy**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

---

### Option 5: Docker (Self-Hosted / VPS)

1. **Build Image**
   ```bash
   docker build -f Dockerfile.prod -t ttcp-worldwide .
   ```

2. **Run with Docker Compose**
   ```bash
   # Create .env file with your settings
   cp .env.example .env
   # Edit .env with your values
   
   # Start services
   docker-compose up -d web-prod postgres
   
   # Run migrations
   docker-compose exec web-prod python manage.py migrate
   docker-compose exec web-prod python manage.py createsuperuser
   ```

3. **With Nginx (Production)**
   ```bash
   docker-compose --profile production up -d
   ```

---

### Option 6: DigitalOcean App Platform

1. **Connect GitHub repo** in DigitalOcean dashboard
2. **Select "Dockerfile" as build type**
3. **Configure Environment Variables**:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS`
   - `DATABASE_URL` (from managed database)
4. **Deploy**

---

## 🗄️ Database Migration

After deploying, always run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

For Docker:
```bash
docker-compose exec web-prod python manage.py migrate
docker-compose exec web-prod python manage.py createsuperuser
```

---

## 🔧 Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SECRET_KEY` | ✅ | Django secret key | `your-50-char-random-string` |
| `DEBUG` | ✅ | Debug mode | `False` |
| `ALLOWED_HOSTS` | ✅ | Comma-separated domains | `yourdomain.com,www.yourdomain.com` |
| `DATABASE_URL` | ⚠️ | Database connection URL | `postgres://user:pass@host:5432/db` |
| `CSRF_TRUSTED_ORIGINS` | ⚠️ | HTTPS origins for CSRF | `https://yourdomain.com` |

---

## 🌐 Custom Domain Setup

1. **Add domain to `ALLOWED_HOSTS`**
2. **Add to `CSRF_TRUSTED_ORIGINS`** (with https://)
3. **Configure DNS** to point to your hosting provider
4. **Enable SSL/HTTPS** (usually automatic with cloud providers)

---

## 📊 Monitoring & Logs

**Render:**
```bash
# View in dashboard or use CLI
render logs
```

**Railway:**
```bash
railway logs
```

**Fly.io:**
```bash
fly logs
```

**Heroku:**
```bash
heroku logs --tail
```

**Docker:**
```bash
docker-compose logs -f web-prod
```

---

## 🔄 CI/CD with GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:
1. Runs tests on every push/PR
2. Builds Docker image
3. (Optional) Deploys to your hosting provider

To enable auto-deploy, add your platform's API token to GitHub Secrets and uncomment the deploy job.

---

## 🛡️ Security Checklist

- [x] `DEBUG=False` in production
- [x] Strong `SECRET_KEY`
- [x] HTTPS enabled (`SECURE_SSL_REDIRECT=True`)
- [x] Secure cookies (`SESSION_COOKIE_SECURE=True`)
- [x] HSTS enabled
- [x] CSRF protection
- [x] XSS protection
- [ ] Regular dependency updates
- [ ] Database backups configured
- [ ] Rate limiting (via Nginx or cloud provider)

---

## 📞 Support

For deployment issues, check:
1. Application logs
2. Database connection
3. Environment variables
4. Static files serving

Common issues:
- **500 Error**: Check `DEBUG=True` temporarily to see error details
- **Static files not loading**: Run `collectstatic` and check `STATIC_ROOT`
- **Database errors**: Verify `DATABASE_URL` format and connectivity
