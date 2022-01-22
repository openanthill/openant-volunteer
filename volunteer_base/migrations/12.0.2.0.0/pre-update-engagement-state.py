# -*- coding: utf-8 -*-

def migrate(cr, version):
    mapping = {
        'new': '10-new',
        'active': '20-active',
        'onhold': '30-onhold',
        'success': '40-success',
        'cancel': '50-cancel',
    }

    for key, val in mapping.items():
        sql = """UPDATE volunteer_engagement
              SET state = '%s'
            WHERE state = '%s'
              """ %(val, key)
        cr.execute(sql)
