#--depends-on check_mode
#--depends-on commands
#--depends-on permissions

import binascii, enum, os, uuid
from src import ModuleManager, utils

STR_NOVOTE = "Unknown vote '%s'"

class Module(ModuleManager.BaseModule):
    def _get_vote(self, channel, vote_id):
        return channel.get_setting("vote-%s" % vote_id, None)
    def _format_vote(self, vote):
        options = ["%d %s" % (len(v), k) for k, v in vote["options"].items()]
        return "%s (%s)" % (vote["description"], ", ".join(options))
    def _format_options(self, vote):
        return ", ".join("'%s'" % o for o in vote["options"])

    @utils.hook("received.command.voters", channel_only=True, min_args=1)
    def end_vote(self, event):
        """
        :help: See voters for vote id
        :usage: <id>
        """
        vote_id = event["args_split"][0]
        vote = self._get_vote(event["target"], vote_id)

        if vote:
            event["stdout"].write("Voters for %s: %s" %
                (vote_id, self._format_vote(vote)))
        else:
            event["stderr"].write(STR_NOVOTE % vote_id)
