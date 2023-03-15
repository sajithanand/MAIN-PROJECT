from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('user_login',views.user_login,name='user_login'),
    path('user_register',views.user_register,name='user_registration'),
    path('reg',views.reg,name='reg'),
    path('user_hom',views.user_hom,name='user_hom'),
    path('restaurant_reg',views.restaurant_reg,name='restaurant_reg'),
    path('rest_reg',views.rest_reg,name='rest_reg'),
    path('user_update',views.user_update,name='user_update'),
    path('use_update',views.use_update,name='use_update'),
    path('restaurant_home',views.restaurant_home,name='restaurant_home'),
    path('accept/<int:id>',views.accept,name='accept'),
    path('rejected/<int:id>',views.rejected,name='rejected'),
    path('verify_restaurants',views.verify_restaurants,name='verify_restaurants'),
    path('res_update',views.res_update,name='res_update'),
    path('update',views.update,name='update'),
    path('home_page',views.home_page,name='home_page'),
    path('login_page',views.login_page,name='login_page'),
    path('about',views.about,name='about'),
    path('service',views.service,name='service'),
    path('view_more/<int:id>',views.view_more,name='view_more'),
    path('add_facility',views.add_facility,name='add_facility'),
    path('add_facili',views.add_facili,name='add_facili'),
    path('manage',views.manage,name='manage'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('add_food',views.add_food,name='add_food'),
    path('add_food_type',views.add_food_type,name='add_food_type'),
    path('manage_foodtype',views.manage_foodtype,name='manage_foodtype'),
    path('edit_foodtypes/<int:id>',views.edit_foodtypes,name='edit_foodtypes'),
    path('edit',views.edit,name='edit'),
    path('map1',views.map1,name='map1'),
    path('map',views.map,name='map'),
    path('delete_foodtype/<int:id>',views.delete_foodtype,name='delete_foodtype'),
    path('home',views.home,name='home'),
    path('rest_home',views.rest_home,name='rest_home'),
    path('add_item',views.add_item,name='add_item'),
    path('add_fooitem',views.add_fooitem,name='add_fooitem'),
    path('manage_item',views.manage_item,name='manage_item'),
    path('edit_foodtypes',views.edit_foodtypes,name='edit_foodtypes'),
    path('getitem',views.getitem,name='getitem'),
    path('edit_fooditem/<int:id>',views.edit_fooditem,name='edit_fooditem'),
    path('edit_food',views.edit_food,name='edit_food'),
    path('delete_item/<int:id>',views.delete_item,name='delete_item'),
    path('view_restaurants',views.view_restaurants,name='view_restaurants'),
    path('web_scrapping',views.web_scrapping,name='web_scrapping'),
    path('viewresults/<int:id>',views.viewresults,name='viewresults'),
    
    path('feedback',views.feedback,name='feedback'),
    path('feedback1',views.feedback1,name='feedback1'),
    path('view_feedback',views.view_feedback,name='view_feedback'),
    path('get_rest',views.get_rest,name='get_rest'),
    path('send_complaint',views.send_complaint,name='send_complaint'),
    path('view_compliant',views.view_compliant,name='view_compliant'),
    path('reply/<int:id>',views.reply,name='reply'),
    path('reply1',views.reply1,name='reply1'),
    path('View_reply',views.View_reply,name='View_reply'),
    path('search',views.search,name='search'),
    
    
    
    
    # path('user_register',views.user_register,name='user_registration'),
    
    
   
]