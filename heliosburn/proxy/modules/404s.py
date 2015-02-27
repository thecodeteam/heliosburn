from module import AbstractModule


class allFail(AbstractModule):

    def onResponse(self, **kwargs):
        self.response_object.handleStatus(version='HTTP/1.1',
                                          code=404,
                                          message="Sorry bub, Not found")

all_fail = allFail()
