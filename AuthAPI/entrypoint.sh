#!/bin/sh
python3 cli_create_super_user.py $ADMIN_LOGIN $ADMIN_PASSWORD $ADMIN_EMAIL &&
exec "$@"
