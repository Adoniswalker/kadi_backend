from django.db import models

from users.models import CustomUser



class Game(models.Model):
    status_choices = [
        ('initiated', 'initiated'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50, choices=status_choices,
                              default='initiated')
    started_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Game {self.id} ({self.status})"


class Player(models.Model):
    status_choices = [
        ('playing', 'Playing'),
        ('waiting', 'Waiting'),
    ]

    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, related_name='players',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='players',
                             on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=status_choices,
                              default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Player {self.user.email} in Game {self.game.id}"


class Deck(models.Model):
    game = models.ForeignKey(Game, related_name='decks',
                             on_delete=models.CASCADE)
    card_order = models.JSONField()  # Store cards as a list of card identifiers (e.g., '2H', 'KC', etc.)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deck for Game {self.game.id}"


class Hand(models.Model):
    player = models.ForeignKey(Player, related_name='hands',
                               on_delete=models.CASCADE)
    cards = models.JSONField()  # Store the player's cards as a list of card identifiers
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hand of {self.player.user.email} in Game {self.player.game.id}"


class Move(models.Model):
    move_type_choices = [
        ('play', 'Play'),
        ('draw', 'Draw'),
    ]

    game = models.ForeignKey(Game, related_name='moves',
                             on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='moves',
                               on_delete=models.CASCADE)
    card_played = models.CharField(
        max_length=10)  # Store card identifier (e.g., '2H', 'KC', etc.)
    move_type = models.CharField(max_length=10, choices=move_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Move by {self.player.user.email} in Game {self.game.id}"


class Penalty(models.Model):
    penalty_type_choices = [
        ('draw_2', 'Draw 2'),
        ('draw_3', 'Draw 3'),
        ('draw_5', 'Draw 5'),
    ]

    player = models.ForeignKey(Player, related_name='penalties',
                               on_delete=models.CASCADE)
    penalty_type = models.CharField(max_length=10,
                                    choices=penalty_type_choices)
    penalty_amount = models.IntegerField()  # Number of cards the player needs to draw
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Penalty for {self.player.user.email} in Game {self.player.game.id}"


class Chat(models.Model):
    game = models.ForeignKey(Game, related_name='chat',
                             on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='chat',
                               on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat message by {self.player.user.email} in Game {self.game.id}"
