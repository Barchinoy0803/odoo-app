FROM odoo:17

COPY ./config/odoo.conf /etc/odoo/odoo.conf
COPY ./addons /mnt/extra-addons

CMD ["odoo", "-i", "base", "-d", "odoo_app", "--without-demo=all"]
