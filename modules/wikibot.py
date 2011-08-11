import re
import api

class Module(api.Module):
    wiki_url = 'https://secure.wikimedia.org/wikipedia/en/wiki/%s'
    def privmsg(self, nick, data, channel):
        data = api.get_message(data)
        if re.search('\[\[.*\]\]', data):
            word = data[data.find('[[') + 2:data.find(']]')]
            self.msg(channel, self.wiki_url % word)