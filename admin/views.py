from flask import render_template

from admin import admin_blueprint as admin


@admin.route('/admin/dashboard/')
def index():
    return render_template('admin/index.html')