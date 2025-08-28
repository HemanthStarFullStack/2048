from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mygame.models import UserProfile, Cell
from mygame.controllers.game_logic import get_board, start_game
import json

@login_required
def home_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    matrix = user_profile.matrix
    
    # if no cells, start a new game
    if not Cell.objects.filter(matrix=matrix).exists():
        start_game(matrix)

    board, score = get_board(matrix)

    context = {
        'board': json.dumps(board),
        'score': score
    }
    return render(request, 'page.html', context)