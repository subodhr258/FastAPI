from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostBase(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/8888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostBase(**res.json())
    #some more validation

@pytest.mark.parametrize("title, content, published",[ 
    ("awesome new title","awesome new content",True),
    ("pizza","pepperoni",False),
    ("skyscraper","wahoo",True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={'title':title, 'content':content, 'published':published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post("/posts/", json={'title':'titleee', 'content':"contenttt"})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == 'titleee'
    assert created_post.content == "contenttt"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title":"arbitrary title", "content":"sagsdfg"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/100000")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[2].id}"
    )
    assert res.status_code == 403

# def test_update_post(authorized_client, test_user, test_posts):
#     data = {
#         "title": "updated title",
#         "content": "updated content",
#         "id" : test_posts[0].id
#     }
#     res = authorized_client.put(f"/posts/{test_posts[0].id}",json=data)
#     updated_post = schemas.Post(**res.json())
#     assert res.status_code == 200
#     assert updated_post.title == data['title']
#     assert updated_post.content == data['content']

#   and a few other tests

