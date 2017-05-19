from blog import app
from flask.ext.principal import Principal, Permission, RoleNeed, ActionNeed, identity_loaded

principals = Principal(app, skip_static=True)

be_admin = RoleNeed('admin')
be_user = RoleNeed('user')
user = Permission(be_user)
admin = Permission(be_admin)
apps_needs = [be_admin, be_user]
apps_permissions = [user, admin]


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    needs = []
    if identity.auth_type in ('user', 'admin'):
        needs.append(be_user)
    if identity.auth_type == 'admin':
        needs.append(be_admin)
    for n in needs:
        identity.provides.add(n)

