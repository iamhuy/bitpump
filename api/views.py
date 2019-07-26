from common.views import BaseApiView


class TestView(BaseApiView):
    permission_classes = ()

    http_method_names = ['get']

    def get_valid(self, serializer):
        reply = {
            'test': 'test',
        }

        return self.reply(reply)
