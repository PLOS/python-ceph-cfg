# Python imports
import logging

# local modules
import model
import mdl_updater
import keyring
import utils
import mdl_query
import mdl_updater_remote


log = logging.getLogger(__name__)


class Error(Exception):
    """
    Error
    """

    def __str__(self):
        doc = self.__doc__.strip()
        return ': '.join([doc] + [str(a) for a in self.args])

def keyring_create_type(**kwargs):
    keyring_type = kwargs.get("keyring_type")
    if (keyring_type is None):
        raise Error("keyring_type is None")
    secret = kwargs.get("secret")
    m = model.model(**kwargs)
    u = mdl_updater.model_updater(m)
    u.hostname_refresh()
    u.defaults_refresh()
    u.load_confg(m.cluster_name)
    u.mon_members_refresh()
    keyobj = keyring.keyring_facard(m)
    keyobj.key_type = keyring_type
    return keyobj.create(secret=secret)


def keyring_present_type(**kwargs):
    """
    Check if keyring exists on disk

    CLI Example:

        salt '*' sesceph.keyring_admin_save \\
                '[mon.]\n\tkey = AQA/vZ9WyDwsKRAAxQ6wjGJH6WV8fDJeyzxHrg==\n\tcaps mon = \"allow *\"\n' \\
                'cluster_name'='ceph' \\
                'cluster_uuid'='cluster_uuid'
    Notes:

    cluster_uuid
        Set the cluster UUID. Defaults to value found in ceph config file.

    cluster_name
        Set the cluster name. Defaults to "ceph".
    keyring_type
        Set the keyring type
    """
    keyring_type = kwargs.get("keyring_type")
    if (keyring_type is None):
        raise Error("keyring_type is None")
    m = model.model(**kwargs)
    u = mdl_updater.model_updater(m)
    u.hostname_refresh()
    try:
        u.defaults_refresh()
    except:
        pass
    keyobj = keyring.keyring_facard(m)
    keyobj.key_type = keyring_type
    return keyobj.present()


def keyring_purge_type(**kwargs):
    keyring_type = kwargs.get("keyring_type", None)
    if (keyring_type is None):
        raise Error("keyring_type is not set")
    m = model.model(**kwargs)
    u = mdl_updater.model_updater(m)
    u.hostname_refresh()
    u.defaults_refresh()
    u.load_confg(m.cluster_name)
    u.mon_members_refresh()
    keyobj = keyring.keyring_facard(m)
    keyobj.key_type = keyring_type
    return keyobj.remove()


def keyring_save_type(**kwargs):
    keyring_type = kwargs.get("keyring_type")
    key_content = kwargs.get("key_content")
    secret = kwargs.get("secret")
    m = model.model(**kwargs)
    u = mdl_updater.model_updater(m)
    u.hostname_refresh()
    u.defaults_refresh()
    u.load_confg(m.cluster_name)
    u.mon_members_refresh()
    keyobj = keyring.keyring_facard(m)
    keyobj.key_type = keyring_type
    if secret is not None:
        utils.is_valid_base64(secret)
        return keyobj.write_secret(secret)
    if key_content is not None:
        return keyobj.write_content(key_content)
    raise Error("Set either the key_content or the key `secret`")

def keyring_auth_add_type(**kwargs):
    keyring_type = kwargs.get("keyring_type")
    if (keyring_type is None):
        raise Error("keyring_type is None")
    if (keyring_type in set(["mon","admin"])):
        raise Error("keyring_type is %s" % (keyring_type))
    m = model.model(**kwargs)
    u = mdl_updater.model_updater(m)
    u.hostname_refresh()
    u.defaults_refresh()
    u.load_confg(m.cluster_name)
    u.mon_members_refresh()
    q = mdl_query.mdl_query(m)
    if q.mon_is():
        u.mon_status()
    keyobj = keyring.keyring_facard(m)
    keyobj.key_type = keyring_type
    if not keyobj.present():
        raise Error("keyring not present")
    mur = mdl_updater_remote.model_updater_remote(m)
    can_connect = mur.connect()
    if not can_connect:
        raise Error("Cant connect to cluster.")
    return mur.auth_add(keyring_type)



def keyring_auth_del_type(**kwargs):
    """
    Write rgw keyring for cluster

    CLI Example:

        salt '*' sesceph.keyring_mds_auth_del \\
                'cluster_name'='ceph' \\
                'cluster_uuid'='cluster_uuid'
    Notes:

    cluster_uuid
        Set the cluster UUID. Defaults to value found in ceph config file.

    cluster_name
        Set the cluster name. Defaults to "ceph".
    """
    keyring_type = kwargs.get("keyring_type")
    if (keyring_type is None):
        raise Error("keyring_type is None")
    if (keyring_type in set(["mon","admin"])):
        raise Error("keyring_type is %s" % (keyring_type))
    m = model.model(**kwargs)
    u = mdl_updater.model_updater(m)
    u.hostname_refresh()
    u.defaults_refresh()
    u.load_confg(m.cluster_name)
    u.mon_members_refresh()
    q = mdl_query.mdl_query(m)
    if q.mon_is():
        u.mon_status()
    keyobj = keyring.keyring_facard(m)
    keyobj.key_type = keyring_type
    if not keyobj.present():
        raise Error("keyring not present")
    mur = mdl_updater_remote.model_updater_remote(m)
    can_connect = mur.connect()
    if not can_connect:
        raise Error("Cant connect to cluster.")
    return mur.auth_del(keyring_type)



