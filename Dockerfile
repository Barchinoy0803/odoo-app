FROM odoo:17

RUN mkdir -p /mnt/extra-addons && \
    chown -R odoo:odoo /mnt/extra-addons && \
    chown -R odoo:odoo /var/lib/odoo

COPY ./config/odoo.conf /etc/odoo/
COPY ./addons /mnt/extra-addons

USER odoo

CMD ["odoo"]