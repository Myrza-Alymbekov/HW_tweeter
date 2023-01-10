from rest_framework.decorators import action
from rest_framework.response import Response
from tweeter import api
from tweeter.serializers import FanSerializer


class LikedMixin:

    @action(detail=True, methods=['get'])
    def like(self, request, pk=None):
        obj = self.get_object()
        if api.is_fan_like(obj, request.user):
            api.remove_like(obj, request.user)
            return Response('Ты забрал свой лайк!')
        api.add_like(obj, request.user)
        api.remove_dislike(obj, request.user)

        return Response("Дякую за лайк!")

    # @action(detail=True, methods=['get'])
    # def unlike(self, request, pk=None):
    #     obj = self.get_object()
    #     api.remove_like(obj, request.user)
    #
    #     return Response("Ты забрал свой лайк!")

    @action(detail=True, methods=['get'])
    def get_fans_like(self, request, pk=None):
        obj = self.get_object()
        fans = api.get_fans_like(obj)
        serializer = FanSerializer(fans, many=True)

        return Response(serializer.data)


class DislikedMixin:
    @action(detail=True, methods=['get'])
    def dislike(self, request, pk=None):
        obj = self.get_object()
        if api.is_fan_dislike(obj, request.user):
            api.remove_dislike(obj, request.user)
            return Response('Ты забрал свой дизлайк!')
        api.remove_like(obj, request.user)
        api.add_dislike(obj, request.user)

        return Response("Ты поставил дизлайк!")

    # @action(detail=True, methods=['post'])
    # def undislike(self, request, pk=None):
    #     obj = self.get_object()
    #     api.remove_dislike(obj, request.user)
    #
    #     return Response()

    @action(detail=True, methods=['get'])
    def get_fans_dislike(self, request, pk=None):
        obj = self.get_object()
        fans = api.get_fans_dislike(obj)
        serializer = FanSerializer(fans, many=True)

        return Response(serializer.data)
