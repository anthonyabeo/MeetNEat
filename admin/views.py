from flask import render_template, redirect, url_for

from admin import admin_blueprint as admin


@admin.route('/login/')
def login_in():
    return render_template('admin/login.html')


@admin.route('/logout/')
def logout():
    return redirect(url_for('admin.index'))


@admin.route('/admin/dashboard/<int:admin_id>/')
def index(admin_id):
    return render_template('admin/index.html', admin_id=admin_id)

