from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models import Game, Player
from games.serializers import GameSerializer, PlayerSerializer



class GameListCreateAPIView(APIView):
    def post(self, request):
        serializer = GameSerializer(data={'started_by': request.user.id})
        if serializer.is_valid():
            serializer.save()
            # add user as player
            player_serializer = PlayerSerializer(data={'game': serializer.data["id"], 'user': request.user.id})
            if not player_serializer.is_valid():
                return Response(player_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            player_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        paginator = PageNumberPagination()
        games = Game.objects.filter(status='initiated')
        serializer = GameSerializer(games, many=True)
        paginator.paginate_queryset(games, request)
        return paginator.get_paginated_response(serializer.data)

class GameDetailAPIView(APIView):

    def get(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def put(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        serializer = GameSerializer(game, data=request.data)
        if serializer.is_valid():
            if game.status == 'initiated' and request.data.get('status') == 'active':
                print("Games should started")
                pass
                # send notifications to users that game has started
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PlayerListCreateAPIView(APIView):
    def get(self, request, game_pk):
        game = get_object_or_404(Game, pk=game_pk)
        paginator = PageNumberPagination()
        players = Player.objects.filter(game=game)
        paginated_games = paginator.paginate_queryset(players, request)
        serializer = PlayerSerializer(players, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, game_pk):
        game = get_object_or_404(Game, pk=game_pk)
        if not game.status == 'initiated':
            Response({"error":"Game has started"}, status=status.HTTP_400_BAD_REQUEST)
        player_serializer = PlayerSerializer(data={'game': game_pk, 'user': request.user.id})
        if player_serializer.is_valid():
            player_serializer.save()
            return Response(player_serializer.data, status=status.HTTP_201_CREATED)
        return Response(player_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
