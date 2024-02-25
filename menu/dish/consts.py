from menu.category.handlers import category_list_redirect_handler, category_detail_redirect_handler


class DishDetailRedirect:
    category_list = 'category_list'
    category_detail = 'category_detail'


DISH_DETAIL_REDIRECT_FUNCTION = {
    DishDetailRedirect.category_list: category_list_redirect_handler,
    DishDetailRedirect.category_detail: category_detail_redirect_handler
}