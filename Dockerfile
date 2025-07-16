FROM odoo:17

COPY ./config/odoo.conf /etc/odoo/odoo.conf
COPY ./addons /mnt/extra-addons
