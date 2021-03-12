set -x DJANGO_SETTINGS_MODULE app.settings.dev
set -x TENTACOOL_DEV_SECRET_KEY (tr -cd 'a-zA-Z0-9' < /dev/urandom | fold -w 32 | head -n 1)
