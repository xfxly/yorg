from yyagl.gameobject import GameObject
from yyagl.engine.logic import VersionChecker
from .usersfrm import UsersFrm
from .matchfrm import MatchFrm
from .messagefrm import MessageFrm
from .friend_dlg import FriendDialog


class MultiplayerFrm(GameObject):

    def __init__(self, menu_args):
        GameObject.__init__(self)
        self.dialog = None
        self.ver_check = VersionChecker()
        self.labels = []
        self.invited_users = []
        self.menu_args = menu_args
        self.users_frm = UsersFrm(menu_args)
        self.users_frm.attach(self.on_invite)
        self.users_frm.attach(self.on_add_chat)
        self.users_frm.attach(self.on_add_groupchat)
        self.match_frm = MatchFrm(menu_args)
        self.match_frm.attach(self.on_start)
        self.msg_frm = MessageFrm(menu_args)
        self.msg_frm.attach(self.on_msg_focus)
        self.eng.xmpp.attach(self.on_users)
        self.eng.xmpp.attach(self.on_user_connected)
        self.eng.xmpp.attach(self.on_user_disconnected)
        self.eng.xmpp.attach(self.on_user_subscribe)
        self.eng.xmpp.attach(self.on_presence_available)
        self.eng.xmpp.attach(self.on_presence_unavailable)
        self.eng.xmpp.attach(self.on_msg)
        self.eng.xmpp.attach(self.on_groupchat_msg)
        self.eng.xmpp.attach(self.on_invite_chat)

    def show(self):
        self.users_frm.show()
        self.match_frm.show()
        self.msg_frm.show()

    def hide(self):
        self.users_frm.hide()
        self.match_frm.hide()
        self.msg_frm.hide()

    def on_user_subscribe(self, user):
        self.dialog = FriendDialog(self.menu_args, user)
        self.dialog.attach(self.on_friend_answer)

    def on_friend_answer(self, user, val):
        self.dialog.detach(self.on_friend_answer)
        self.dialog = self.dialog.destroy()
        self.eng.xmpp.client.send_presence_subscription(
            pto=user,
            pfrom=self.eng.xmpp.client.boundjid.full,
            ptype='subscribed' if val else 'unsubscribed')

    def on_invite(self, usr):
        self.match_frm.on_invite(usr)

    def on_users(self): self.users_frm.on_users()

    def on_user_connected(self, user): self.users_frm.on_users()

    def on_user_disconnected(self, user): self.users_frm.on_users()

    def on_presence_available(self, user): self.users_frm.on_users()

    def on_presence_unavailable(self, user): self.users_frm.on_users()

    def on_start(self): self.users_frm.room_name = None

    def on_msg(self, msg): self.msg_frm.on_msg(msg)

    def on_groupchat_msg(self, msg): self.msg_frm.on_groupchat_msg(msg)

    def on_invite_chat(self, msg):
        self.msg_frm.add_groupchat(str(msg['body']), str(msg['from'].bare))
        self.eng.xmpp.client.plugin['xep_0045'].joinMUC(
            msg['body'], self.eng.xmpp.client.boundjid.bare)

    def on_add_chat(self, usr): self.msg_frm.add_chat(usr)

    def on_add_groupchat(self, room, usr): self.msg_frm.add_groupchat(room, usr)

    def on_msg_focus(self, val): self.notify('on_msg_focus', val)

    def destroy(self):
        self.frm = self.frm.destroy()
        GameObject.destroy(self)