from inspect import getsourcefile
from os.path import abspath, dirname, join
from twisted.application import internet, service
from twisted.web import static, server, resource
from twisted.internet import reactor
import yaml



base_path = dirname(abspath(getsourcefile(lambda _: None)))
config_file = join(base_path,"config.yaml")

with open(config_file, 'r+') as config_lines:
    config = yaml.load(config_lines.read())

webroot = config['server']['web_root'].format(base_path)



root=static.File(webroot)
root.indexNames=['index.asis']
#root.processors = { '.asis' : static.ASISProcessor}
#application = service.Application('web')
#sc = service.IServiceCollection(application)
site = server.Site(root)

reactor.listenTCP(config['server']['port'], server.Site(root), 
                    interface=config['server']['bind'])
reactor.run()
