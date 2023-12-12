from app import db
from app.models import User,Category,Post
from flask_login import current_user
def test_posts_page_view(client):
    response = client.get('/post/', follow_redirects=True)
    assert response.status_code == 200
    assert b"posts" in response.data

def test_new_post_page_without_authorizing_view(client):
    response = client.get('/post/newpost', follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Щоб побачити цю сторінку необхідно авторизуватися" in html
    assert response.request.path == "/login/"

def test_tag_page_without_authorizing_view(client):
    response = client.get('/post/tag/', follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Щоб побачити цю сторінку необхідно авторизуватися" in html
    assert response.request.path == "/login/"

def test_new_post_page_with_authorizing_view(login_test_user,client):
    response = client.get('/post/newpost', follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Новий пост" in html
    assert response.request.path == "/post/newpost"

def test_tag_page_with_authorizing_view(login_test_user,client):
    response = client.get('/post/tag/', follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Теги" in html
    assert response.request.path == "/post/tag/"

def test_categories_page_view(client):
    response = client.get('post/category', follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Категорії" in html
    

def test_posts_in_categorie_page_view(client):
    newcategory = Category(name="Newcategory")
    db.session.add(newcategory)
    db.session.commit()
    response = client.get('post/post/categories/1', follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'Список постів категорії "Newcategory"' in html

def test_post_page_view(client):
    newpost = Post(title="New title",text="text",user_id=1,category_id=1)
    db.session.add(newpost)
    db.session.commit()
    response = client.get('post/1', follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'New title' in html

#===============================================================#
#==========================Post CRUD tests===========================#
#===============================================================#

def test_add_new_post(client,login_test_user):
    response = client.post('/post/newpost', data={
            'newpost': 'New title',
            'newposttext': 'New text',
            'enabled': 'y',
            'type':'other',
            'category':1
        }, follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    print(html)
    print(response.request.path)
    assert 'Пост був успішно доданий!' in html

def test_change_post(client,login_test_user):
    response = client.post('/post/2/update', data={
            'newpost': 'Newest post title',
            'newposttext': 'Newest post text',
            'enabled': 'y',
            'type':'other',
            'category':1
        }, follow_redirects=True)
    assert response.status_code == 200
    post = db.session.get(Post,2)
    assert post.title == "Newest post title"
    html = response.get_data(as_text=True)
    assert 'Успішне оновлення посту.' in html

def test_delete_post(client,login_test_user):
    response = client.get('post/2/delete', follow_redirects=True)
    assert response.status_code == 200
    post = db.session.get(Post,2)
    assert post == None
    html = response.get_data(as_text=True)
    assert 'Пост успішно видалений' in html
    
def test_add_new_category(client,login_test_user):
    response = client.post('/post/category', data={
            'name': 'Driving',
        }, follow_redirects=True)
    assert response.status_code == 200
    category = db.session.get(Category,2)
    assert category.name == 'Driving'
    html = response.get_data(as_text=True)
    print(html)
    assert "Категорія Driving додана." in html

def test_add_existing_category(client,login_test_user):
    response = client.post('/post/category', data={
            'name': 'Driving',
        }, follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    print(html)
    assert "Категорія Driving вже існує." in html

def test_change_existing_category(client,login_test_user):
    response = client.post('post/2/category/change', data={
            'name': 'New category',
        }, follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    print(html)
    assert "Категорія успішно оновлена" in html

def test_delete_category(client,login_test_user):
    response = client.get('post/2/category/delete', follow_redirects=True)
    assert response.status_code == 200
    post = db.session.get(Category,2)
    assert post == None
    html = response.get_data(as_text=True)
    assert 'Категорія New category успішно видалена' in html    