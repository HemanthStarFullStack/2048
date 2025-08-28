from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from mygame.controllers.game_logic import get_board, move_up, move_down, move_left, move_right, update_db_from_board, add_new_tile
import json

class Command(BaseCommand):
    help = 'Tests the 2048 game logic'

    def handle(self, *args, **options):
        self.stdout.write("Starting game logic test...")

        # Create a user
        username = 'testuser_cmd'
        password = 'testpassword123'
        try:
            user = User.objects.get(username=username)
            user.delete()
        except User.DoesNotExist:
            pass
        user = User.objects.create_user(username=username, password=password)
        self.stdout.write(f"Created user: {username}")

        # Login
        client = Client()
        login_successful = client.login(username=username, password=password)
        if not login_successful:
            self.stdout.write(self.style.ERROR("Login failed!"))
            return

        self.stdout.write(self.style.SUCCESS("Login successful!"))

        # Get the home page
        response = client.get('/')
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Failed to get home page. Status code: {response.status_code}"))
            return

        self.stdout.write("Successfully fetched the home page.")

        # The board should be initialized automatically by the home_page view
        # Let's get the board from the database to check
        user_profile = user.userprofile
        matrix = user_profile.matrix
        board, score = get_board(matrix)

        self.stdout.write("Initial board:")
        self.print_board(board)
        self.stdout.write(f"Initial score: {score}")

        # Test a move
        self.stdout.write("\nTesting move up...")
        response = client.post('/moveup/')
        self.handle_move_response(response, "up")

        self.stdout.write("\nTesting move down...")
        response = client.post('/movedown/')
        self.handle_move_response(response, "down")

        self.stdout.write("\nTesting move left...")
        response = client.post('/moveleft/')
        self.handle_move_response(response, "left")

        self.stdout.write("\nTesting move right...")
        response = client.post('/moveright/')
        self.handle_move_response(response, "right")

        self.stdout.write(self.style.SUCCESS("\nTest finished successfully!"))

    def handle_move_response(self, response, move):
        if response.status_code == 200:
            data = response.json()
            self.stdout.write(f"Board after move {move}:")
            self.print_board(data['board'])
            self.stdout.write(f"Score: {data['score']}")
        else:
            self.stdout.write(self.style.ERROR(f"Move {move} failed. Status code: {response.status_code}"))

    def print_board(self, board):
        for row in board:
            self.stdout.write(" ".join([str(cell).rjust(4) for cell in row]))
