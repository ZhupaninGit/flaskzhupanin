from app.post import bp
from flask import render_template,redirect,url_for,flash,request
from .form import postForm,changePostForm,categoryForm,categoryFormChange,tagForm,changeTag
from app.models import Post,EnumPost,Category,Tag
from app import db
from .photo import save_photo,delete_photo
from flask_login import current_user,login_required
from sqlalchemy import desc

@bp.route("/<int:post_id>",methods=["GET","POST"])
@bp.route('/',methods=["GET","POST"])
def post(post_id = None):
    page = request.args.get('page', 1, type=int)
    postlist = Post.query.paginate(page=page, per_page=3) 
    if post_id is not None:
        currentPost = db.session.get(Post,post_id)
        category = db.session.get(Category,currentPost.category_id)
        return render_template("currentpost.html",active="Пости",title=f"Пост №{post_id}",currentPost=currentPost,EnumPost=EnumPost,category=category)
    post = postForm()
    return render_template("post.html",active="Пости",title="Пости",postlist=postlist,EnumPost=EnumPost,post=post)

from flask import request

@bp.route('/post/categories/<int:category_id>')
def posts_in_category(category_id):
    category = db.session.get(Category,category_id)
    page = request.args.get('page', 1, type=int)
    postlist = Post.query.filter_by(category_id=category.id).order_by(Post.created.desc()).paginate(page=page, per_page=3)
    return render_template('categoriesposts.html',active="Пости", postlist=postlist, EnumPost=EnumPost, categoryname=category.name,category_id=category_id)


@bp.route('/newpost',methods=["GET","POST"])
@login_required
def addnewpost():
    post = postForm()
    if post.validate_on_submit():
        image = "default.jpg"
        type = "other"
        if post.image.data:
            image = save_photo(post.image.data)
        type = post.type.data
        category = db.session.get(Category,int(post.category.data))
        newpost = Post(title=post.newpost.data,text=post.newposttext.data,image=image,enabled=post.enabled.data,type=type,user_id=current_user.id,category=category)
        db.session.add(newpost)
        db.session.commit()
        selected_tags = post.tag.data
        for tag_id in selected_tags:
            tag = Tag.query.get(tag_id)
            if tag:
                newpost.tags.append(tag)


        db.session.commit()
        flash("Пост був успішно доданий!","successs")
        return redirect(url_for("post.post"))
    return render_template("newpost.html",active="Пости",title="Пости",post=post,EnumPost=EnumPost)


@bp.route("/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = db.session.get(Post,post_id)
    if post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        flash("Пост успішно видалений", "successs")
        return redirect(url_for("post.post"))


@bp.route("/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    formChange = changePostForm()
    post = db.session.get(Post,post_id)
   
    if formChange.validate_on_submit():
        try:
            if formChange.image.data:
                delete_photo(post.image)
                picture_file = save_photo(formChange.image.data)
                post.image = picture_file
            post.title = formChange.newpost.data
            post.text = formChange.newposttext.data
            post.enabled = formChange.enabled.data
            post.type = formChange.type.data
            category = db.session.get(Category,int(formChange.category.data))
            post.category = category
            selected_tags = formChange.tag.data
            for tag_id in selected_tags:
                tag = Tag.query.get(tag_id)
                if tag:
                    post.tags.append(tag)
            db.session.commit()
            flash('Успішне оновлення посту.', category='successs')
            return redirect(url_for("post.post",post_id=post_id))
        except:
            flash('Щось пішло не так.', category='error')
            return redirect(url_for("post.post",post_id=post_id))
    elif request.method == "GET":
        formChange.newpost.data = post.title
        formChange.newposttext.data = post.text
        formChange.enabled.data = post.enabled
        formChange.type.data = post.type
        formChange.category.data = post.category

    return render_template('changepost.html', formChange=formChange,title="Post",postid=post_id,active="Пости")

@bp.route('/category', methods=["GET", "POST"])
def category():
    form = categoryForm()
    categories = db.session.query(Category).all()
    if form.validate_on_submit():
        name = form.name.data.strip()
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            flash(f"Категорія {name} вже існує.", "error")
        else:
            new_category = Category(name=form.name.data)
            db.session.add(new_category)
            db.session.commit()
            flash(f"Категорія {name} додана.", "successs")
            return redirect(url_for("post.category"))
        
    return render_template("categories.html", active="Пости", title="Категорії", categories=categories, form=form)

@bp.route("/<int:category_id>/category/delete", methods=["GET", "POST"])
@login_required
def delete_category(category_id):
    category = db.session.get(Category,category_id)
    db.session.delete(category)
    db.session.commit()
    flash(f"Категорія {category.name} успішно видалена", "successs")
    return redirect(url_for("post.category"))

@bp.route("/<int:category_id>/category/change", methods=["GET", "POST"])
@login_required
def change_category(category_id):
    form = categoryFormChange()
    category = db.session.get(Category,category_id)
    if form.validate_on_submit():
        name = form.name.data.strip()
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            flash(f"Категорія {name} вже існує.", "error")
            return redirect(url_for("post.category"))
        else:
            category.name = form.name.data
            db.session.commit()
            flash(f"Категорія успішно оновлена", "successs")
            return redirect(url_for("post.category"))
    return render_template("changecategory.html",active="Пости",title="Редагування категорії",form=form,categoryid=category_id,name=category.name)

@bp.route('/tag/', methods=["GET", "POST"])
@login_required
def tag():
    form = tagForm()
    tags = db.session.query(Tag).all()
    if form.validate_on_submit():
        name = form.name.data.strip()
        existing_tag = Tag.query.filter_by(name=name).first()
        if existing_tag:
            flash(f"Тег '{name}' вже існує.", "error")
        else:
            new_tag = Tag(name=form.name.data)
            db.session.add( new_tag)
            db.session.commit()
            flash(f"Тег '{name}' доданий.", "successs")
            return redirect(url_for("post.tag"))


    return render_template("tag.html", active="Пости", title="Теги", tags=tags, form=form)

@bp.route("/<int:tag_id>/tag/delete", methods=["GET", "POST"])
@login_required
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Тег '{tag.name}' успішно видалений", "successs")
    return redirect(url_for("post.tag"))