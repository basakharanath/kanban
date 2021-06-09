from django.urls import path, include
from users.views import *
from boards.views import *


urls = [
    path('user/login/', user_login),
    path('user/signup/', user_signup),

    path('board/byuserid/', board_details),
    path('board/create/', create_board),
    path('board/update/', update_board),

    path('boardlist/create/', create_list),
    path('boardlist/update/', update_list),

    path('listcard/create/', create_card),
    path('listcard/update/', update_card),
    path('listcard/movecard/', move_card),

    path('cardattachment/create/', create_card_attachment),
    path('cardattachment/update/', update_card_attachment),

]