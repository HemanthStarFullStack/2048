from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from mygame.models import UserProfile
from mygame.controllers.game_logic import get_board, move_down, update_db_from_board, add_new_tile
import json

@login_required
def movedown(request):
    user_profile = UserProfile.objects.get(user=request.user)
    matrix = user_profile.matrix

    board, _ = get_board(matrix)

    new_board, score_add = move_down(board)

    if new_board != board:
        update_db_from_board(matrix, new_board)
        add_new_tile(matrix)

    final_board, final_score = get_board(matrix)

    return JsonResponse({'board': final_board, 'score': final_score})
