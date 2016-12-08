from routewatch.DB.client import DB as database
from routewatch.UI import app
from routewatch.Security.crypto import get_secret, encrypt

DB = database()

from flask import request, redirect


@app.route('/')
def index():
    data = """
        <a href="/prefixes">Prefixes</a><br><a href="/prefixes/add">Add Prefix</a><br>
        <a href="/recipients">Recipients</a><br><a href="/recipients/add">Add Recipient</a><br>
        <a href="/settings">Settings</a><br>
    """
    return data


@app.route('/prefixes')
def prefixes():
    prefix_list = [
        '<form action="/prefixes/delete/{}" method="POST">{} <button>X</button></form>'.format(prefix.id, prefix.prefix)
        for prefix in DB.get("Prefix")]
    data = """
        <a href="/">Menu</a>
        <ul>
            {prefixes}
        </ul>
        <br>
        <a href="/prefixes/add">Add Prefix</a>
    """.format(prefixes="<br>".join(prefix_list))
    return data


@app.route('/prefixes/add', methods=["GET", "POST"])
def add_prefix():
    if request.method == 'POST':
        DB.create("Prefix", prefix=request.form["prefix"], protocol=request.form["protocol"])
        DB.commit()
        data = redirect("/prefixes")
    else:
        data = """
        <a href="/prefixes">Cancel</a>
        <form action="/prefixes/add" method="POST">
            Prefix: <input id="prefix" name="prefix" placeholder="0.0.0.0/0"></input> <br>
            Protocol: <input id="protocol" name="protocol" placeholder="4"></input> <br>
            <button>Add</button>
        </form>
    """
    return data


@app.route('/prefixes/delete/<id>', methods=["POST"])
def delete_prefix(ident):
    if request.method == 'POST':
        DB.delete("Prefix", id=ident)
        DB.commit()
        data = redirect("/prefixes")
        return data


@app.route('/recipients')
def recipients():
    recipient_list = [
        '<form action="/recipients/delete/{}" method="POST">{} <button>X</button></form>'.format(recipient.id,
                                                                                                 recipient.email) for
        recipient in DB.get("Recipient")]
    data = """
        <a href="/">Menu</a>
        <ul>
            {recipients}
        </ul>
        <br>
        <a href="/recipients/add">Add Recipient</a>
    """.format(recipients="<br>".join(recipient_list))
    return data


@app.route('/recipients/add', methods=["GET", "POST"])
def add_recipient():
    if request.method == 'POST':
        DB.create("Recipient", email=request.form["email"])
        DB.commit()
        data = redirect("/recipients")
    else:
        data = """
        <a href="/recipients">Cancel</a>
        <form action="/recipients/add" method="POST">
            Recipient: <input id="email" name="email" placeholder="your.name@example.com"></input> <br>
            <button>Add</button>
        </form>
    """
    return data


@app.route('/recipients/delete/<id>', methods=["POST"])
def delete_recipient(ident):
    if request.method == 'POST':
        DB.delete("Recipient", id=ident)
        DB.commit()
        data = redirect("/recipients")
        return data


@app.route('/settings')
def settings():
    settings_list = [
        '<form action="/settings/delete/{}" method="POST">{} <button>X</button></form>'.format(setting.id, setting.name)
        for setting in DB.get("Settings")]
    data = """
        <a href="/">Menu</a>
        <ul>
            {recipients}
        </ul>
        <br>
        <a href="/settings/add">Add Settings</a>
    """.format(recipients="<br>".join(settings_list))
    return data


@app.route('/settings/add', methods=["GET", "POST"])
def add_setting():
    if request.method == 'POST':
        encryption_requested = request.form.get("encrypt")
        print(encryption_requested)
        if encryption_requested:
            data = encrypt(request.form["data"].encode(), get_secret()).decode()
        else:
            data = request.form["data"]
        DB.create("Settings", name=request.form["name"], data=data)
        DB.commit()
        data = redirect("/settings")
    else:
        data = """
        <a href="/settings">Cancel</a>
        <form action="/settings/add" method="POST">
            Name: <input id="name" name="name" placeholder="e.g. lg_user"></input> <br>
            Encrypt: <input id="encrypt" name="encrypt" type="checkbox"></input> <br>
            Data: <input id="data" name="data" placeholder=""></input> <br>
            <button>Add</button>
        </form>
    """
    return data


@app.route('/settings/delete/<id>', methods=["POST"])
def delete_setting(ident):
    if request.method == 'POST':
        DB.delete("Settings", id=ident)
        DB.commit()
        data = redirect("/settings")
        return data
